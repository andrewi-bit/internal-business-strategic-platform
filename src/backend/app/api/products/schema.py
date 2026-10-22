from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

ProductName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]

class ProductCreateRequest(BaseModel):
    product_name: ProductName
    product_description: str | None = None
    product_status_id: UUID

    model_config = ConfigDict(extra="forbid")

class ProductUpdateRequest(BaseModel):
    product_name: ProductName = None
    product_description: str | None = None
    product_status_id: UUID = None

    model_config = ConfigDict(extra="forbid")
