from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ddd_fastapi_boilerplate"

    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Application Configuration
    APP_NAME: str = "DDD FastAPI Boilerplate"
    APP_VERSION: str = "0.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # Use ConfigDict instead of class Config
    model_config = {"env_file": ".env"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
