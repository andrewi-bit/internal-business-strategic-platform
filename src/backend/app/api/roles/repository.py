from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission_model import Permission
from app.models.role_model import Role
from app.models.role_permission_model import RolePermission

class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, include_inactive: bool = False):
        query = select(Role)

        if not include_inactive:
            query = query.where(Role.is_active.is_(True))

        result = await self.db.execute(query.order_by(Role.name.asc()))
        return result.scalars().all()

    async def get_by_id(self, role_id: UUID):
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str):
        result = await self.db.execute(
            select(Role).where(Role.code == code)
        )
        return result.scalar_one_or_none()

    async def get_permissions(self, role_id: UUID):
        result = await self.db.execute(
            select(Permission)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .where(RolePermission.role_id == role_id)
            .order_by(Permission.code.asc())
        )
        return result.scalars().all()

    async def get_permissions_by_ids(self, permission_ids: list[UUID]):
        if not permission_ids:
            return []

        result = await self.db.execute(
            select(Permission).where(Permission.id.in_(permission_ids))
        )
        return result.scalars().all()

    async def create(self, role: Role):
        self.db.add(role)
        await self.db.flush()
        return role

    async def replace_permissions(
        self,
        role_id: UUID,
        permission_ids: list[UUID],
    ):
        result = await self.db.execute(
            select(RolePermission).where(RolePermission.role_id == role_id)
        )

        for relation in result.scalars().all():
            await self.db.delete(relation)

        for permission_id in permission_ids:
            self.db.add(
                RolePermission(
                    role_id=role_id,
                    permission_id=permission_id,
                )
            )

        await self.db.flush()

    async def save(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
