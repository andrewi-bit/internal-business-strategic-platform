from enum import Enum

from pydantic import BeforeValidator, ConfigDict, Field, StringConstraints, create_model
from typing_extensions import Annotated

class MasterDataType(str, Enum):
    COMPANY_SIZES = "company-sizes"
    CUSTOMER_TYPES = "customer-types"
    INDUSTRIES = "industries"
    LEGAL_STRUCTURES = "legal-structures"
    BUSINESS_UNITS = "business-units"
    PROJECT_STATUSES = "project-statuses"
    PRODUCT_STATUSES = "product-statuses"

def _normalize_code(value):
    # Huruf besar dulu, baru dicek polanya, supaya "zz_uji" diterima sebagai "ZZ_UJI".
    return value.strip().upper() if isinstance(value, str) else value

MasterDataCode = Annotated[
    str,
    BeforeValidator(_normalize_code),
    StringConstraints(pattern=r"^[A-Z][A-Z0-9_]*$", max_length=50),
]

MasterDataName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]

SortOrder = Annotated[int, Field(ge=1, le=32767)]

def build_create_schema(prefix: str, model_name: str):
    # Nama kolom berbeda per tabel (industry_code, business_unit_code, ...),
    # jadi schema dibuat per tipe master data.
    return create_model(
        f"{model_name}CreateRequest",
        __config__=ConfigDict(extra="forbid"),
        **{
            f"{prefix}_code": (MasterDataCode, ...),
            f"{prefix}_name": (MasterDataName, ...),
            f"{prefix}_description": (str | None, None),
            "sort_order": (SortOrder | None, None),
        },
    )

def build_update_schema(prefix: str, model_name: str):
    # Kolom code tidak ikut, sehingga mengirim <x>_code dibalas 422.
    return create_model(
        f"{model_name}UpdateRequest",
        __config__=ConfigDict(extra="forbid"),
        **{
            f"{prefix}_name": (MasterDataName, None),
            f"{prefix}_description": (str | None, None),
            "sort_order": (SortOrder, None),
            "is_active": (bool, None),
        },
    )
