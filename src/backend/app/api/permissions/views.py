
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.permissions.repository import PermissionRepository
from app.api.permissions.schema import (
    PermissionCreateRequest,
    PermissionUpdateRequest,
)
from app.api.permissions.usecase import PermissionUseCase
from app.connections.session import get_db
from app.models.user_model import User

router = APIRouter(prefix="/permissions", tags=["Permissions"])

def get_permission_use_case(
    db: AsyncSession = Depends(get_db),
) -> PermissionUseCase:
    return PermissionUseCase(PermissionRepository(db))

@router.get("")
async def get_permissions(
    _: User = Depends(require_permission("role.manage")),
    use_case: PermissionUseCase = Depends(get_permission_use_case),
):
    permissions = await use_case.list_permissions()

    return {
        "success": True,
        "message": "Data permission berhasil diambil.",
        "data": [
            {
                "id": str(permission.id),
                "code": permission.code,
                "name": permission.name,
                "description": permission.description,
            }
            for permission in permissions
        ],
        "meta": None,
    }

@router.post("")
async def create_permission(
    payload: PermissionCreateRequest,
    _: User = Depends(require_permission("role.manage")),
    use_case: PermissionUseCase = Depends(get_permission_use_case),
):
    permission = await use_case.create_permission(payload)

    return {
        "success": True,
        "message": "Permission berhasil dibuat.",
        "data": {
            "id": str(permission.id),
            "code": permission.code,
            "name": permission.name,
            "description": permission.description,
        },
        "meta": None,
    }

@router.patch("/{permission_id}")
async def update_permission(
    permission_id: UUID,
    payload: PermissionUpdateRequest,
    _: User = Depends(require_permission("role.manage")),
    use_case: PermissionUseCase = Depends(get_permission_use_case),
):
    permission = await use_case.update_permission(
        permission_id,
        payload,
    )

    return {
        "success": True,
        "message": "Permission berhasil diperbarui.",
        "data": {
            "id": str(permission.id),
            "code": permission.code,
            "name": permission.name,
            "description": permission.description,
        },
        "meta": None,
    }
