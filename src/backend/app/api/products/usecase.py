from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.products.repository import ProductRepository
from app.api.products.schema import ProductCreateRequest, ProductUpdateRequest
from app.models.product_model import Product
from app.models.product_status_model import ProductStatus

def serialize_product(product: Product, status: ProductStatus):
    return {
        "id": product.id,
        "product_name": product.product_name,
        "product_description": product.product_description,
        "product_status": {
            "id": status.id,
            "product_status_code": status.product_status_code,
            "product_status_name": status.product_status_name,
        },
    }

class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def _get_or_404(self, product_id: UUID) -> Product:
        product = await self.repository.get_by_id(product_id)

        if product is None:
            raise HTTPException(404, "Product tidak ditemukan.")

        return product

    async def _get_status_or_422(self, product_status_id: UUID) -> ProductStatus:
        status = await self.repository.get_status_by_id(product_status_id)

        if status is None:
            raise HTTPException(422, "Product status tidak ditemukan.")

        return status

    async def _ensure_unique_name(self, name: str, exclude_id: UUID | None = None):
        existing = await self.repository.get_by_name(name)

        if existing is not None and existing.id != exclude_id:
            raise HTTPException(409, "Nama product sudah digunakan.")

    async def list_products(self, product_status_id: UUID | None = None):
        rows = await self.repository.get_all(product_status_id)
        return [serialize_product(product, status) for product, status in rows]

    async def create_product(self, payload: ProductCreateRequest):
        status = await self._get_status_or_422(payload.product_status_id)
        await self._ensure_unique_name(payload.product_name)

        product = Product(
            product_name=payload.product_name,
            product_description=payload.product_description,
            product_status_id=payload.product_status_id,
        )

        try:
            await self.repository.create(product)
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Nama product sudah digunakan.")

        return serialize_product(product, status)

    async def update_product(self, product_id: UUID, payload: ProductUpdateRequest):
        product = await self._get_or_404(product_id)
        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(400, "Tidak ada data yang diperbarui.")

        if "product_status_id" in changes:
            await self._get_status_or_422(changes["product_status_id"])

        if "product_name" in changes:
            await self._ensure_unique_name(changes["product_name"], exclude_id=product.id)

        for field, value in changes.items():
            setattr(product, field, value)

        try:
            await self.repository.save()
        except IntegrityError:
            await self.repository.rollback()
            raise HTTPException(409, "Nama product sudah digunakan.")

        status = await self.repository.get_status_by_id(product.product_status_id)
        return serialize_product(product, status)

    async def delete_product(self, product_id: UUID):
        product = await self._get_or_404(product_id)

        if not await self.repository.try_delete(product):
            raise HTTPException(
                409,
                "Product masih dipakai project, jadi tidak bisa dihapus. "
                "Ubah status-nya menjadi Deprecated jika product tidak dijual lagi.",
            )

        await self.repository.save()
        return {"id": product_id, "deleted": True}
