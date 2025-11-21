"""Application settings loaded from environment variables and .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-level settings."""

    app_name: str = "Banking Service"
    api_prefix: str = "/api/v1"
    api_version: str = "0.1.0"
    database_url: str = "postgresql+asyncpg://localhost:5432/banking_db"

    model_config = SettingsConfigDict(
        env_prefix="BANKING_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
