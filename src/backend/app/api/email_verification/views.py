from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schema import (
    VerifyEmailRequest,
    VerifyEmailResponse,
    ResendOTPRequest,
    ResendOTPResponse,
)
from app.api.email_verification.usecase import (
    verify_user_email,
    resend_user_otp,
)
from app.connections.session import get_db
from app.core.responses import success_response

router = APIRouter(
    prefix="/auth",
    tags=["Email Verification"],
)

@router.post(
    "/verify-email",
    status_code=status.HTTP_200_OK,
)
async def verify_email(
    payload: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await verify_user_email(db, payload)

        return success_response(
            message=result.message,
            data=result.model_dump(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "EMAIL_VERIFICATION_FAILED",
                "message": str(exc),
            },
        ) from exc

@router.post(
    "/resend-otp",
    status_code=status.HTTP_200_OK,
)
async def resend_otp(
    payload: ResendOTPRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await resend_user_otp(db, payload)

        return success_response(
            message=result.message,
            data=result.model_dump(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "RESEND_OTP_FAILED",
                "message": str(exc),
            },
        ) from exc
