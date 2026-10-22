from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_request_model import RoleRequest
from app.models.role_model import Role
from app.models.division_model import Division
from app.models.user_model import User

class RoleRequestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, request_id: UUID) -> RoleRequest | None:
        result = await self.db.execute(
            select(RoleRequest).where(RoleRequest.id == request_id)
        )
        return result.scalar_one_or_none()

    async def get_pending_by_user(
        self, user_id: UUID
    ) -> RoleRequest | None:
        result = await self.db.execute(
            select(RoleRequest).where(
                RoleRequest.user_id == user_id,
                RoleRequest.status == "pending",
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: UUID) -> list[RoleRequest]:
        result = await self.db.execute(
            select(RoleRequest)
            .where(RoleRequest.user_id == user_id)
            .order_by(RoleRequest.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[RoleRequest]:
        result = await self.db.execute(
            select(RoleRequest).order_by(RoleRequest.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_active_role(self, role_id: UUID) -> Role | None:
        result = await self.db.execute(
            select(Role).where(
                Role.id == role_id,
                Role.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def get_active_division(
        self, division_id: UUID
    ) -> Division | None:
        result = await self.db.execute(
            select(Division).where(
                Division.id == division_id,
                Division.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def get_user(self, user_id: UUID) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, request: RoleRequest) -> RoleRequest:
        self.db.add(request)
        await self.db.flush()
        return request

    async def save(self) -> None:
        await self.db.flush()

    async def get_latest_by_user(self, user_id: UUID):
        result = await self.db.execute(
            select(
                RoleRequest,
                Division.name.label("division_name"),
                Role.name.label("role_name"),
            )
            .join(
                Division,
                Division.id == RoleRequest.division_id,
            )
            .join(
                Role,
                Role.id == RoleRequest.requested_role_id,
            )
            .where(RoleRequest.user_id == user_id)
            .order_by(
                RoleRequest.created_at.desc(),
                RoleRequest.id.desc(),
            )
            .limit(1)
        )

        row = result.first()
        if row is None:
            return None

        request, division_name, role_name = row
        return {
            "id": request.id,
            "user_id": request.user_id,
            "requested_role_id": request.requested_role_id,
            "division_id": request.division_id,
            "division_name": division_name,
            "role_name": role_name,
            "reason": request.reason,
            "status": request.status,
            "reviewed_by": request.reviewed_by,
            "reviewed_at": request.reviewed_at,
            "review_notes": request.review_notes,
            "created_at": request.created_at,
            "updated_at": request.updated_at,
        }
