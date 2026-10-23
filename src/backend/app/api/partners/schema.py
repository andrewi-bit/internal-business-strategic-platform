from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

PartnerName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
]

class PartnerCreateRequest(BaseModel):
    partner_name: PartnerName

    model_config = ConfigDict(extra="forbid")

class PartnerUpdateRequest(BaseModel):
    partner_name: PartnerName = None
    is_active: bool = None

    model_config = ConfigDict(extra="forbid")
