from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schema import VerifyEmailRequest, VerifyEmailResponse, ResendOTPRequest, ResendOTPResponse
from app.api.email_verification.usecase import verify_user_email, resend_user_otp
from app.connections.session import get_db

router = APIRouter(prefix="/auth", tags=["Email Verification"])

@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_email(
    payload: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
) -> VerifyEmailResponse:
    try:
        return await verify_user_email(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.post(
    "/resend-otp",
    response_model=ResendOTPResponse,
    status_code=status.HTTP_200_OK,
)
async def resend_otp(
    payload: ResendOTPRequest,
    db: AsyncSession = Depends(get_db),
) -> ResendOTPResponse:
    try:
        return await resend_user_otp(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
