import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, MySQLDsn, RedisDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get external APP_ENV, default to empty (which will just use .env)
_APP_ENV = os.getenv("APP_ENV", "").lower()
_ENV_FILE = f".env.{_APP_ENV}" if _APP_ENV else ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Skeleton"
    API_V1_STR: str = "/api/v1"

    # Database
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        # Access fields directly from the values dictionary or validation info
        # Note: In Pydantic v2, we access the data differently if needed,
        # but for simple pre-validation, we can often rely on the input or compute it.
        # However, `values` argument in `mode='before'` definition might not be fully populated
        # if fields are validated in order.
        # A safer approach in Pydantic V2 is to use `computed_field` or validate on `after`.
        # For simplicity/compatibility, we can construct it if it's missing.

        return MySQLDsn.build(
            scheme="mysql+aiomysql",
            username=values.data.get("MYSQL_USER"),
            password=values.data.get("MYSQL_PASSWORD"),
            host=values.data.get("MYSQL_HOST"),
            port=values.data.get("MYSQL_PORT"),
        ).unicode_string()

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_URI: Optional[str] = None

    @field_validator("REDIS_URI", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.data.get("REDIS_HOST"),
            port=values.data.get("REDIS_PORT"),
            password=values.data.get("REDIS_PASSWORD"),
            path=f"{values.data.get('REDIS_DB') or 0}",
        ).unicode_string()

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Gunicorn
    GUNICORN_BIND: str = "0.0.0.0:8000"
    GUNICORN_WORKERS: int = 4
    GUNICORN_WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
