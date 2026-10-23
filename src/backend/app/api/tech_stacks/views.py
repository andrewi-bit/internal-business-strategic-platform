from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.tech_stacks.repository import TechStackRepository
from app.api.tech_stacks.schema import (
    TechStackCategory,
    TechStackCreateRequest,
    TechStackUpdateRequest,
)
from app.api.tech_stacks.usecase import TechStackUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User

router = APIRouter(prefix="/tech-stacks", tags=["Tech Stacks"])

def get_tech_stack_use_case(
    db: AsyncSession = Depends(get_db),
) -> TechStackUseCase:
    return TechStackUseCase(TechStackRepository(db))

@router.get("")
async def get_tech_stacks(
    tech_stack_category: TechStackCategory | None = Query(default=None),
    include_inactive: bool = Query(default=False),
    current_user: User = Depends(require_permission("portfolio.view")),
    db: AsyncSession = Depends(get_db),
    use_case: TechStackUseCase = Depends(get_tech_stack_use_case),
):
    if include_inactive:
        await require_permission("portfolio.manage")(current_user=current_user, db=db)

    data = await use_case.list_tech_stacks(tech_stack_category, include_inactive)
    return success_response(message="Data tech stack berhasil diambil.", data=data)

@router.post("")
async def create_tech_stack(
    payload: TechStackCreateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: TechStackUseCase = Depends(get_tech_stack_use_case),
):
    data = await use_case.create_tech_stack(payload)
    return success_response(message="Tech stack berhasil ditambahkan.", data=data)

@router.patch("/{tech_stack_id}")
async def update_tech_stack(
    tech_stack_id: UUID,
    payload: TechStackUpdateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: TechStackUseCase = Depends(get_tech_stack_use_case),
):
    data = await use_case.update_tech_stack(tech_stack_id, payload)
    return success_response(message="Tech stack berhasil diperbarui.", data=data)

@router.delete("/{tech_stack_id}")
async def delete_tech_stack(
    tech_stack_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: TechStackUseCase = Depends(get_tech_stack_use_case),
):
    data, message = await use_case.delete_tech_stack(tech_stack_id)
    return success_response(message=message, data=data)
