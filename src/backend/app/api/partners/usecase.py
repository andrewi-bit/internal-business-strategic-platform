from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.partners.repository import PartnerRepository
from app.api.partners.schema import PartnerCreateRequest, PartnerUpdateRequest
from app.models.partner_model import Partner

def serialize_partner(partner: Partner):
    return {
        "id": partner.id,
        "partner_name": partner.partner_name,
        "is_active": partner.is_active,
    }

class PartnerUseCase:
    def __init__(self, repository: PartnerRepository):
        self.repository = repository

    async def _get_or_404(self, partner_id: UUID) -> Partner:
        partner = await self.repository.get_by_id(partner_id)

        if partner is None:
            raise HTTPException(404, "Partner tidak ditemukan.")

        return partner

    async def _ensure_unique_name(self, name: str, exclude_id: UUID | None = None):
        existing = await self.repository.get_by_name(name)

        if existing is None or existing.id == exclude_id:
            return

        if not existing.is_active:
            raise HTTPException(
                409,
                "Partner dengan nama ini sudah ada tetapi nonaktif. "
                "Aktifkan kembali lewat PATCH dengan is_active true.",
            )

        raise HTTPException(409, "Nama partner sudah digunakan.")

    async def list_partners(self, search: str | None = None, include_inactive: bool = False):
        partners = await self.repository.get_all(search, include_inactive)
        return [serialize_partner(partner) for partner in partners]

    async def create_partner(self, payload: PartnerCreateRequest):
        await self._ensure_unique_name(payload.partner_name)

        partner = Partner(partner_name=payload.partner_name, is_active=True)

        try:
            await self.repository.create(partner)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Nama partner sudah digunakan.")

        return serialize_partner(partner)

    async def update_partner(self, partner_id: UUID, payload: PartnerUpdateRequest):
        partner = await self._get_or_404(partner_id)
        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        if "partner_name" in changes:
            await self._ensure_unique_name(changes["partner_name"], exclude_id=partner.id)

        for field, value in changes.items():
            setattr(partner, field, value)

        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Nama partner sudah digunakan.")

        return serialize_partner(partner)

    async def delete_partner(self, partner_id: UUID):
        partner = await self._get_or_404(partner_id)

        if await self.repository.try_delete(partner):
            await self.repository.save()
            return {"id": partner_id, "deleted": True}, "Partner berhasil dihapus."

        partner = await self._get_or_404(partner_id)
        partner.is_active = False
        await self.repository.save()

        return (
            {"id": partner_id, "deleted": False, "is_active": False},
            "Partner masih dipakai project, jadi dinonaktifkan.",
        )
