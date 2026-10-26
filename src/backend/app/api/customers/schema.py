from uuid import UUID

from app.api.portfolios.fields import CustomerName
from app.api.portfolios.fields import optional_text as _optional_text
from pydantic import BaseModel, ConfigDict, Field


class CustomerInput(BaseModel):
    """Dipakai saat membuat customer baru, baik lewat /customers maupun inline di POST /portfolios."""

    customer_name: CustomerName
    company_size_id: UUID
    annual_revenue: _optional_text(100) = Field(
        default=None,
        description='Teks bebas, mengikuti Excel, contoh "115T (FY 2025)"',
    )
    customer_type_id: UUID
    industry_id: UUID
    location: _optional_text(150) = None
    legal_structure_id: UUID

    model_config = ConfigDict(extra="forbid")


class CustomerUpdateRequest(BaseModel):
    customer_name: CustomerName = None
    company_size_id: UUID = None
    annual_revenue: _optional_text(100) = None
    customer_type_id: UUID = None
    industry_id: UUID = None
    location: _optional_text(150) = None
    legal_structure_id: UUID = None

    model_config = ConfigDict(extra="forbid")
