from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated

ReasonText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=10, max_length=2000),
]

class RoleRequestCreate(BaseModel):
    division_id: UUID
    requested_role_id: UUID
    reason: ReasonText

class RoleRequestReview(BaseModel):
    status: Literal["approved", "rejected"]
    review_notes: str | None = Field(default=None, max_length=2000)

class RoleRequestResponse(BaseModel):
    id: UUID
    user_id: UUID
    requested_role_id: UUID
    division_id: UUID
    role_name: str
    division_name: str
    reason: str
    status: str
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    review_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)