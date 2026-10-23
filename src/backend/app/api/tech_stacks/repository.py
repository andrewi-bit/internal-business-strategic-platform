from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_stack_model import TechStack

class TechStackRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        tech_stack_category: str | None = None,
        include_inactive: bool = False,
    ):
        query = select(TechStack)

        if tech_stack_category is not None:
            query = query.where(TechStack.tech_stack_category == tech_stack_category)

        if not include_inactive:
            query = query.where(TechStack.is_active.is_(True))

        result = await self.db.execute(
            query.order_by(
                TechStack.tech_stack_category.asc(),
                TechStack.tech_stack_name.asc(),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, tech_stack_id: UUID):
        result = await self.db.execute(
            select(TechStack).where(TechStack.id == tech_stack_id)
        )
        return result.scalar_one_or_none()

    async def get_by_category_and_name(self, tech_stack_category: str, name: str):
        result = await self.db.execute(
            select(TechStack).where(
                TechStack.tech_stack_category == tech_stack_category,
                func.lower(TechStack.tech_stack_name) == name.lower(),
            )
        )
        return result.scalar_one_or_none()

    async def create(self, tech_stack: TechStack):
        self.db.add(tech_stack)
        await self.db.flush()
        return tech_stack

    async def try_delete(self, tech_stack: TechStack) -> bool:
        # False jika database menolak karena tech stack masih dipakai project.
        try:
            async with self.db.begin_nested():
                await self.db.delete(tech_stack)
                await self.db.flush()
        except IntegrityError:
            return False

        return True

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
