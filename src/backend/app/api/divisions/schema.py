from uuid import UUID

from pydantic import BaseModel, ConfigDict

class DivisionResponse(BaseModel):
    id: UUID
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)