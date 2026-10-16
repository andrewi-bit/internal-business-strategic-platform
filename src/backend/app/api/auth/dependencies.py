from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import repository
from app.connections.session import get_db
from app.core.security import decode_access_token
from app.models.user_model import User

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if not subject:
            raise credentials_exception

        user_id = UUID(subject)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user = await repository.get_user_by_id(db, user_id)

    if user is None or not user.is_active or user.email_verified_at is None:
        raise credentials_exception

    return user
