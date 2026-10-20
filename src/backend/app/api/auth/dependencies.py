from uuid import UUID

import jwt
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.connections.redis import get_redis
from app.api.auth import repository
from app.connections.session import get_db
from app.core.security import decode_access_token
from app.models.user_model import User

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    is_revoked = await redis.exists(f"revoked_access_token:{token_hash}")

    if is_revoked:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        token_version = payload.get("ver")

        if (
            not subject
            or isinstance(token_version, bool)
            or not isinstance(token_version, int)
            or token_version < 0
        ):
            raise credentials_exception

        user_id = UUID(subject)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user = await repository.get_user_by_id(db, user_id)

    if (
        user is None
        or not user.is_active
        or user.email_verified_at is None
        or token_version != user.token_version
    ):
        raise credentials_exception

    return user