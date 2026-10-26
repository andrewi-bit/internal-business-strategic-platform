from uuid import UUID

from app.api.portfolios.calculations import ACTIVE_PROJECT_STATUS_CODE
from app.api.portfolios.repository import like_pattern
from app.models.customer_model import Customer
from app.models.project_model import Project
from app.models.project_status_model import ProjectStatus
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


def customer_load_options():
    return (
        joinedload(Customer.company_size),
        joinedload(Customer.customer_type),
        joinedload(Customer.industry),
        joinedload(Customer.legal_structure),
    )


class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_customers(
        self,
        *,
        search: str | None,
        industry_id: UUID | None,
        company_size_id: UUID | None,
        customer_type_id: UUID | None,
        page: int,
        page_size: int,
    ) -> tuple[list[tuple[Customer, int, int]], int]:
        conditions = []

        if search and search.strip():
            conditions.append(Customer.customer_name.ilike(like_pattern(search), escape="\\"))
        if industry_id is not None:
            conditions.append(Customer.industry_id == industry_id)
        if company_size_id is not None:
            conditions.append(Customer.company_size_id == company_size_id)
        if customer_type_id is not None:
            conditions.append(Customer.customer_type_id == customer_type_id)

        total = (
            await self.db.execute(select(func.count(Customer.id)).where(*conditions))
        ).scalar_one()

        project_count = (
            select(func.count(Project.id))
            .where(Project.customer_id == Customer.id)
            .correlate(Customer)
            .scalar_subquery()
        )
        active_count = (
            select(func.count(Project.id))
            .join(ProjectStatus, ProjectStatus.id == Project.project_status_id)
            .where(
                Project.customer_id == Customer.id,
                ProjectStatus.project_status_code == ACTIVE_PROJECT_STATUS_CODE,
            )
            .correlate(Customer)
            .scalar_subquery()
        )

        rows = (
            await self.db.execute(
                select(Customer, project_count, active_count)
                .where(*conditions)
                .options(*customer_load_options())
                .order_by(func.lower(Customer.customer_name), Customer.id)
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
        ).unique().all()

        return [(row[0], row[1], row[2]) for row in rows], total

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        result = await self.db.execute(
            select(Customer)
            .where(Customer.id == customer_id)
            .options(*customer_load_options())
            .execution_options(populate_existing=True)
        )
        return result.unique().scalar_one_or_none()

    async def get_by_name(self, name: str) -> Customer | None:
        result = await self.db.execute(
            select(Customer).where(func.lower(Customer.customer_name) == name.strip().lower())
        )
        return result.scalar_one_or_none()

    async def counts(self, customer_id: UUID) -> tuple[int, int]:
        row = (
            await self.db.execute(
                select(
                    func.count(Project.id),
                    func.count(Project.id).filter(
                        ProjectStatus.project_status_code == ACTIVE_PROJECT_STATUS_CODE
                    ),
                )
                .select_from(Project)
                .join(ProjectStatus, ProjectStatus.id == Project.project_status_id)
                .where(Project.customer_id == customer_id)
            )
        ).one()
        return row[0], row[1]

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
