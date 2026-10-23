from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.tech_stacks.repository import TechStackRepository
from app.api.tech_stacks.schema import (
    TechStackCategory,
    TechStackCreateRequest,
    TechStackUpdateRequest,
)
from app.models.tech_stack_model import TechStack

DUPLICATE_MESSAGE = "Nama tech stack sudah digunakan di kategori ini."

def serialize_tech_stack(tech_stack: TechStack):
    return {
        "id": tech_stack.id,
        "tech_stack_category": tech_stack.tech_stack_category,
        "tech_stack_name": tech_stack.tech_stack_name,
        "is_active": tech_stack.is_active,
    }

class TechStackUseCase:
    def __init__(self, repository: TechStackRepository):
        self.repository = repository

    async def _get_or_404(self, tech_stack_id: UUID) -> TechStack:
        tech_stack = await self.repository.get_by_id(tech_stack_id)

        if tech_stack is None:
            raise HTTPException(404, "Tech stack tidak ditemukan.")

        return tech_stack

    async def _ensure_unique(
        self,
        tech_stack_category: str,
        name: str,
        exclude_id: UUID | None = None,
    ):
        existing = await self.repository.get_by_category_and_name(
            tech_stack_category,
            name,
        )

        if existing is not None and existing.id != exclude_id:
            raise HTTPException(409, DUPLICATE_MESSAGE)

    async def list_tech_stacks(
        self,
        tech_stack_category: TechStackCategory | None = None,
        include_inactive: bool = False,
    ):
        category = tech_stack_category.value if tech_stack_category else None
        tech_stacks = await self.repository.get_all(category, include_inactive)
        return [serialize_tech_stack(tech_stack) for tech_stack in tech_stacks]

    async def create_tech_stack(self, payload: TechStackCreateRequest):
        category = payload.tech_stack_category.value
        await self._ensure_unique(category, payload.tech_stack_name)

        tech_stack = TechStack(
            tech_stack_category=category,
            tech_stack_name=payload.tech_stack_name,
            is_active=True,
        )

        try:
            await self.repository.create(tech_stack)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, DUPLICATE_MESSAGE)

        return serialize_tech_stack(tech_stack)

    async def update_tech_stack(
        self,
        tech_stack_id: UUID,
        payload: TechStackUpdateRequest,
    ):
        tech_stack = await self._get_or_404(tech_stack_id)
        changes = payload.model_dump(exclude_unset=True, mode="json")

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        if "tech_stack_category" in changes or "tech_stack_name" in changes:
            await self._ensure_unique(
                changes.get("tech_stack_category", tech_stack.tech_stack_category),
                changes.get("tech_stack_name", tech_stack.tech_stack_name),
                exclude_id=tech_stack.id,
            )

        for field, value in changes.items():
            setattr(tech_stack, field, value)

        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, DUPLICATE_MESSAGE)

        return serialize_tech_stack(tech_stack)

    async def delete_tech_stack(self, tech_stack_id: UUID):
        tech_stack = await self._get_or_404(tech_stack_id)

        if await self.repository.try_delete(tech_stack):
            await self.repository.save()
            return {"id": tech_stack_id, "deleted": True}, "Tech stack berhasil dihapus."

        tech_stack = await self._get_or_404(tech_stack_id)
        tech_stack.is_active = False
        await self.repository.save()

        return (
            {"id": tech_stack_id, "deleted": False, "is_active": False},
            "Tech stack masih dipakai project, jadi dinonaktifkan.",
        )
