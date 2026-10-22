from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

from app.settings import settings
from app.api.auth.views import router as auth_router
from app.api.email_verification.views import (
    router as email_verification_router,
)
from app.api.divisions.views import router as divisions_router
from app.api.role_requests.views import router as role_requests_router
from app.api.roles.views import router as roles_router
from app.api.users.views import router as users_router
from app.api.permissions.views import router as permissions_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)

app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    email_verification_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    divisions_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    role_requests_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    roles_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    users_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    permissions_router,
    prefix=settings.API_V1_PREFIX,
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
    }
