# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # -----------------------------
    # App Settings
    # -----------------------------
    APP_NAME: str = "Multi-Agent Orchestration Engine"
    ENV: str = "development"

    # -----------------------------
    # Database Settings
    # -----------------------------
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    # -----------------------------
    # API Keys
    # -----------------------------
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None

    # -----------------------------
    # Redis (optional)
    # -----------------------------
    REDIS_URL: str | None = "redis://localhost:6379/0"

    # -----------------------------
    # JWT / Security (optional)
    # -----------------------------
    JWT_SECRET: str | None = None
    JWT_ALGORITHM: str = "HS256"

    # -----------------------------
    # Email (optional)
    # -----------------------------
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_SERVER: str | None = None
    MAIL_PORT: int | None = None

    # -----------------------------
    # Construct Database URL
    # -----------------------------
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    # -----------------------------
    # Alembic (sync URL)
    # -----------------------------
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    # -----------------------------
    # Load .env
    # -----------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


# -----------------------------
# Singleton (Best Practice)
# -----------------------------
@lru_cache
def get_settings() -> Settings:
    return Settings()


# -----------------------------
# Global Access
# -----------------------------
settings = get_settings()