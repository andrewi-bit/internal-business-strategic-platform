from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

class MasterDataRepository:
    def __init__(self, db: AsyncSession, model, prefix: str):
        self.db = db
        self.model = model
        self.code_column = getattr(model, f"{prefix}_code")
        self.name_column = getattr(model, f"{prefix}_name")

    async def get_all(self, include_inactive: bool = False):
        query = select(self.model)

        if not include_inactive:
            query = query.where(self.model.is_active.is_(True))

        result = await self.db.execute(
            query.order_by(self.model.sort_order.asc(), self.name_column.asc())
        )
        return result.scalars().all()

    async def get_by_id(self, item_id: UUID):
        result = await self.db.execute(
            select(self.model).where(self.model.id == item_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str):
        result = await self.db.execute(
            select(self.model).where(self.code_column == code)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str):
        result = await self.db.execute(
            select(self.model).where(func.lower(self.name_column) == name.lower())
        )
        return result.scalar_one_or_none()

    async def get_next_sort_order(self) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(self.model.sort_order), 0))
        )
        return result.scalar_one() + 1

    async def create(self, item):
        self.db.add(item)
        await self.db.flush()
        return item

    async def try_delete(self, item) -> bool:
        # False jika database menolak karena data masih dipakai (ON DELETE RESTRICT).
        try:
            async with self.db.begin_nested():
                await self.db.delete(item)
                await self.db.flush()
        except IntegrityError:
            return False

        return True

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
