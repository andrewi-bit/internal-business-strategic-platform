from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import repository as auth_repository
from app.api.auth.schema import (
    ResendOTPRequest,
    ResendOTPResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from app.api.email_verification import repository as otp_repository
from app.api.email_verification.service_email import send_otp_email
from app.core.otp import (
    generate_otp,
    get_otp_expiry,
    hash_otp,
    verify_otp,
)

async def verify_user_email(
    db: AsyncSession,
    payload: VerifyEmailRequest,
) -> VerifyEmailResponse:
    email = str(payload.email).strip().lower()

    user = await auth_repository.get_user_by_email(db, email)

    if user is None:
        raise ValueError("Email atau OTP tidak valid")

    if user.email_verified_at is not None:
        raise ValueError("Email sudah terverifikasi")

    otp_record = await otp_repository.get_latest_valid_otp(
        db,
        user_id=user.id,
    )

    if otp_record is None:
        raise ValueError("OTP tidak valid atau sudah kedaluwarsa")

    if not verify_otp(payload.otp, otp_record.otp_hash):
        raise ValueError("OTP tidak valid atau sudah kedaluwarsa")

    try:
        await otp_repository.invalidate_unused_otps(
            db,
            user_id=user.id,
        )
        await auth_repository.mark_email_verified(db, user)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return VerifyEmailResponse(
        message="Email berhasil diverifikasi",
        email=user.email,
    )

async def resend_user_otp(
    db: AsyncSession,
    payload: ResendOTPRequest,
) -> ResendOTPResponse:
    email = str(payload.email).strip().lower()

    user = await auth_repository.get_user_by_email(db, email)

    if user is None:
        raise ValueError("Email tidak ditemukan")

    if user.email_verified_at is not None:
        raise ValueError("Email sudah terverifikasi")

    try:
        await otp_repository.invalidate_unused_otps(
            db,
            user_id=user.id,
        )

        otp = generate_otp()

        await otp_repository.create_otp(
            db,
            user_id=user.id,
            otp_hash=hash_otp(otp),
            expires_at=get_otp_expiry(),
        )

        send_otp_email(to_email=user.email, otp=otp)

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return ResendOTPResponse(
        message="OTP baru berhasil dikirim ke email",
        email=user.email,
    )

