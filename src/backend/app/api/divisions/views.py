from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.api.divisions.usecase import list_active_divisions
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User

router = APIRouter(prefix="/divisions", tags=["Divisions"])

@router.get("")
async def get_divisions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    divisions = await list_active_divisions(db)

    return success_response(
        message="Daftar division berhasil diambil",
        data=[
            division.model_dump(mode="json")
            for division in divisions
        ],
    )