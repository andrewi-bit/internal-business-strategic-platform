from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_model import Role
from app.models.user_model import User

class UserManagementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_users(
        self,
        page: int,
        page_size: int,
        search: str | None,
        role_id: UUID | None,
        is_active: bool | None,
    ):
        filters = [User.deleted_at.is_(None)]

        if search:
            term = f"%{search.strip()}%"
            filters.append(
                or_(
                    User.full_name.ilike(term),
                    User.email.ilike(term),
                )
            )

        if role_id is not None:
            filters.append(User.role_id == role_id)

        if is_active is not None:
            filters.append(User.is_active.is_(is_active))

        total_result = await self.db.execute(
            select(func.count(User.id)).where(*filters)
        )
        total = total_result.scalar_one()

        result = await self.db.execute(
            select(User, Role.name.label("role_name"))
            .outerjoin(Role, Role.id == User.role_id)
            .where(*filters)
            .order_by(User.created_at.desc(), User.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        return result.all(), total

    async def get_user(self, user_id: UUID):
        result = await self.db.execute(
            select(User, Role.name.label("role_name"))
            .outerjoin(Role, Role.id == User.role_id)
            .where(
                User.id == user_id,
                User.deleted_at.is_(None),
            )
        )
        return result.first()

    async def get_active_role(self, role_id: UUID):
        result = await self.db.execute(
            select(Role).where(
                Role.id == role_id,
                Role.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()