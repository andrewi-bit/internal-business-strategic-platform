from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.api.auth.permissions import require_permission
from app.api.roles.repository import RoleRepository
from app.api.roles.schema import (
    RoleCreateRequest,
    RolePermissionsUpdateRequest,
    RoleUpdateRequest,
)
from app.api.roles.usecase import RoleUseCase
from app.connections.session import get_db
from app.models.permission_model import Permission
from app.models.role_permission_model import RolePermission
from app.models.user_model import User
from sqlalchemy import select
from fastapi import HTTPException

router = APIRouter(prefix="/roles", tags=["Roles"])

def get_role_use_case(
    db: AsyncSession = Depends(get_db),
) -> RoleUseCase:
    return RoleUseCase(RoleRepository(db))

async def ensure_role_manager(
    current_user: User,
    db: AsyncSession,
) -> None:
    if current_user.role_id is None:
        raise HTTPException(
            status_code=403,
            detail="Anda tidak memiliki izin untuk melakukan tindakan ini.",
        )

    result = await db.execute(
        select(Permission.id)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id,
        )
        .where(
            RolePermission.role_id == current_user.role_id,
            Permission.code == "role.manage",
        )
    )

    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=403,
            detail="Anda tidak memiliki izin untuk melakukan tindakan ini.",
        )

@router.get("")
async def get_all_roles(
    include_inactive: bool = Query(default=False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    use_case: RoleUseCase = Depends(get_role_use_case),
):
    if include_inactive:
        await ensure_role_manager(current_user, db)

    roles = await use_case.list_roles(include_inactive)

    return {
        "success": True,
        "message": "Data role berhasil diambil.",
        "data": [
            {
                "id": str(role.id),
                "name": role.name,
                "code": role.code,
                "description": role.description,
                "is_active": role.is_active,
            }
            for role in roles
        ],
        "meta": None,
    }

@router.post("")
async def create_role(
    payload: RoleCreateRequest,
    _: User = Depends(require_permission("role.manage")),
    use_case: RoleUseCase = Depends(get_role_use_case),
):
    data = await use_case.create_role(payload)
    return {
        "success": True,
        "message": "Role berhasil dibuat.",
        "data": data,
        "meta": None,
    }

@router.get("/{role_id}")
async def get_role_detail(
    role_id: UUID,
    _: User = Depends(require_permission("role.manage")),
    use_case: RoleUseCase = Depends(get_role_use_case),
):
    data = await use_case.get_role_detail(role_id)
    return {
        "success": True,
        "message": "Detail role berhasil diambil.",
        "data": data,
        "meta": None,
    }

@router.patch("/{role_id}")
async def update_role(
    role_id: UUID,
    payload: RoleUpdateRequest,
    _: User = Depends(require_permission("role.manage")),
    use_case: RoleUseCase = Depends(get_role_use_case),
):
    data = await use_case.update_role(role_id, payload)
    return {
        "success": True,
        "message": "Role berhasil diperbarui.",
        "data": data,
        "meta": None,
    }

@router.put("/{role_id}/permissions")
async def set_role_permissions(
    role_id: UUID,
    payload: RolePermissionsUpdateRequest,
    _: User = Depends(require_permission("role.manage")),
    use_case: RoleUseCase = Depends(get_role_use_case),
):
    data = await use_case.set_role_permissions(
        role_id,
        payload.permission_ids,
    )
    return {
        "success": True,
        "message": "Permission role berhasil diperbarui.",
        "data": data,
        "meta": None,
    }
