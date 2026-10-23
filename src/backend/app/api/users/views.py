from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.users.schema import UserUpdateRequest
from app.api.users.usecase import UserManagementUseCase
from app.connections.session import get_db
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["User Management"])


def success_response(message: str, data, meta=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta,
    }


@router.get("")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, max_length=150),
    role_id: UUID | None = Query(None),
    is_active: bool | None = Query(None),
    admin: User = Depends(require_permission("user.manage")),
    db: AsyncSession = Depends(get_db),
):
    result = await UserManagementUseCase(db).list_users(
        page=page,
        page_size=page_size,
        search=search,
        role_id=role_id,
        is_active=is_active,
    )

    return success_response(
        "Daftar user berhasil diambil.",
        result["data"],
        result["meta"],
    )

@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    admin: User = Depends(require_permission("user.manage")),
    db: AsyncSession = Depends(get_db),
):
    data = await UserManagementUseCase(db).get_user(user_id)
    return success_response("Detail user berhasil diambil.", data)

@router.patch("/{user_id}")
async def update_user(
    user_id: UUID,
    payload: UserUpdateRequest,
    admin: User = Depends(require_permission("user.manage")),
    db: AsyncSession = Depends(get_db),
):
    data = await UserManagementUseCase(db).update_user(
        user_id=user_id,
        admin=admin,
        payload=payload,
    )
    return success_response("User berhasil diperbarui.", data)
