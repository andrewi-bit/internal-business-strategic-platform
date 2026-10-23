from enum import Enum

from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

class TechStackCategory(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATA_STORAGE = "data_storage"

TechStackName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]

class TechStackCreateRequest(BaseModel):
    tech_stack_category: TechStackCategory
    tech_stack_name: TechStackName

    model_config = ConfigDict(extra="forbid")

class TechStackUpdateRequest(BaseModel):
    tech_stack_category: TechStackCategory = None
    tech_stack_name: TechStackName = None
    is_active: bool = None

    model_config = ConfigDict(extra="forbid")
