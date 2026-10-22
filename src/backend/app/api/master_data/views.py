from typing import Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.master_data.schema import MasterDataType
from app.api.master_data.usecase import MasterDataUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User

router = APIRouter(prefix="/master-data", tags=["Master Data"])

CREATE_EXAMPLE = {
    "industries": {
        "summary": "Contoh untuk type industries",
        "value": {
            "industry_code": "AGRITECH",
            "industry_name": "Agritech",
            "industry_description": None,
            "sort_order": None,
        },
    }
}

UPDATE_EXAMPLE = {
    "industries": {
        "summary": "Contoh untuk type industries",
        "value": {"industry_name": "Agritech", "is_active": False},
    }
}

def get_master_data_use_case(
    data_type: MasterDataType,
    db: AsyncSession = Depends(get_db),
) -> MasterDataUseCase:
    return MasterDataUseCase(db, data_type)

@router.get("/{data_type}")
async def get_master_data(
    data_type: MasterDataType,
    include_inactive: bool = Query(default=False),
    current_user: User = Depends(require_permission("portfolio.view")),
    db: AsyncSession = Depends(get_db),
    use_case: MasterDataUseCase = Depends(get_master_data_use_case),
):
    if include_inactive:
        await require_permission("portfolio.manage")(current_user=current_user, db=db)

    data = await use_case.list_items(include_inactive)
    return success_response(
        message=f"Data {use_case.label} berhasil diambil.",
        data=data,
    )

@router.post("/{data_type}")
async def create_master_data(
    data_type: MasterDataType,
    payload: dict[str, Any] = Body(..., openapi_examples=CREATE_EXAMPLE),
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: MasterDataUseCase = Depends(get_master_data_use_case),
):
    data = await use_case.create_item(payload)
    return success_response(
        message=f"{use_case.label} berhasil ditambahkan.",
        data=data,
    )

@router.patch("/{data_type}/{item_id}")
async def update_master_data(
    data_type: MasterDataType,
    item_id: UUID,
    payload: dict[str, Any] = Body(..., openapi_examples=UPDATE_EXAMPLE),
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: MasterDataUseCase = Depends(get_master_data_use_case),
):
    data = await use_case.update_item(item_id, payload)
    return success_response(
        message=f"{use_case.label} berhasil diperbarui.",
        data=data,
    )

@router.delete("/{data_type}/{item_id}")
async def delete_master_data(
    data_type: MasterDataType,
    item_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: MasterDataUseCase = Depends(get_master_data_use_case),
):
    data, message = await use_case.delete_item(item_id)
    return success_response(message=message, data=data)
