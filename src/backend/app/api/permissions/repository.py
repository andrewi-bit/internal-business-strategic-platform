from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission_model import Permission

class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Permission).order_by(Permission.code.asc())
        )
        return result.scalars().all()

    async def get_by_id(self, permission_id: UUID):
        result = await self.db.execute(
            select(Permission).where(Permission.id == permission_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str):
        result = await self.db.execute(
            select(Permission).where(Permission.code == code)
        )
        return result.scalar_one_or_none()

    async def create(self, permission: Permission):
        self.db.add(permission)
        await self.db.flush()
        return permission

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
