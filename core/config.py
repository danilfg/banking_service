from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Banking Service"
    api_prefix: str = "/api/v1"
    api_version: str = "0.1.0"

    class Config:
        env_prefix = "BANKING_"


settings = Settings()
