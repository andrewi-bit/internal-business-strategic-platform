from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.permissions import require_permission
from app.api.products.repository import ProductRepository
from app.api.products.schema import ProductCreateRequest, ProductUpdateRequest
from app.api.products.usecase import ProductUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_use_case(
    db: AsyncSession = Depends(get_db),
) -> ProductUseCase:
    return ProductUseCase(ProductRepository(db))

@router.get("")
async def get_products(
    product_status_id: UUID | None = Query(default=None),
    _: User = Depends(require_permission("portfolio.view")),
    use_case: ProductUseCase = Depends(get_product_use_case),
):
    data = await use_case.list_products(product_status_id)
    return success_response(message="Data product berhasil diambil.", data=data)

@router.post("")
async def create_product(
    payload: ProductCreateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: ProductUseCase = Depends(get_product_use_case),
):
    data = await use_case.create_product(payload)
    return success_response(message="Product berhasil ditambahkan.", data=data)

@router.patch("/{product_id}")
async def update_product(
    product_id: UUID,
    payload: ProductUpdateRequest,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: ProductUseCase = Depends(get_product_use_case),
):
    data = await use_case.update_product(product_id, payload)
    return success_response(message="Product berhasil diperbarui.", data=data)

@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: ProductUseCase = Depends(get_product_use_case),
):
    data = await use_case.delete_product(product_id)
    return success_response(message="Product berhasil dihapus.", data=data)
