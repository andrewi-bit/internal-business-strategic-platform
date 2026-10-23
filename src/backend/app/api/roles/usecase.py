from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.roles.repository import RoleRepository
from app.api.roles.schema import RoleCreateRequest, RoleUpdateRequest
from app.models.role_model import Role

class RoleUseCase:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    async def list_roles(self, include_inactive: bool = False):
        return await self.repository.get_all(include_inactive)

    async def get_role_detail(self, role_id: UUID):
        role = await self.repository.get_by_id(role_id)

        if role is None:
            raise HTTPException(404, "Role tidak ditemukan.")

        permissions = await self.repository.get_permissions(role_id)

        return {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "is_active": role.is_active,
            "permissions": [
                {
                    "id": permission.id,
                    "code": permission.code,
                    "name": permission.name,
                    "description": permission.description,
                }
                for permission in permissions
            ],
        }

    async def create_role(self, payload: RoleCreateRequest):
        if await self.repository.get_by_code(payload.code):
            raise HTTPException(409, "Code role sudah digunakan.")

        role = Role(
            name=payload.name,
            code=payload.code,
            description=payload.description,
            is_active=True,
        )

        try:
            await self.repository.create(role)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Code role sudah digunakan.")

        return await self.get_role_detail(role.id)

    async def update_role(self, role_id: UUID, payload: RoleUpdateRequest):
        role = await self.repository.get_by_id(role_id)

        if role is None:
            raise HTTPException(404, "Role tidak ditemukan.")

        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        if role.code == "SUPER_ADMIN" and changes.get("is_active") is False:
            raise HTTPException(400, "Role SUPER_ADMIN tidak boleh dinonaktifkan.")

        for field, value in changes.items():
            setattr(role, field, value)

        await self.repository.save()
        return await self.get_role_detail(role_id)

    async def set_role_permissions(
        self,
        role_id: UUID,
        permission_ids: list[UUID],
    ):
        role = await self.repository.get_by_id(role_id)

        if role is None:
            raise HTTPException(404, "Role tidak ditemukan.")

        if len(permission_ids) != len(set(permission_ids)):
            raise HTTPException(422, "Permission ID tidak boleh duplikat.")

        permissions = await self.repository.get_permissions_by_ids(permission_ids)

        if len(permissions) != len(permission_ids):
            raise HTTPException(422, "Satu atau lebih permission tidak ditemukan.")

        try:
            await self.repository.replace_permissions(role_id, permission_ids)
            await self.repository.save()
        except Exception:
            await self.repository.rollback()
            raise

        return await self.get_role_detail(role_id)
