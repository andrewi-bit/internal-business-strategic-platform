from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.connections.session import get_db
from app.models.role_model import Role
from app.models.user_model import User

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("")
async def get_all_roles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Role)
        .where(Role.is_active.is_(True))
        .order_by(Role.name.asc())
    )
    roles = result.scalars().all()

    return {
        "success": True,
        "message": "Data role berhasil diambil.",
        "data": [
            {
                "id": str(role.id),
                "name": role.name,
                "code": role.code,
                "description": role.description,
            }
            for role in roles
        ],
        "meta": None,
    }