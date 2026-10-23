from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.connections.session import get_db
from app.models.permission_model import Permission
from app.models.role_permission_model import RolePermission
from app.models.user_model import User

def require_permission(permission_code: str):
    async def check_permission(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        if current_user.role_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak memiliki izin untuk melakukan tindakan ini.",
            )

        query = (
            select(Permission.id)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .where(
                RolePermission.role_id == current_user.role_id,
                Permission.code == permission_code,
            )
        )

        result = await db.execute(query)

        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak memiliki izin untuk melakukan tindakan ini.",
            )

        return current_user

    return check_permission