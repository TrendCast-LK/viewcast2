from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    secret_key: str = "dev-only-insecure-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    database_url: str = "sqlite:///./viewcast.db"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    upload_dir: Path = BASE_DIR / "uploads"

    # From https://console.cloud.google.com — create a project, enable
    # "YouTube Data API v3", then create an API key under Credentials.
    # Without this, channel lookups fail gracefully (see app/services/youtube.py).
    youtube_api_key: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
