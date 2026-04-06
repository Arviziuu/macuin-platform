from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://macuin_user:macuin_secret_2024@db:5432/macuin_db"
    SECRET_KEY: str = "macuin-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
