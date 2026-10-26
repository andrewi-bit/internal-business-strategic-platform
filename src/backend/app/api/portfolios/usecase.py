from decimal import Decimal
from uuid import UUID

from app.api.customers.repository import CustomerRepository
from app.api.customers.usecase import CustomerUseCase, page_meta
from app.api.portfolios import calculations as calc
from app.api.portfolios.references import ReferenceChecker
from app.api.portfolios.repository import PortfolioFilters, PortfolioRepository
from app.api.portfolios.schema import (
    PortfolioCreateRequest,
    PortfolioSortBy,
    PortfolioUpdateRequest,
    SortOrder,
)
from app.api.portfolios.serializers import (
    serialize_portfolio_detail,
    serialize_portfolio_row,
)
from app.models.business_unit_model import BusinessUnit
from app.models.partner_model import Partner
from app.models.product_model import Product
from app.models.project_financial_model import ProjectFinancial
from app.models.project_model import Project
from app.models.project_partner_model import ProjectPartner
from app.models.project_product_model import ProjectProduct
from app.models.project_status_model import ProjectStatus
from app.models.project_tech_stack_model import ProjectTechStack
from app.models.tech_stack_model import TechStack
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

CODE_TAKEN = "Project ID (project_code) sudah digunakan."


class PortfolioUseCase:
    def __init__(self, repository: PortfolioRepository):
        self.repository = repository
        self.customers = CustomerUseCase(CustomerRepository(repository.db))

    # ------------------------------------------------------------------ reads
    async def list_portfolios(
        self,
        filters: PortfolioFilters,
        sort_by: PortfolioSortBy,
        sort_order: SortOrder,
        page: int,
        page_size: int,
    ):
        projects, total = await self.repository.list_projects(
            filters, sort_by, sort_order, page, page_size
        )
        today = calc.today_wib()
        return [serialize_portfolio_row(p, today) for p in projects], page_meta(page, page_size, total)

    async def get_portfolio(self, project_id: UUID):
        project = await self.repository.get_project(project_id)
        if project is None:
            raise HTTPException(404, "Portofolio tidak ditemukan.")
        return serialize_portfolio_detail(project, calc.today_wib())

    async def summary(self):
        today = calc.today_wib()
        totals = await self.repository.summary_totals()
        ending = await self.repository.ending_soon(today)

        return {
            "totals": totals,
            "by_status": await self.repository.group_by_status(),
            "by_business_unit": await self.repository.group_by_business_unit(),
            "by_industry": await self.repository.group_by_industry(),
            "by_company_size": await self.repository.group_by_company_size(),
            "by_year": await self.repository.group_by_year(),
            "by_product": await self.repository.group_by_product(),
            "ending_soon": [serialize_portfolio_row(p, today) for p in ending],
        }

    # ------------------------------------------------------------------ helpers
    async def _check_references(
        self,
        *,
        business_unit_id=None,
        project_status_id=None,
        product_ids=None,
        tech_stack_ids=None,
        partner_ids=None,
        existing_products=(),
        existing_tech_stacks=(),
        existing_partners=(),
    ) -> None:
        checker = ReferenceChecker(self.repository.db)

        if business_unit_id is not None:
            await checker.check("project.business_unit_id", BusinessUnit, [business_unit_id])
        if project_status_id is not None:
            await checker.check("project.project_status_id", ProjectStatus, [project_status_id])
        # Item yang sudah terpasang boleh tetap ada walau master-nya sudah dinonaktifkan;
        # hanya item yang baru ditambahkan yang harus aktif.
        if product_ids:
            await checker.check("product_ids", Product, set(product_ids) - set(existing_products))
        if tech_stack_ids:
            await checker.check(
                "tech_stack_ids", TechStack, set(tech_stack_ids) - set(existing_tech_stacks)
            )
        if partner_ids:
            await checker.check("partners", Partner, set(partner_ids) - set(existing_partners))

        checker.raise_if_invalid()

    @staticmethod
    def _check_dates(start, end) -> None:
        if end < start:
            raise HTTPException(
                422,
                detail={
                    "code": "INVALID_DATE_RANGE",
                    "message": "end_date tidak boleh lebih awal dari start_date.",
                    "details": None,
                },
            )

    async def _ensure_unique_code(self, code: str, exclude_id: UUID | None = None) -> None:
        existing = await self.repository.get_project_by_code(code)
        if existing is not None and existing.id != exclude_id:
            raise HTTPException(409, CODE_TAKEN)

    async def _commit(self) -> None:
        try:
            await self.repository.save()
        except IntegrityError as error:
            await self.repository.rollback()
            text = str(error.orig)
            if "project_code" in text:
                raise HTTPException(409, CODE_TAKEN)
            if "customer_name" in text:
                raise HTTPException(409, "Nama customer sudah digunakan.")
            raise HTTPException(409, "Data bentrok dengan data yang sudah ada.")

    # ------------------------------------------------------------------ writes
    async def create_portfolio(self, payload: PortfolioCreateRequest, user_id: UUID | None):
        project_in = payload.project
        partner_ids = [item.partner_id for item in payload.partners]

        await self._check_references(
            business_unit_id=project_in.business_unit_id,
            project_status_id=project_in.project_status_id,
            product_ids=payload.product_ids,
            tech_stack_ids=payload.tech_stack_ids,
            partner_ids=partner_ids,
        )
        await self._ensure_unique_code(project_in.project_code)

        if payload.customer is not None:
            customer = await self.customers.build_customer(payload.customer, user_id)
            await self.repository.flush()
            customer_id = customer.id
        else:
            existing = await self.customers.repository.get_by_id(payload.customer_id)
            if existing is None:
                raise HTTPException(
                    422,
                    detail={
                        "code": "INVALID_REFERENCE",
                        "message": "Ada data referensi yang tidak valid.",
                        "details": [
                            {"field": "customer_id", "ids": [str(payload.customer_id)], "reason": "tidak ditemukan"}
                        ],
                    },
                )
            customer_id = existing.id

        project = Project(
            **project_in.model_dump(),
            customer_id=customer_id,
            created_by=user_id,
            updated_by=user_id,
        )
        self.repository.add(project)
        await self.repository.flush()

        revenue = payload.financial.revenue
        self.repository.add(
            ProjectFinancial(
                project_id=project.id,
                revenue=project_in.value_before_tax if revenue is None else revenue,
                cogs=payload.financial.cogs,
                operational_costs=payload.financial.operational_costs,
            )
        )
        for product_id in dict.fromkeys(payload.product_ids):
            self.repository.add(ProjectProduct(project_id=project.id, product_id=product_id))
        for tech_stack_id in dict.fromkeys(payload.tech_stack_ids):
            self.repository.add(ProjectTechStack(project_id=project.id, tech_stack_id=tech_stack_id))
        for item in payload.partners:
            self.repository.add(
                ProjectPartner(
                    project_id=project.id, partner_id=item.partner_id, partner_role=item.partner_role
                )
            )

        await self._commit()
        return await self.get_portfolio(project.id)

    async def update_portfolio(self, project_id: UUID, payload: PortfolioUpdateRequest, user_id: UUID | None):
        project = await self.repository.get_project(project_id)
        if project is None:
            raise HTTPException(404, "Portofolio tidak ditemukan.")

        sent = payload.model_fields_set
        if not sent:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        project_changes = (
            payload.project.model_dump(exclude_unset=True) if payload.project is not None else {}
        )
        financial_changes = (
            payload.financial.model_dump(exclude_unset=True) if payload.financial is not None else {}
        )

        for name in ("customer_id", "product_ids", "tech_stack_ids", "partners"):
            if name in sent and getattr(payload, name) is None:
                raise HTTPException(422, f"{name} tidak boleh null.")

        existing_products = {link.product_id for link in project.products}
        existing_tech = {link.tech_stack_id for link in project.tech_stacks}
        existing_partners = {link.partner_id for link in project.partners}

        await self._check_references(
            business_unit_id=project_changes.get("business_unit_id"),
            project_status_id=project_changes.get("project_status_id"),
            product_ids=payload.product_ids,
            tech_stack_ids=payload.tech_stack_ids,
            partner_ids=[p.partner_id for p in payload.partners] if payload.partners is not None else None,
            existing_products=existing_products,
            existing_tech_stacks=existing_tech,
            existing_partners=existing_partners,
        )

        start = project_changes.get("start_date", project.start_date)
        end = project_changes.get("end_date", project.end_date)
        self._check_dates(start, end)

        if "project_code" in project_changes:
            await self._ensure_unique_code(project_changes["project_code"], exclude_id=project.id)

        if payload.customer_id is not None:
            if await self.customers.repository.get_by_id(payload.customer_id) is None:
                raise HTTPException(
                    422,
                    detail={
                        "code": "INVALID_REFERENCE",
                        "message": "Ada data referensi yang tidak valid.",
                        "details": [
                            {"field": "customer_id", "ids": [str(payload.customer_id)], "reason": "tidak ditemukan"}
                        ],
                    },
                )
            project.customer_id = payload.customer_id

        for field, value in project_changes.items():
            setattr(project, field, value)
        project.updated_by = user_id

        if financial_changes:
            for field in ("revenue", "cogs", "operational_costs"):
                if field in financial_changes and financial_changes[field] is None:
                    raise HTTPException(422, f"financial.{field} tidak boleh null.")
            if project.financial is None:
                self.repository.add(
                    ProjectFinancial(
                        project_id=project.id,
                        revenue=financial_changes.get("revenue", project.value_before_tax),
                        cogs=financial_changes.get("cogs", Decimal(0)),
                        operational_costs=financial_changes.get("operational_costs", Decimal(0)),
                    )
                )
            else:
                for field, value in financial_changes.items():
                    setattr(project.financial, field, value)

        if payload.product_ids is not None:
            wanted = set(payload.product_ids)
            for link in list(project.products):
                if link.product_id not in wanted:
                    project.products.remove(link)
            for product_id in wanted - existing_products:
                self.repository.add(ProjectProduct(project_id=project.id, product_id=product_id))

        if payload.tech_stack_ids is not None:
            wanted = set(payload.tech_stack_ids)
            for link in list(project.tech_stacks):
                if link.tech_stack_id not in wanted:
                    project.tech_stacks.remove(link)
            for tech_stack_id in wanted - existing_tech:
                self.repository.add(ProjectTechStack(project_id=project.id, tech_stack_id=tech_stack_id))

        if payload.partners is not None:
            wanted_roles = {item.partner_id: item.partner_role for item in payload.partners}
            for link in list(project.partners):
                if link.partner_id not in wanted_roles:
                    project.partners.remove(link)
                else:
                    link.partner_role = wanted_roles[link.partner_id]
            for partner_id, role in wanted_roles.items():
                if partner_id not in existing_partners:
                    self.repository.add(
                        ProjectPartner(project_id=project.id, partner_id=partner_id, partner_role=role)
                    )

        await self._commit()
        return await self.get_portfolio(project_id)

    async def delete_portfolio(self, project_id: UUID) -> None:
        project = await self.repository.get_project(project_id)
        if project is None:
            raise HTTPException(404, "Portofolio tidak ditemukan.")

        await self.repository.delete(project)
        await self._commit()
