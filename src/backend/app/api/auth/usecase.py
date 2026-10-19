from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.models.user_model import User

from app.api.auth import repository
from app.api.auth.schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.api.email_verification import repository as otp_repository
from app.api.email_verification.service_email import send_otp_email
from app.core.otp import generate_otp, hash_otp, get_otp_expiry
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token,  hash_refresh_token

from app.settings import settings

async def register_user(
    db: AsyncSession,
    payload: RegisterRequest,
) -> RegisterResponse:
    email = str(payload.email).strip().lower()

    existing_user = await repository.get_user_by_email(db, email)
    if existing_user is not None:
        raise ValueError("Email sudah terdaftar")

    try:
        user = await repository.create_user(
            db,
            email=email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
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

    return RegisterResponse(
        message="Registrasi berhasil. Silakan cek email untuk kode OTP.",
        email=user.email,
    )

async def login_user(
    db: AsyncSession,
    payload: LoginRequest,
) -> tuple[LoginResponse, str]:
    email = str(payload.email).strip().lower()
    user = await repository.get_user_by_email(db, email)

    if user is None or user.password_hash is None:
        raise ValueError("Email atau password salah")

    if not verify_password(payload.password, user.password_hash):
        raise ValueError("Email atau password salah")

    if not user.is_active:
        raise PermissionError("Akun tidak aktif")

    if user.email_verified_at is None:
        raise PermissionError("Email belum diverifikasi")

    now = datetime.now(timezone.utc)
    raw_refresh_token = create_refresh_token()

    try:
        user.last_login_at = now

        await repository.create_refresh_token(
            db,
            user_id=user.id,
            family_id=uuid4(),
            token_hash=hash_refresh_token(raw_refresh_token),
            expires_at=now + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    response = LoginResponse(
        access_token=create_access_token(str(user.id)),
        token_type="bearer",
    )

    return response, raw_refresh_token

async def refresh_access_token(
    db: AsyncSession,
    raw_token: str,
) -> tuple[LoginResponse, str]:
    now = datetime.now(timezone.utc)

    token = await repository.get_refresh_token_by_hash(
        db,
        hash_refresh_token(raw_token),
        for_update=True,
    )

    if token is None:
        raise ValueError("Refresh token tidak valid")

    # Token lama digunakan kembali setelah dirotasi.
    # Cabut seluruh token aktif dalam keluarga tersebut.
    if token.revoked_at is not None:
        try:
            await repository.revoke_refresh_token_family(
                db,
                token.family_id,
            )
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        raise ValueError("Refresh token sudah tidak berlaku")

    if token.expires_at <= now:
        try:
            await repository.revoke_refresh_token(db, token)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        raise ValueError("Refresh token sudah kedaluwarsa")

    user = await repository.get_user_by_id(db, token.user_id)

    if (
        user is None
        or not user.is_active
        or user.email_verified_at is None
    ):
        try:
            await repository.revoke_refresh_token_family(
                db,
                token.family_id,
            )
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        raise PermissionError("Akun tidak dapat melakukan autentikasi")

    new_raw_token = create_refresh_token()

    try:
        new_token = await repository.create_refresh_token(
            db,
            user_id=token.user_id,
            family_id=token.family_id,
            token_hash=hash_refresh_token(new_raw_token),
            expires_at=now + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            ),
        )

        await repository.revoke_refresh_token(
            db,
            token,
            replaced_by_id=new_token.id,
        )

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return (
        LoginResponse(
            access_token=create_access_token(str(user.id)),
            token_type="bearer",
        ),
        new_raw_token,
    )

async def logout_user(
    db: AsyncSession,
    raw_token: str | None,
) -> None:
    if not raw_token:
        return

    token = await repository.get_refresh_token_by_hash(
        db,
        hash_refresh_token(raw_token),
        for_update=True,
    )

    if token is None:
        return

    try:
        await repository.revoke_refresh_token_family(
            db,
            token.family_id,
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise
