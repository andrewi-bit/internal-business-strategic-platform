from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.role_requests.repository import RoleRequestRepository
from app.api.role_requests.schema import (
    RoleRequestCreate,
    RoleRequestReview,
)
from app.models.role_request_model import RoleRequest
from app.models.user_model import User

class RoleRequestUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = RoleRequestRepository(db)

    async def create(
        self,
        user: User,
        payload: RoleRequestCreate,
    ) -> RoleRequest:
        pending = await self.repository.get_pending_by_user(user.id)

        if pending:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Anda masih memiliki pengajuan role yang pending.",
            )

        role = await self.repository.get_active_role(
            payload.requested_role_id
        )
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role tujuan tidak ditemukan atau tidak aktif.",
            )

        if role.code == "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role Super Admin tidak dapat diajukan melalui fitur ini.",
            )

        division = await self.repository.get_active_division(
            payload.division_id
        )
        if division is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Division tidak ditemukan atau tidak aktif.",
            )

        request = RoleRequest(
            user_id=user.id,
            requested_role_id=role.id,
            division_id=division.id,
            reason=payload.reason,
            status="pending",
        )

        try:
            await self.repository.create(request)
            await self.db.commit()
            await self.db.refresh(request)
            return request
        except IntegrityError as exc:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pengajuan pending sudah ada. Silakan periksa status pengajuan Anda.",
            ) from exc

    async def get_my_request(self, user: User):
        return await self.repository.get_latest_by_user(user.id)

    async def get_all_requests(self) -> list[RoleRequest]:
        return await self.repository.get_all()

    async def review(
        self,
        request_id: UUID,
        reviewer: User,
        payload: RoleRequestReview,
    ) -> RoleRequest:
        request = await self.repository.get_by_id(request_id)

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengajuan role tidak ditemukan.",
            )

        if request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pengajuan ini sudah pernah direview.",
            )

        if payload.status == "approved":
            role = await self.repository.get_active_role(
                request.requested_role_id
            )
            if role is None or role.code == "SUPER_ADMIN":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role tujuan tidak valid untuk persetujuan.",
                )

            target_user = await self.repository.get_user(request.user_id)
            if target_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User pemohon tidak ditemukan.",
                )

            target_user.role_id = role.id

        request.status = payload.status
        request.reviewed_by = reviewer.id
        request.review_notes = (
            payload.review_notes.strip()
            if payload.review_notes and payload.review_notes.strip()
            else None
        )

        from datetime import datetime, timezone
        request.reviewed_at = datetime.now(timezone.utc)

        try:
            await self.repository.save()
            await self.db.commit()
            await self.db.refresh(request)
            return request
        except Exception:
            await self.db.rollback()
            raise
