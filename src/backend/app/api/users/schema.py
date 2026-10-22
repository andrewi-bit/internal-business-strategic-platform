from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated

FullName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]

class UserUpdateRequest(BaseModel):
    full_name: FullName | None = None
    role_id: UUID | None = None
    is_active: bool | None = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role_id: UUID | None
    role_name: str | None
    is_active: bool
    email_verified_at: datetime | None
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)