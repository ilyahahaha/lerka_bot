from functools import lru_cache

from pydantic import BaseSettings


@lru_cache(maxsize=1)
class Settings(BaseSettings):
    bot_token: str

    allowed_ids: list[int]

    class Config:
        env_file = ".env"
