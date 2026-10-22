import hashlib
import logging
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from authlib.integrations.starlette_client import OAuth
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import repository
from app.api.auth.dependencies import bearer_scheme, get_current_user
from app.api.auth.schema import (
    RegisterRequest,
    LoginRequest,
    CurrentUserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.api.auth.usecase import (
    register_user,
    login_user,
    refresh_access_token,
    logout_user,
    request_password_reset,
    reset_password,
)
from app.connections.redis import get_redis
from app.connections.session import get_db
from app.core.responses import success_response
from app.core.security import (
    decode_access_token,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from app.models.user_model import User
from app.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "openid email profile"},
)

COOKIE_PATH = f"{settings.API_V1_PREFIX}/auth"


def set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path=COOKIE_PATH,
    )


def clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        path=COOKIE_PATH,
    )


@router.get("/google/login")
async def google_login(request: Request):
    redirect_response = await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI,
    )

    return success_response(
        message="URL login Google berhasil dibuat",
        data={"login_url": redirect_response.headers["location"]},
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "GOOGLE_USER_INFO_UNAVAILABLE",
                    "message": "Informasi akun Google tidak tersedia",
                },
            )

        google_id = user_info.get("sub")
        email = str(user_info.get("email", "")).strip().lower()
        full_name = user_info.get("name") or email
        email_verified = user_info.get("email_verified", False)
        hosted_domain = user_info.get("hd", "")

        allowed_domain = settings.GOOGLE_ALLOWED_DOMAIN.lower()

        if (
            not google_id
            or not email
            or "@" not in email
            or email.rsplit("@", 1)[-1] != allowed_domain
            or hosted_domain.lower() != allowed_domain
            or email_verified is not True
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "GOOGLE_ACCOUNT_NOT_ALLOWED",
                    "message": "Akun Google tidak diizinkan",
                },
            )

        user = await repository.get_user_by_google_id(db, google_id)

        if user is None:
            user = await repository.get_user_by_email(db, email)

            if user is not None:
                if user.email_verified_at is None:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "code": "EMAIL_NOT_VERIFIED",
                            "message": (
                                "Verifikasi email akun manual terlebih dahulu"
                            ),
                        },
                    )

                if not user.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "code": "ACCOUNT_INACTIVE",
                            "message": "Akun tidak aktif",
                        },
                    )

                if user.google_id is not None:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail={
                            "code": "GOOGLE_ACCOUNT_ALREADY_LINKED",
                            "message": (
                                "Akun Google sudah terhubung ke akun lain"
                            ),
                        },
                    )

                await repository.link_google_id(db, user, google_id)

            else:
                user = User(
                    email=email,
                    full_name=full_name,
                    google_id=google_id,
                    email_verified_at=datetime.now(timezone.utc),
                    role_id=None,
                    is_active=True,
                )
                db.add(user)
                await db.flush()

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "ACCOUNT_INACTIVE",
                    "message": "Akun tidak aktif",
                },
            )

        if user.email_verified_at is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "EMAIL_NOT_VERIFIED",
                    "message": "Email belum diverifikasi",
                },
            )

        now = datetime.now(timezone.utc)
        raw_refresh_token = create_refresh_token()

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

        set_refresh_cookie(response, raw_refresh_token)

        access_token = create_access_token(
            str(user.id),
            user.token_version,
        )

        return success_response(
            message="Login Google berhasil",
            data={
                "access_token": access_token,
                "token_type": "bearer",
            },
        )

    except HTTPException:
        await db.rollback()
        raise

    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "ACCOUNT_CONFLICT",
                "message": "Akun sudah terdaftar atau terhubung",
            },
        ) from exc

    except Exception as exc:
        await db.rollback()
        logger.exception("Autentikasi Google gagal")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "GOOGLE_AUTHENTICATION_FAILED",
                "message": "Autentikasi Google gagal",
            },
        ) from exc


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await register_user(db, payload)

        return success_response(
            message=result.message,
            data=result.model_dump(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "REGISTRATION_CONFLICT",
                "message": str(exc),
            },
        ) from exc

    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_ALREADY_REGISTERED",
                "message": "Email sudah terdaftar",
            },
        ) from exc


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    try:
        login_response, refresh_token = await login_user(db, payload)
        set_refresh_cookie(response, refresh_token)

        return success_response(
            message="Login berhasil",
            data=login_response.model_dump(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": str(exc),
            },
        ) from exc

    except PermissionError as exc:
        if str(exc) == "Email belum diverifikasi":
            detail = {
                "code": "EMAIL_NOT_VERIFIED",
                "message": "Email belum diverifikasi",
            }
        elif str(exc) == "Akun tidak aktif":
            detail = {
                "code": "ACCOUNT_INACTIVE",
                "message": "Akun tidak aktif",
            }
        else:
            detail = {
                "code": "AUTHENTICATION_FORBIDDEN",
                "message": str(exc),
            }

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        ) from exc


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
)
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await request_password_reset(db, str(payload.email))

    return success_response(
        message=result.message,
        data=None,
    )


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
)
async def reset_password_endpoint(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await reset_password(
            db,
            payload.token,
            payload.new_password,
        )

        return success_response(
            message=result.message,
            data=None,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_OR_EXPIRED_RESET_TOKEN",
                "message": "Token reset tidak valid atau kedaluwarsa",
            },
        ) from exc


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    result = CurrentUserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
    )

    return success_response(
        message="Data user berhasil diambil",
        data=result.model_dump(),
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get(
        settings.REFRESH_TOKEN_COOKIE_NAME
    )

    if not refresh_token:
        clear_refresh_cookie(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "REFRESH_TOKEN_MISSING",
                "message": "Refresh token tidak ditemukan",
            },
        )

    try:
        login_response, new_refresh_token = await refresh_access_token(
            db,
            refresh_token,
        )

        set_refresh_cookie(response, new_refresh_token)

        return success_response(
            message="Token berhasil diperbarui",
            data=login_response.model_dump(),
        )

    except ValueError as exc:
        clear_refresh_cookie(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_REFRESH_TOKEN",
                "message": str(exc),
            },
        ) from exc

    except PermissionError as exc:
        clear_refresh_cookie(response)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "REFRESH_FORBIDDEN",
                "message": str(exc),
            },
        ) from exc


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    request: Request,
    response: Response,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    access_token = credentials.credentials
    payload = decode_access_token(access_token)

    expires_at = payload.get("exp")

    if expires_at is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_ACCESS_TOKEN",
                "message": "Token tidak memiliki waktu kedaluwarsa",
            },
        )

    ttl = int(expires_at - datetime.now(timezone.utc).timestamp())

    if ttl > 0:
        token_hash = hashlib.sha256(
            access_token.encode("utf-8")
        ).hexdigest()

        await redis.set(
            f"revoked_access_token:{token_hash}",
            "1",
            ex=ttl,
        )

    refresh_token = request.cookies.get(
        settings.REFRESH_TOKEN_COOKIE_NAME
    )

    await logout_user(db, refresh_token)
    clear_refresh_cookie(response)

    return success_response(
        message="Logout berhasil",
        data=None,
    )
