from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Multi-Agent Orchestration Engine"
    ENV: str = "development"

    # Database Settings (Required in .env)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    # API Keys
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    # Construct URLs using computed_field (Pydantic v2 way)
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """For FastAPI / SQLAlchemy Async Driver"""
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{password}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @computed_field
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """For Alembic / SQLAlchemy Sync Driver"""
        password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql://{self.DB_USER}:"
            f"{password}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()