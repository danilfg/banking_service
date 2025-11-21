"""Configuration for the banking service application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-level settings loaded from environment variables."""

    app_name: str = "Banking Service"
    api_prefix: str = "/api/v1"
    api_version: str = "0.1.0"

    class Config:
        env_prefix = "BANKING_"


settings = Settings()
