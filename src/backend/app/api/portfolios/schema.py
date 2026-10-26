from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from app.api.customers.schema import CustomerInput
from app.api.portfolios.fields import (
    Money,
    PartnerRole,
    ProjectCode,
    ProjectName,
    ProjectYear,
)
from app.api.portfolios.fields import (
    optional_text as _optional_text,
)
from pydantic import BaseModel, ConfigDict, Field, model_validator


class PortfolioSortBy(str, Enum):
    CREATED_AT = "created_at"
    PROJECT_NAME = "project_name"
    PROJECT_CODE = "project_code"
    CUSTOMER_NAME = "customer_name"
    PROJECT_YEAR = "project_year"
    START_DATE = "start_date"
    END_DATE = "end_date"
    VALUE_BEFORE_TAX = "value_before_tax"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


# ───────────────────────── Project perspective ─────────────────────────
class ProjectInput(BaseModel):
    project_code: ProjectCode = Field(description='"Project ID" di Excel, unik. Contoh ITMS_MON_BMRI_2026_PRO')
    project_name: ProjectName
    opportunity: _optional_text(250) = None
    project_year: ProjectYear
    contract_po_name: _optional_text(250) = None
    contract_po_number: _optional_text(150) = None
    business_unit_id: UUID
    project_status_id: UUID
    value_before_tax: Money
    carry_over_value: Money | None = None
    project_manager: _optional_text(150) = None
    account_manager: _optional_text(150) = None
    start_date: date
    end_date: date
    project_objective: _optional_text(5000) = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def _check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date tidak boleh lebih awal dari start_date")
        return self


class ProjectUpdateInput(BaseModel):
    project_code: ProjectCode = None
    project_name: ProjectName = None
    opportunity: _optional_text(250) = None
    project_year: ProjectYear = None
    contract_po_name: _optional_text(250) = None
    contract_po_number: _optional_text(150) = None
    business_unit_id: UUID = None
    project_status_id: UUID = None
    value_before_tax: Money = None
    carry_over_value: Money | None = None
    project_manager: _optional_text(150) = None
    account_manager: _optional_text(150) = None
    start_date: date = None
    end_date: date = None
    project_objective: _optional_text(5000) = None

    model_config = ConfigDict(extra="forbid")


# ───────────────────────── Financial perspective ─────────────────────────
class FinancialInput(BaseModel):
    revenue: Money | None = Field(
        default=None,
        description="Kosong = sama dengan value_before_tax project (seperti formula di Excel)",
    )
    cogs: Money = Decimal(0)
    operational_costs: Money = Decimal(0)

    model_config = ConfigDict(extra="forbid")


class FinancialUpdateInput(BaseModel):
    revenue: Money = None
    cogs: Money = None
    operational_costs: Money = None

    model_config = ConfigDict(extra="forbid")


# ───────────────────────── Partner perspective ─────────────────────────
class ProjectPartnerInput(BaseModel):
    partner_id: UUID
    partner_role: PartnerRole = Field(
        default="Partner",
        description="Contoh: Principal, Vendor",
    )

    model_config = ConfigDict(extra="forbid")


# ───────────────────────── Portfolio (semua perspektif) ─────────────────────────
class PortfolioCreateRequest(BaseModel):
    customer_id: UUID | None = Field(default=None, description="Customer yang sudah ada")
    customer: CustomerInput | None = Field(default=None, description="Atau buat customer baru sekaligus")
    project: ProjectInput
    financial: FinancialInput = Field(default_factory=FinancialInput)
    product_ids: list[UUID] = Field(default_factory=list, description='Tech Stack: "Product Use"')
    tech_stack_ids: list[UUID] = Field(
        default_factory=list,
        description="Tech Stack: Frontend, Backend, Data & Storage (kategori ikut master tech stack)",
    )
    partners: list[ProjectPartnerInput] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def _exactly_one_customer(self):
        if (self.customer_id is None) == (self.customer is None):
            raise ValueError("Isi salah satu: customer_id atau customer")
        return self

    @model_validator(mode="after")
    def _unique_partners(self):
        ids = [item.partner_id for item in self.partners]
        if len(ids) != len(set(ids)):
            raise ValueError("partner_id tidak boleh dobel dalam satu portofolio")
        return self


class PortfolioUpdateRequest(BaseModel):
    """PATCH: hanya bagian yang dikirim yang diubah. List (product_ids, tech_stack_ids, partners)
    yang dikirim menggantikan seluruh isi list sebelumnya."""

    customer_id: UUID = None
    project: ProjectUpdateInput = None
    financial: FinancialUpdateInput = None
    product_ids: list[UUID] = None
    tech_stack_ids: list[UUID] = None
    partners: list[ProjectPartnerInput] = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def _unique_partners(self):
        if self.partners is not None:
            ids = [item.partner_id for item in self.partners]
            if len(ids) != len(set(ids)):
                raise ValueError("partner_id tidak boleh dobel dalam satu portofolio")
        return self
