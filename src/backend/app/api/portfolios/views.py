from uuid import UUID

from app.api.auth.permissions import require_permission
from app.api.portfolios.repository import PortfolioFilters, PortfolioRepository
from app.api.portfolios.schema import (
    PortfolioCreateRequest,
    PortfolioSortBy,
    PortfolioUpdateRequest,
    SortOrder,
)
from app.api.portfolios.usecase import PortfolioUseCase
from app.connections.session import get_db
from app.core.responses import success_response
from app.models.user_model import User
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/portfolios", tags=["Portfolios"])


def get_portfolio_use_case(db: AsyncSession = Depends(get_db)) -> PortfolioUseCase:
    return PortfolioUseCase(PortfolioRepository(db))


def get_filters(
    search: str | None = Query(default=None, max_length=200, description="Cari nama project, kode, opportunity, kontrak, customer"),
    customer_id: UUID | None = None,
    customer_name: str | None = Query(default=None, max_length=200),
    industry_id: UUID | None = None,
    company_size_id: UUID | None = None,
    customer_type_id: UUID | None = None,
    business_unit_id: UUID | None = None,
    project_status_id: list[UUID] | None = Query(default=None),
    active_only: bool = False,
    year: int | None = Query(default=None, ge=1900, le=2200),
    product_id: UUID | None = None,
    tech_stack_id: UUID | None = None,
    partner_id: UUID | None = None,
    project_manager: str | None = Query(default=None, max_length=150),
    account_manager: str | None = Query(default=None, max_length=150),
) -> PortfolioFilters:
    return PortfolioFilters(
        search=search,
        customer_id=customer_id,
        customer_name=customer_name,
        industry_id=industry_id,
        company_size_id=company_size_id,
        customer_type_id=customer_type_id,
        business_unit_id=business_unit_id,
        project_status_ids=project_status_id or [],
        active_only=active_only,
        project_year=year,
        product_id=product_id,
        tech_stack_id=tech_stack_id,
        partner_id=partner_id,
        project_manager=project_manager,
        account_manager=account_manager,
    )


@router.get("")
async def list_portfolios(
    filters: PortfolioFilters = Depends(get_filters),
    sort_by: PortfolioSortBy = PortfolioSortBy.CREATED_AT,
    sort_order: SortOrder = SortOrder.DESC,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _: User = Depends(require_permission("portfolio.view")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    data, meta = await use_case.list_portfolios(filters, sort_by, sort_order, page, page_size)
    return success_response(message="Data portofolio berhasil diambil.", data=data, meta=meta)


# Harus di atas "/{portfolio_id}" supaya "summary" tidak dibaca sebagai id.
@router.get("/summary")
async def get_portfolio_summary(
    _: User = Depends(require_permission("portfolio.view")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    data = await use_case.summary()
    return success_response(message="Ringkasan portofolio berhasil diambil.", data=data)


@router.get("/{portfolio_id}")
async def get_portfolio(
    portfolio_id: UUID,
    _: User = Depends(require_permission("portfolio.view")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    data = await use_case.get_portfolio(portfolio_id)
    return success_response(message="Detail portofolio berhasil diambil.", data=data)


@router.post("", status_code=201)
async def create_portfolio(
    payload: PortfolioCreateRequest,
    current_user: User = Depends(require_permission("portfolio.manage")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    data = await use_case.create_portfolio(payload, current_user.id)
    return success_response(message="Portofolio berhasil ditambahkan.", data=data)


@router.patch("/{portfolio_id}")
async def update_portfolio(
    portfolio_id: UUID,
    payload: PortfolioUpdateRequest,
    current_user: User = Depends(require_permission("portfolio.manage")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    data = await use_case.update_portfolio(portfolio_id, payload, current_user.id)
    return success_response(message="Portofolio berhasil diperbarui.", data=data)


@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: UUID,
    _: User = Depends(require_permission("portfolio.manage")),
    use_case: PortfolioUseCase = Depends(get_portfolio_use_case),
):
    await use_case.delete_portfolio(portfolio_id)
    return success_response(message="Portofolio berhasil dihapus.")
