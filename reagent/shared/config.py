"""Global configuration management."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    # --- Application ---
    app_name: str = "ReAgent"
    debug: bool = False
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"

    # --- Storage ---
    database_url: str = "sqlite:///./reagent.db"
    redis_url: str = "redis://localhost:6379"

    # --- AI Model Providers ---
    # Default provider: "openai" | "anthropic" | "litellm"
    ai_default_provider: str = "openai"

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = "https://api.openai.com/v1"
    openai_default_model: str = "gpt-4o"

    # Anthropic
    anthropic_api_key: Optional[str] = None
    anthropic_default_model: str = "claude-sonnet-4-20250514"

    # Local / LiteLLM
    local_api_base: Optional[str] = "http://localhost:11434/v1"
    local_api_key: str = "ollama"
    local_default_model: str = "qwen2.5:14b"

    # --- Content Generation ---
    content_output_dir: str = "./outputs"
    ffmpeg_path: str = "ffmpeg"
    banner_default_width: int = 1200
    banner_default_height: int = 628

    # --- Security ---
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="REAGENT_")


settings = Settings()

# Ensure output directory exists
Path(settings.content_output_dir).mkdir(parents=True, exist_ok=True)
