from enum import Enum
from pydantic_settings import BaseSettings


class RoleEnum(str, Enum):
    """User roles in the system"""
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Finance Dashboard Backend"
    app_version: str = "1.0.0"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
