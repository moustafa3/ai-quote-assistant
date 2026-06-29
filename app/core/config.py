from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Values can come from a local .env file during development.
    The .env file must never be committed to GitHub.
    """

    app_name: str = "ai-quote-assistant"
    environment: str = "local"

    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-5.5"

    erp_provider: str = "mock"
    erp_api_base_url: str = "http://localhost:9000"
    erp_api_key: str = "local-demo-key"
    erp_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.

    Caching avoids reloading environment variables on every request.
    """
    return Settings()