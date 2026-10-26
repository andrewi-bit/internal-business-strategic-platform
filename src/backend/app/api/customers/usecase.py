from uuid import UUID

from app.api.customers.repository import CustomerRepository
from app.api.customers.schema import CustomerInput, CustomerUpdateRequest
from app.api.portfolios.references import ReferenceChecker
from app.api.portfolios.serializers import serialize_customer
from app.models.company_size_model import CompanySize
from app.models.customer_model import Customer
from app.models.customer_type_model import CustomerType
from app.models.industry_model import Industry
from app.models.legal_structure_model import LegalStructure
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

NAME_TAKEN = "Nama customer sudah digunakan."


async def check_customer_references(checker: ReferenceChecker, ids: dict) -> None:
    """ids: field -> id (None dilewati)."""
    models = {
        "company_size_id": CompanySize,
        "customer_type_id": CustomerType,
        "industry_id": Industry,
        "legal_structure_id": LegalStructure,
    }
    for field, model in models.items():
        if ids.get(field) is not None:
            await checker.check(field, model, [ids[field]])


def page_meta(page: int, page_size: int, total: int) -> dict:
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
    }


class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def _get_or_404(self, customer_id: UUID) -> Customer:
        customer = await self.repository.get_by_id(customer_id)
        if customer is None:
            raise HTTPException(404, "Customer tidak ditemukan.")
        return customer

    async def _ensure_unique_name(self, name: str, exclude_id: UUID | None = None) -> None:
        existing = await self.repository.get_by_name(name)
        if existing is not None and existing.id != exclude_id:
            raise HTTPException(409, NAME_TAKEN)

    async def build_customer(self, payload: CustomerInput, user_id: UUID | None) -> Customer:
        """Dipakai juga oleh POST /portfolios saat customer dibuat inline."""
        checker = ReferenceChecker(self.repository.db)
        await check_customer_references(checker, payload.model_dump())
        checker.raise_if_invalid()
        await self._ensure_unique_name(payload.customer_name)

        customer = Customer(**payload.model_dump(), created_by=user_id, updated_by=user_id)
        self.repository.add(customer)
        return customer

    async def list_customers(self, filters: dict, page: int, page_size: int):
        rows, total = await self.repository.list_customers(page=page, page_size=page_size, **filters)
        data = [
            serialize_customer(customer, project_count=count, active_project_count=active)
            for customer, count, active in rows
        ]
        return data, page_meta(page, page_size, total)

    async def get_customer(self, customer_id: UUID):
        customer = await self._get_or_404(customer_id)
        count, active = await self.repository.counts(customer_id)
        return serialize_customer(customer, project_count=count, active_project_count=active)

    async def create_customer(self, payload: CustomerInput, user_id: UUID | None):
        customer = await self.build_customer(payload, user_id)
        try:
            await self.repository.flush()
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, NAME_TAKEN)
        return await self.get_customer(customer.id)

    async def update_customer(self, customer_id: UUID, payload: CustomerUpdateRequest, user_id: UUID | None):
        customer = await self._get_or_404(customer_id)
        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        checker = ReferenceChecker(self.repository.db)
        await check_customer_references(checker, changes)
        checker.raise_if_invalid()

        if "customer_name" in changes:
            await self._ensure_unique_name(changes["customer_name"], exclude_id=customer.id)

        for field, value in changes.items():
            setattr(customer, field, value)
        customer.updated_by = user_id

        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, NAME_TAKEN)

        return await self.get_customer(customer_id)

    async def delete_customer(self, customer_id: UUID) -> None:
        customer = await self._get_or_404(customer_id)
        count, _ = await self.repository.counts(customer_id)

        if count:
            raise HTTPException(
                409,
                f"Customer masih memiliki {count} project, hapus atau pindahkan project-nya terlebih dahulu.",
            )

        await self.repository.delete(customer)
        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Customer masih dipakai data lain.")
