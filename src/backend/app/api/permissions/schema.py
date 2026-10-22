from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

PermissionCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        pattern=r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$",
        max_length=100,
    ),
]

PermissionName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]

class PermissionCreateRequest(BaseModel):
    code: PermissionCode
    name: PermissionName
    description: str | None = Field(default=None, max_length=2000)

class PermissionUpdateRequest(BaseModel):
    name: PermissionName | None = None
    description: str | None = Field(default=None, max_length=2000)

class PermissionResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
