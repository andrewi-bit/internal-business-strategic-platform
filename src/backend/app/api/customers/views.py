from uuid import UUID

from app.api.auth.permissions import require_permission
from app.api.customers.repository import CustomerRepository
from app.api.customers.schema import CustomerInput, CustomerUpdateRequest
from app.api.customers.usecase import CustomerUseCase
from app.api.portfolios.repository import PortfolioFilters, PortfolioRepository
from app.api.portfolios.schema import PortfolioSortBy, SortOrder
from app.api.portfolios.usecase import PortfolioUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_customer_use_case(db: AsyncSession = Depends(get_db)) -> CustomerUseCase:
    return CustomerUseCase(CustomerRepository(db))


@router.get("")
async def list_customers(
    search: str | None = Query(default=None, max_length=200),
    industry_id: UUID | None = None,
    company_size_id: UUID | None = None,
    customer_type_id: UUID | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _: User = Depends(require_permission("portfolio.view")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    filters = {
        "search": search,
        "industry_id": industry_id,
        "company_size_id": company_size_id,
        "customer_type_id": customer_type_id,
    }
    data, meta = await use_case.list_customers(filters, page, page_size)
    return success_response(message="Data customer berhasil diambil.", data=data, meta=meta)


@router.get("/{customer_id}")
async def get_customer(
    customer_id: UUID,
    _: User = Depends(require_permission("portfolio.view")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    data = await use_case.get_customer(customer_id)
    return success_response(message="Detail customer berhasil diambil.", data=data)


@router.get("/{customer_id}/portfolios")
async def get_customer_portfolios(
    customer_id: UUID,
    sort_by: PortfolioSortBy = PortfolioSortBy.END_DATE,
    sort_order: SortOrder = SortOrder.DESC,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _: User = Depends(require_permission("portfolio.view")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
    db: AsyncSession = Depends(get_db),
):
    """Semua project milik satu customer (filter berdasarkan customer)."""
    await use_case.get_customer(customer_id)  # 404 bila tidak ada
    portfolio_use_case = PortfolioUseCase(PortfolioRepository(db))
    data, meta = await portfolio_use_case.list_portfolios(
        PortfolioFilters(customer_id=customer_id), sort_by, sort_order, page, page_size
    )
    return success_response(message="Portofolio customer berhasil diambil.", data=data, meta=meta)


@router.post("", status_code=201)
async def create_customer(
    payload: CustomerInput,
    current_user: User = Depends(require_permission("portfolio.manage")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    data = await use_case.create_customer(payload, current_user.id)
    return success_response(message="Customer berhasil ditambahkan.", data=data)


@router.patch("/{customer_id}")
async def update_customer(
    customer_id: UUID,
    payload: CustomerUpdateRequest,
    current_user: User = Depends(require_permission("portfolio.manage")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    data = await use_case.update_customer(customer_id, payload, current_user.id)
    return success_response(message="Customer berhasil diperbarui.", data=data)


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: CustomerUseCase = Depends(get_customer_use_case),
):
    await use_case.delete_customer(customer_id)
    return success_response(message="Customer berhasil dihapus.")
