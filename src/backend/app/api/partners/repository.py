from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.partner_model import Partner

class PartnerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, search: str | None = None, include_inactive: bool = False):
        query = select(Partner)

        if search:
            term = f"%{search.strip()}%"
            query = query.where(Partner.partner_name.ilike(term))

        if not include_inactive:
            query = query.where(Partner.is_active.is_(True))

        result = await self.db.execute(query.order_by(Partner.partner_name.asc()))
        return result.scalars().all()

    async def get_by_id(self, partner_id: UUID):
        result = await self.db.execute(
            select(Partner).where(Partner.id == partner_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, partner_name: str):
        result = await self.db.execute(
            select(Partner).where(
                func.lower(Partner.partner_name) == partner_name.lower()
            )
        )
        return result.scalar_one_or_none()

    async def create(self, partner: Partner):
        self.db.add(partner)
        await self.db.flush()
        return partner

    async def try_delete(self, partner: Partner) -> bool:
        # False jika database menolak karena partner masih dipakai project.
        try:
            async with self.db.begin_nested():
                await self.db.delete(partner)
                await self.db.flush()
        except IntegrityError:
            return False

        return True

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
