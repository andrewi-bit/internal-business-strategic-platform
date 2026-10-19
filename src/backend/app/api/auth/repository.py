from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.models.token_model import RefreshToken

async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    result = await db.execute(
        select(User).where(
            func.lower(User.email) == email.strip().lower()
        )
    )
    return result.scalar_one_or_none()

async def get_user_by_google_id(
    db: AsyncSession,
    google_id: str,
) -> User | None:
    result = await db.execute(
        select(User).where(User.google_id == google_id)
    )
    return result.scalar_one_or_none()

async def link_google_id(
    db: AsyncSession,
    user: User,
    google_id: str,
) -> User:
    user.google_id = google_id
    await db.flush()
    return user

async def create_user(
    db: AsyncSession,
    *,
    email: str,
    full_name: str,
    password_hash: str,
) -> User:
    user = User(
        email=email.strip().lower(),
        full_name=full_name.strip(),
        password_hash=password_hash,
    )

    db.add(user)
    await db.flush()

    return user

async def get_user_by_id(
    db: AsyncSession,
    user_id: UUID,
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def mark_email_verified(
    db: AsyncSession,
    user: User,
) -> User:
    user.email_verified_at = datetime.now(timezone.utc)
    await db.flush()
    return user

async def create_refresh_token(
    db: AsyncSession,
    *,
    user_id: UUID,
    family_id: UUID,
    token_hash: str,
    expires_at: datetime,
) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        family_id=family_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    await db.flush()

    return refresh_token

async def get_refresh_token_by_hash(
    db: AsyncSession,
    token_hash: str,
    *,
    for_update: bool = False,
) -> RefreshToken | None:
    query = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash
    )

    if for_update:
        query = query.with_for_update()

    result = await db.execute(query)
    return result.scalar_one_or_none()

async def revoke_refresh_token(
    db: AsyncSession,
    refresh_token: RefreshToken,
    *,
    replaced_by_id: UUID | None = None,
) -> None:
    refresh_token.revoked_at = datetime.now(timezone.utc)
    refresh_token.replaced_by_id = replaced_by_id

    await db.flush()

async def revoke_refresh_token_family(
    db: AsyncSession,
    family_id: UUID,
) -> None:
    await db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.family_id == family_id,
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=datetime.now(timezone.utc))
    )