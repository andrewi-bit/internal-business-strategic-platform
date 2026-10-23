from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.permissions.repository import PermissionRepository
from app.api.permissions.schema import (
    PermissionCreateRequest,
    PermissionUpdateRequest,
)
from app.models.permission_model import Permission

class PermissionUseCase:
    def __init__(self, repository: PermissionRepository):
        self.repository = repository

    async def list_permissions(self):
        return await self.repository.get_all()

    async def create_permission(self, payload: PermissionCreateRequest):
        if await self.repository.get_by_code(payload.code):
            raise HTTPException(
                status_code=409,
                detail="Code permission sudah digunakan.",
            )

        permission = Permission(
            code=payload.code,
            name=payload.name,
            description=payload.description,
        )

        try:
            await self.repository.create(permission)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(
                status_code=409,
                detail="Code permission sudah digunakan.",
            )

        return permission

    async def update_permission(
        self,
        permission_id: UUID,
        payload: PermissionUpdateRequest,
    ):
        permission = await self.repository.get_by_id(permission_id)

        if permission is None:
            raise HTTPException(
                status_code=404,
                detail="Permission tidak ditemukan.",
            )

        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(
                status_code=400,
                detail="Tidak ada data yang diperbarui.",
            )

        for field, value in changes.items():
            setattr(permission, field, value)

        await self.repository.save()
        return permission
