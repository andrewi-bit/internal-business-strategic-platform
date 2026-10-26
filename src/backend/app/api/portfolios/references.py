from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ReferenceChecker:
    """Memeriksa bahwa semua id yang dikirim klien menunjuk ke master data yang ada (dan aktif),
    lalu membalas satu error 422 yang menyebut field dan id mana yang bermasalah."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._problems: list[dict] = []

    async def check(
        self,
        field: str,
        model,
        ids: set[UUID] | list[UUID],
        *,
        require_active: bool = True,
    ) -> None:
        wanted = set(ids)

        if not wanted:
            return

        query = select(model.id).where(model.id.in_(wanted))

        # Product tidak punya is_active (statusnya lewat product_status), jadi hanya dicek keberadaannya.
        if require_active and hasattr(model, "is_active"):
            query = query.where(model.is_active.is_(True))

        found = set((await self.db.execute(query)).scalars().all())
        missing = wanted - found

        if missing:
            self._problems.append(
                {
                    "field": field,
                    "ids": sorted(str(item) for item in missing),
                    "reason": "tidak ditemukan atau sudah nonaktif"
                    if require_active and hasattr(model, "is_active")
                    else "tidak ditemukan",
                }
            )

    def raise_if_invalid(self) -> None:
        if self._problems:
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "INVALID_REFERENCE",
                    "message": "Ada data referensi yang tidak valid.",
                    "details": self._problems,
                },
            )
