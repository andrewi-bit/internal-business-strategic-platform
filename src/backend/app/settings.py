import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_NAME: str = "Internal Business Strategic Platform"
    PORT: int = 8000
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    FRONTEND_URL: str = "http://localhost:3000"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PGADMIN_EMAIL: str = "admin@example.com"
    PGADMIN_PASSWORD: str = "admin"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    env_state = os.getenv("APP_ENV", "development")
    env_file_path = f"app/config/env/{env_state}.env"

    return Settings(_env_file=env_file_path)


settings = get_settings()