from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from app.api.portfolios.calculations import ACTIVE_PROJECT_STATUS_CODE
from app.api.portfolios.schema import PortfolioSortBy, SortOrder
from app.models.business_unit_model import BusinessUnit
from app.models.company_size_model import CompanySize
from app.models.customer_model import Customer
from app.models.industry_model import Industry
from app.models.product_model import Product
from app.models.project_financial_model import ProjectFinancial
from app.models.project_model import Project
from app.models.project_partner_model import ProjectPartner
from app.models.project_product_model import ProjectProduct
from app.models.project_status_model import ProjectStatus
from app.models.project_tech_stack_model import ProjectTechStack
from sqlalchemy import distinct, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

ENDING_SOON_DAYS = 90
ENDING_SOON_LIMIT = 5


@dataclass
class PortfolioFilters:
    search: str | None = None
    customer_id: UUID | None = None
    customer_name: str | None = None
    industry_id: UUID | None = None
    company_size_id: UUID | None = None
    customer_type_id: UUID | None = None
    business_unit_id: UUID | None = None
    project_status_ids: list[UUID] = field(default_factory=list)
    project_year: int | None = None
    product_id: UUID | None = None
    tech_stack_id: UUID | None = None
    partner_id: UUID | None = None
    project_manager: str | None = None
    account_manager: str | None = None
    active_only: bool = False


def like_pattern(term: str) -> str:
    """Pola ILIKE "mengandung" dengan %, _ dan \\ dari input pengguna diperlakukan sebagai huruf biasa."""
    escaped = term.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def project_load_options():
    """Semua yang dibutuhkan serializer, supaya tidak ada query tambahan per baris."""
    return (
        joinedload(Project.customer).options(
            joinedload(Customer.company_size),
            joinedload(Customer.customer_type),
            joinedload(Customer.industry),
            joinedload(Customer.legal_structure),
        ),
        joinedload(Project.business_unit),
        joinedload(Project.project_status),
        selectinload(Project.financial),
        selectinload(Project.products).joinedload(ProjectProduct.product),
        selectinload(Project.tech_stacks).joinedload(ProjectTechStack.tech_stack),
        selectinload(Project.partners).joinedload(ProjectPartner.partner),
    )


SORT_COLUMNS = {
    PortfolioSortBy.CREATED_AT: Project.created_at,
    PortfolioSortBy.PROJECT_NAME: func.lower(Project.project_name),
    PortfolioSortBy.PROJECT_CODE: func.lower(Project.project_code),
    PortfolioSortBy.CUSTOMER_NAME: func.lower(Customer.customer_name),
    PortfolioSortBy.PROJECT_YEAR: Project.project_year,
    PortfolioSortBy.START_DATE: Project.start_date,
    PortfolioSortBy.END_DATE: Project.end_date,
    PortfolioSortBy.VALUE_BEFORE_TAX: Project.value_before_tax,
}


def filter_conditions(filters: PortfolioFilters) -> list:
    conditions = []

    if filters.search and filters.search.strip():
        pattern = like_pattern(filters.search)
        conditions.append(
            or_(
                Project.project_name.ilike(pattern, escape="\\"),
                Project.project_code.ilike(pattern, escape="\\"),
                Project.opportunity.ilike(pattern, escape="\\"),
                Project.contract_po_name.ilike(pattern, escape="\\"),
                Customer.customer_name.ilike(pattern, escape="\\"),
            )
        )

    if filters.customer_id is not None:
        conditions.append(Project.customer_id == filters.customer_id)

    if filters.customer_name and filters.customer_name.strip():
        conditions.append(
            Customer.customer_name.ilike(like_pattern(filters.customer_name), escape="\\")
        )

    if filters.industry_id is not None:
        conditions.append(Customer.industry_id == filters.industry_id)

    if filters.company_size_id is not None:
        conditions.append(Customer.company_size_id == filters.company_size_id)

    if filters.customer_type_id is not None:
        conditions.append(Customer.customer_type_id == filters.customer_type_id)

    if filters.business_unit_id is not None:
        conditions.append(Project.business_unit_id == filters.business_unit_id)

    if filters.project_status_ids:
        conditions.append(Project.project_status_id.in_(filters.project_status_ids))

    if filters.active_only:
        conditions.append(
            Project.project_status_id.in_(
                select(ProjectStatus.id).where(
                    ProjectStatus.project_status_code == ACTIVE_PROJECT_STATUS_CODE
                )
            )
        )

    if filters.project_year is not None:
        conditions.append(Project.project_year == filters.project_year)

    if filters.product_id is not None:
        conditions.append(Project.products.any(ProjectProduct.product_id == filters.product_id))

    if filters.tech_stack_id is not None:
        conditions.append(
            Project.tech_stacks.any(ProjectTechStack.tech_stack_id == filters.tech_stack_id)
        )

    if filters.partner_id is not None:
        conditions.append(Project.partners.any(ProjectPartner.partner_id == filters.partner_id))

    if filters.project_manager and filters.project_manager.strip():
        conditions.append(
            Project.project_manager.ilike(like_pattern(filters.project_manager), escape="\\")
        )

    if filters.account_manager and filters.account_manager.strip():
        conditions.append(
            Project.account_manager.ilike(like_pattern(filters.account_manager), escape="\\")
        )

    return conditions


class PortfolioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ------------------------------------------------------------------ reads
    async def list_projects(
        self,
        filters: PortfolioFilters,
        sort_by: PortfolioSortBy,
        sort_order: SortOrder,
        page: int,
        page_size: int,
    ) -> tuple[list[Project], int]:
        conditions = filter_conditions(filters)

        total = (
            await self.db.execute(
                select(func.count(Project.id))
                .select_from(Project)
                .join(Customer, Customer.id == Project.customer_id)
                .where(*conditions)
            )
        ).scalar_one()

        column = SORT_COLUMNS[sort_by]
        ordering = column.desc() if sort_order == SortOrder.DESC else column.asc()

        result = await self.db.execute(
            select(Project)
            .join(Customer, Customer.id == Project.customer_id)
            .where(*conditions)
            .options(*project_load_options())
            # id sebagai pembeda terakhir supaya urutan antar halaman stabil
            .order_by(ordering, Project.id.asc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )

        return list(result.unique().scalars().all()), total

    async def get_project(self, project_id: UUID) -> Project | None:
        # populate_existing: setelah update, objek yang sudah ada di session ikut disegarkan
        result = await self.db.execute(
            select(Project)
            .where(Project.id == project_id)
            .options(*project_load_options())
            .execution_options(populate_existing=True)
        )
        return result.unique().scalar_one_or_none()

    async def get_project_by_code(self, project_code: str) -> Project | None:
        result = await self.db.execute(
            select(Project).where(func.lower(Project.project_code) == project_code.lower())
        )
        return result.scalar_one_or_none()

    # --------------------------------------------------------------- dashboard
    async def summary_totals(self) -> dict:
        is_active = ProjectStatus.project_status_code == ACTIVE_PROJECT_STATUS_CODE
        profit = ProjectFinancial.revenue - ProjectFinancial.cogs - ProjectFinancial.operational_costs

        row = (
            await self.db.execute(
                select(
                    func.count(Project.id),
                    func.count(Project.id).filter(is_active),
                    func.coalesce(func.sum(Project.value_before_tax), 0),
                    func.coalesce(func.sum(Project.value_before_tax).filter(is_active), 0),
                    func.coalesce(func.sum(profit), 0),
                    func.coalesce(func.sum(profit).filter(is_active), 0),
                )
                .select_from(Project)
                .join(ProjectStatus, ProjectStatus.id == Project.project_status_id)
                .outerjoin(ProjectFinancial, ProjectFinancial.project_id == Project.id)
            )
        ).one()

        customers = (await self.db.execute(select(func.count(Customer.id)))).scalar_one()

        return {
            "customers": customers,
            "projects": row[0],
            "active_projects": row[1],
            "total_value_before_tax": Decimal(row[2]),
            "active_value_before_tax": Decimal(row[3]),
            "total_net_profit": Decimal(row[4]),
            "active_net_profit": Decimal(row[5]),
        }

    async def _group(self, master, prefix: str, link_condition, *, include_empty: bool, via_customer: bool):
        """Jumlah project dan total nilainya per baris master data."""
        count_project = func.count(Project.id)
        sum_value = func.coalesce(func.sum(Project.value_before_tax), 0)

        statement = select(
            master.id,
            getattr(master, f"{prefix}_code"),
            getattr(master, f"{prefix}_name"),
            count_project,
            sum_value,
        ).select_from(master)

        if via_customer:
            join_customer = Customer.__table__.c[link_condition]
            join_on = join_customer == master.id
            if include_empty:
                statement = statement.outerjoin(Customer, join_on).outerjoin(
                    Project, Project.customer_id == Customer.id
                )
            else:
                statement = statement.join(Customer, join_on).join(
                    Project, Project.customer_id == Customer.id
                )
        else:
            join_on = Project.__table__.c[link_condition] == master.id
            statement = statement.outerjoin(Project, join_on) if include_empty else statement.join(Project, join_on)

        statement = statement.where(master.is_active.is_(True)).group_by(
            master.id,
            getattr(master, f"{prefix}_code"),
            getattr(master, f"{prefix}_name"),
            master.sort_order,
        )

        if not include_empty:
            statement = statement.having(count_project > 0)

        rows = (await self.db.execute(statement.order_by(master.sort_order))).all()

        return [
            {
                "id": row[0],
                "code": row[1],
                "name": row[2],
                "project_count": row[3],
                "value_before_tax": Decimal(row[4]),
            }
            for row in rows
        ]

    async def group_by_status(self):
        return await self._group(
            ProjectStatus, "project_status", "project_status_id", include_empty=True, via_customer=False
        )

    async def group_by_business_unit(self):
        return await self._group(
            BusinessUnit, "business_unit", "business_unit_id", include_empty=True, via_customer=False
        )

    async def group_by_industry(self):
        return await self._group(
            Industry, "industry", "industry_id", include_empty=False, via_customer=True
        )

    async def group_by_company_size(self):
        return await self._group(
            CompanySize, "company_size", "company_size_id", include_empty=False, via_customer=True
        )

    async def group_by_year(self) -> list[dict]:
        rows = (
            await self.db.execute(
                select(
                    Project.project_year,
                    func.count(Project.id),
                    func.coalesce(func.sum(Project.value_before_tax), 0),
                )
                .group_by(Project.project_year)
                .order_by(Project.project_year)
            )
        ).all()

        return [
            {"year": row[0], "project_count": row[1], "value_before_tax": Decimal(row[2])}
            for row in rows
        ]

    async def group_by_product(self) -> list[dict]:
        used = func.count(distinct(ProjectProduct.project_id))
        rows = (
            await self.db.execute(
                select(Product.id, Product.product_name, used)
                .join(ProjectProduct, ProjectProduct.product_id == Product.id)
                .group_by(Product.id, Product.product_name)
                .order_by(used.desc(), func.lower(Product.product_name))
            )
        ).all()

        return [{"id": row[0], "name": row[1], "project_count": row[2]} for row in rows]

    async def ending_soon(self, today: date) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .join(ProjectStatus, ProjectStatus.id == Project.project_status_id)
            .where(
                ProjectStatus.project_status_code == ACTIVE_PROJECT_STATUS_CODE,
                Project.end_date <= today + timedelta(days=ENDING_SOON_DAYS),
            )
            .options(*project_load_options())
            .order_by(Project.end_date.asc(), Project.id.asc())
            .limit(ENDING_SOON_LIMIT)
        )
        return list(result.unique().scalars().all())

    # ------------------------------------------------------------------ writes
    def add(self, item) -> None:
        self.db.add(item)

    async def delete(self, item) -> None:
        await self.db.delete(item)

    async def flush(self) -> None:
        await self.db.flush()

    async def save(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()
