from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    """Базовые переменные окружения для сервисов FastAPI."""

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = "banking-service"
    environment: Literal['local', 'dev', 'prod'] = 'local'
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    host: str = '0.0.0.0'
    port: int = 8000

    # security
    jwt_secret_key: str = 'insecure-development-key'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    # infrastructure
    database_url: str | None = None
    redis_url: str | None = None
    kafka_bootstrap_servers: str = 'kafka:9092'
    splunk_hec_url: str | None = None
    splunk_hec_token: str | None = None

    cors_origins: list[str] = ['http://localhost:3000']
    cors_allow_credentials: bool = True


@lru_cache
def load_settings() -> ServiceSettings:
    """Ленивая загрузка настроек для сервисов."""

    return ServiceSettings()
