from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.master_data.repository import MasterDataRepository
from app.api.master_data.schema import (
    MasterDataType,
    build_create_schema,
    build_update_schema,
)
from app.models.business_unit_model import BusinessUnit
from app.models.company_size_model import CompanySize
from app.models.customer_type_model import CustomerType
from app.models.industry_model import Industry
from app.models.legal_structure_model import LegalStructure
from app.models.product_status_model import ProductStatus
from app.models.project_status_model import ProjectStatus

@dataclass(frozen=True)
class MasterDataConfig:
    model: Any
    prefix: str
    label: str
    create_schema: type[BaseModel]
    update_schema: type[BaseModel]

def _config(model, prefix: str, label: str) -> MasterDataConfig:
    return MasterDataConfig(
        model=model,
        prefix=prefix,
        label=label,
        create_schema=build_create_schema(prefix, model.__name__),
        update_schema=build_update_schema(prefix, model.__name__),
    )

MASTER_DATA_CONFIGS: dict[MasterDataType, MasterDataConfig] = {
    MasterDataType.COMPANY_SIZES: _config(CompanySize, "company_size", "Company size"),
    MasterDataType.CUSTOMER_TYPES: _config(CustomerType, "customer_type", "Customer type"),
    MasterDataType.INDUSTRIES: _config(Industry, "industry", "Industry"),
    MasterDataType.LEGAL_STRUCTURES: _config(LegalStructure, "legal_structure", "Legal structure"),
    MasterDataType.BUSINESS_UNITS: _config(BusinessUnit, "business_unit", "Business unit"),
    MasterDataType.PROJECT_STATUSES: _config(ProjectStatus, "project_status", "Project status"),
    MasterDataType.PRODUCT_STATUSES: _config(ProductStatus, "product_status", "Product status"),
}

def _validate(schema: type[BaseModel], payload: dict[str, Any]):
    try:
        return schema.model_validate(payload)
    except ValidationError as exc:
        errors = exc.errors(include_url=False)
        for error in errors:
            error["loc"] = ("body", *error["loc"])
        raise RequestValidationError(jsonable_encoder(errors))

class MasterDataUseCase:
    def __init__(self, db: AsyncSession, data_type: MasterDataType):
        self.config = MASTER_DATA_CONFIGS[data_type]
        self.prefix = self.config.prefix
        self.label = self.config.label
        self.repository = MasterDataRepository(db, self.config.model, self.prefix)

    def serialize(self, item) -> dict[str, Any]:
        return {
            "id": item.id,
            f"{self.prefix}_code": getattr(item, f"{self.prefix}_code"),
            f"{self.prefix}_name": getattr(item, f"{self.prefix}_name"),
            f"{self.prefix}_description": getattr(item, f"{self.prefix}_description"),
            "sort_order": item.sort_order,
            "is_active": item.is_active,
        }

    async def _get_or_404(self, item_id: UUID):
        item = await self.repository.get_by_id(item_id)

        if item is None:
            raise HTTPException(404, f"{self.label} tidak ditemukan.")

        return item

    async def _ensure_unique_name(self, name: str, exclude_id: UUID | None = None):
        existing = await self.repository.get_by_name(name)

        if existing is not None and existing.id != exclude_id:
            raise HTTPException(409, f"Nama {self.label} sudah digunakan.")

    async def list_items(self, include_inactive: bool = False):
        items = await self.repository.get_all(include_inactive)
        return [self.serialize(item) for item in items]

    async def create_item(self, payload: dict[str, Any]):
        data = _validate(self.config.create_schema, payload).model_dump()
        code = data[f"{self.prefix}_code"]
        name = data[f"{self.prefix}_name"]

        if await self.repository.get_by_code(code):
            raise HTTPException(409, f"Kode {self.label} sudah digunakan.")

        await self._ensure_unique_name(name)

        if data["sort_order"] is None:
            data["sort_order"] = await self.repository.get_next_sort_order()

        item = self.config.model(**data, is_active=True)

        try:
            await self.repository.create(item)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, f"Kode atau nama {self.label} sudah digunakan.")

        return self.serialize(item)

    async def update_item(self, item_id: UUID, payload: dict[str, Any]):
        changes = _validate(self.config.update_schema, payload).model_dump(
            exclude_unset=True
        )
        item = await self._get_or_404(item_id)

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        name_field = f"{self.prefix}_name"
        if name_field in changes:
            await self._ensure_unique_name(changes[name_field], exclude_id=item.id)

        for field, value in changes.items():
            setattr(item, field, value)

        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, f"Nama {self.label} sudah digunakan.")

        return self.serialize(item)

    async def delete_item(self, item_id: UUID):
        item = await self._get_or_404(item_id)

        if await self.repository.try_delete(item):
            await self.repository.save()
            return {"id": item_id, "deleted": True}, f"{self.label} berhasil dihapus."

        item = await self._get_or_404(item_id)
        item.is_active = False
        await self.repository.save()

        return (
            {"id": item_id, "deleted": False, "is_active": False},
            f"{self.label} masih dipakai data lain, jadi dinonaktifkan.",
        )
