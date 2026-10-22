
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.api.auth.permissions import require_permission
from app.api.role_requests.schema import (
    RoleRequestCreate,
    RoleRequestResponse,
    RoleRequestReview,
)
from app.api.role_requests.usecase import RoleRequestUseCase
from app.connections.session import get_db
from app.models.user_model import User

router = APIRouter(
    prefix="/role-requests",
    tags=["Role Requests"],
)

def success_response(message: str, data):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": None,
    }

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role_request(
    payload: RoleRequestCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    request = await RoleRequestUseCase(db).create(current_user, payload)

    return success_response(
        "Pengajuan role berhasil dibuat.",
        RoleRequestResponse.model_validate(request).model_dump(mode="json"),
    )

@router.get("/me")
async def get_my_role_requests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    request = await RoleRequestUseCase(db).get_my_request(current_user)

    data = (
        RoleRequestResponse.model_validate(request).model_dump(mode="json")
        if request is not None
        else None
    )

    return success_response(
        "Data pengajuan role berhasil diambil.",
        data,
    )

@router.get("")
async def get_all_role_requests(
    current_user: User = Depends(
        require_permission("role_request.review")
    ),
    db: AsyncSession = Depends(get_db),
):
    requests = await RoleRequestUseCase(db).get_all_requests()

    data = [
        RoleRequestResponse.model_validate(item).model_dump(mode="json")
        for item in requests
    ]

    return success_response("Daftar pengajuan role berhasil diambil.", data)

@router.patch("/{request_id}/review")
async def review_role_request(
    request_id: UUID,
    payload: RoleRequestReview,
    current_user: User = Depends(
        require_permission("role_request.review")
    ),
    db: AsyncSession = Depends(get_db),
):
    request = await RoleRequestUseCase(db).review(
        request_id,
        current_user,
        payload,
    )

    return success_response(
        "Pengajuan role berhasil direview.",
        RoleRequestResponse.model_validate(request).model_dump(mode="json"),
    )
