from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    FILE_ALLOWED_TYPES: list = ["application/pdf", "text/plain"]
    FILE_MAX_SIZE: int = 10  # MB
    FILE_DEFAULT_CHUNK_SIZE: int = 1024 * 1024  # 1MB

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
