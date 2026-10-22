from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated

RoleName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]

RoleCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_upper=True,
        pattern=r"^[A-Z][A-Z0-9_]*$",
        max_length=50,
    ),
]

class RoleCreateRequest(BaseModel):
    name: RoleName
    code: RoleCode
    description: str | None = Field(default=None, max_length=2000)


class RoleUpdateRequest(BaseModel):
    name: RoleName | None = None
    description: str | None = Field(default=None, max_length=2000)
    is_active: bool | None = None

class RoleResponse(BaseModel):
    id: UUID
    name: str
    code: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class RolePermissionsUpdateRequest(BaseModel):
    permission_ids: list[UUID]
