from fastapi.encoders import jsonable_encoder
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def get_error_code(status_code: int) -> str:
    codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_SERVER_ERROR",
    }
    return codes.get(status_code, "HTTP_ERROR")

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    detail = exc.detail
    code = get_error_code(exc.status_code)

    if isinstance(detail, dict):
        code = detail.get("code", code)
        message = detail.get("message", "Request gagal")
        error_details = detail.get("details")
    else:
        message = str(detail)
        error_details = None

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": message,
            "error": {
                "code": code,
                "details": error_details,
            },
        },
        headers=exc.headers,
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validasi request gagal",
            "error": {
                "code": "VALIDATION_ERROR",
                "details": jsonable_encoder(exc.errors(), custom_encoder={ValueError: str}),
            },
        },
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Terjadi kesalahan internal server",
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "details": None,
            },
        },
    )
