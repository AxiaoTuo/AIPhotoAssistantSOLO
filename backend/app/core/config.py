from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # AI API Keys
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    ANTHROPIC_API_KEY: Optional[str] = None

    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    DEFAULT_AI_MODEL: str = "deepseek"

    # JWT
    JWT_SECRET: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # App
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
