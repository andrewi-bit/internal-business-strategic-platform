from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.partners.repository import PartnerRepository
from app.api.partners.schema import PartnerCreateRequest, PartnerUpdateRequest
from app.api.partners.usecase import PartnerUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User

router = APIRouter(prefix="/partners", tags=["Partners"])

def get_partner_use_case(
    db: AsyncSession = Depends(get_db),
) -> PartnerUseCase:
    return PartnerUseCase(PartnerRepository(db))

@router.get("")
async def get_partners(
    search: str | None = Query(default=None, max_length=200),
    include_inactive: bool = Query(default=False),
    current_user: User = Depends(require_permission("portfolio.view")),
    db: AsyncSession = Depends(get_db),
    use_case: PartnerUseCase = Depends(get_partner_use_case),
):
    if include_inactive:
        await require_permission("portfolio.manage")(current_user=current_user, db=db)

    data = await use_case.list_partners(search, include_inactive)
    return success_response(message="Data partner berhasil diambil.", data=data)

@router.post("")
async def create_partner(
    payload: PartnerCreateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: PartnerUseCase = Depends(get_partner_use_case),
):
    data = await use_case.create_partner(payload)
    return success_response(message="Partner berhasil ditambahkan.", data=data)

@router.patch("/{partner_id}")
async def update_partner(
    partner_id: UUID,
    payload: PartnerUpdateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: PartnerUseCase = Depends(get_partner_use_case),
):
    data = await use_case.update_partner(partner_id, payload)
    return success_response(message="Partner berhasil diperbarui.", data=data)

@router.delete("/{partner_id}")
async def delete_partner(
    partner_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: PartnerUseCase = Depends(get_partner_use_case),
):
    data, message = await use_case.delete_partner(partner_id)
    return success_response(message=message, data=data)
