from math import ceil
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.repository import UserManagementRepository
from app.api.users.schema import UserUpdateRequest
from app.models.user_model import User

class UserManagementUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = UserManagementRepository(db)

    @staticmethod
    def serialize(row):
        user, role_name = row
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role_id": user.role_id,
            "role_name": role_name,
            "is_active": user.is_active,
            "email_verified_at": user.email_verified_at,
            "last_login_at": user.last_login_at,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    async def list_users(
        self,
        page: int,
        page_size: int,
        search: str | None,
        role_id: UUID | None,
        is_active: bool | None,
    ):
        rows, total = await self.repository.list_users(
            page, page_size, search, role_id, is_active
        )

        return {
            "data": [self.serialize(row) for row in rows],
            "meta": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": ceil(total / page_size) if total else 0,
            },
        }

    async def get_user(self, user_id: UUID):
        row = await self.repository.get_user(user_id)

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan.",
            )

        return self.serialize(row)

    async def update_user(
        self,
        user_id: UUID,
        admin: User,
        payload: UserUpdateRequest,
    ):
        user = await self.db.get(User, user_id)

        if user is None or user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan.",
            )

        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tidak ada field yang diperbarui.",
            )

        if "full_name" in changes:
            if changes["full_name"] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nama lengkap tidak boleh null.",
                )
            user.full_name = changes["full_name"]

        if "role_id" in changes:
            new_role_id = changes["role_id"]

            if new_role_id is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Role tidak boleh null.",
                )

            if user.id == admin.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Anda tidak dapat mengubah role akun sendiri.",
                )

            role = await self.repository.get_active_role(new_role_id)
            if role is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role tidak ditemukan atau tidak aktif.",
                )

            user.role_id = role.id

        if "is_active" in changes:
            new_status = changes["is_active"]

            if new_status is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Status akun tidak boleh null.",
                )

            if user.id == admin.id and not new_status:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Anda tidak dapat menonaktifkan akun sendiri.",
                )

            user.is_active = new_status

        user.updated_by = admin.id

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return await self.get_user(user.id)
