from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.email_otp_model import EmailOTP

async def create_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
    otp_hash: str,
    expires_at: datetime,
) -> EmailOTP:
    otp = EmailOTP(
        user_id=user_id,
        otp_hash=otp_hash,
        expires_at=expires_at,
    )
    db.add(otp)
    await db.flush()
    return otp

async def get_latest_valid_otp(
    db: AsyncSession,
    *,
    user_id: UUID,
) -> EmailOTP | None:
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(EmailOTP)
        .where(
            EmailOTP.user_id == user_id,
            EmailOTP.used_at.is_(None),
            EmailOTP.expires_at > now,
        )
        .order_by(EmailOTP.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()

async def invalidate_unused_otps(
    db: AsyncSession,
    *,
    user_id: UUID,
) -> None:
    await db.execute(
        update(EmailOTP)
        .where(
            EmailOTP.user_id == user_id,
            EmailOTP.used_at.is_(None),
        )
        .values(used_at=datetime.now(timezone.utc))
    )