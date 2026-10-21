from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None = None
    meta: dict[str, Any] | None = None

class APIErrorDetail(BaseModel):
    code: str
    details: Any | None = None

class APIErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: APIErrorDetail

def success_response(
    message: str,
    data: Any = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta,
    }

