"""Global configuration management."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ReAgent"
    debug: bool = False
    redis_url: str = "redis://localhost:6379"
    database_url: str = "sqlite:///./reagent.db"
    sentry_dsn: str = ""
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_prefix = "REAGENT_"


settings = Settings()
