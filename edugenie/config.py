from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    app_name: str = "EduGenie"

    app_version: str = "1.0.0"

    environment: str = "development"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-3.8-flash"

    gemini_temperature: float = 0.3

    gemini_max_output_tokens: int = 2048

    explanation_backend: str = "auto"

    local_model_id: str = (
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    local_max_input_chars: int = 6000

    local_max_new_tokens: int = 256

    model_cache_dir: str = str(
        BASE_DIR / ".model-cache"
    )

    model_config = SettingsConfigDict(
    env_file=BASE_DIR / ".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",
)


@lru_cache
def get_settings() -> Settings:

    return Settings()