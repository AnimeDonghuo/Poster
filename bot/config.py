import os
from dataclasses import dataclass


@dataclass
class Config:
    BOT_TOKEN: str
    TMDB_API_KEY: str
    OMDB_API_KEY: str
    REDIS_URL: str | None
    DEBUG: bool
    DEFAULT_LANGUAGE: str
    POSTER_PAGE_SIZE: int
    CACHE_TTL_SECONDS: int
    REQUEST_TIMEOUT: int

    @staticmethod
    def from_env() -> "Config":
        return Config(
            BOT_TOKEN=os.environ["BOT_TOKEN"],
            TMDB_API_KEY=os.environ.get("TMDB_API_KEY", ""),
            OMDB_API_KEY=os.environ.get("OMDB_API_KEY", ""),
            REDIS_URL=os.environ.get("REDIS_URL"),
            DEBUG=os.environ.get("DEBUG", "false").lower() == "true",
            DEFAULT_LANGUAGE=os.environ.get("DEFAULT_LANGUAGE", "en-US"),
            POSTER_PAGE_SIZE=int(os.environ.get("POSTER_PAGE_SIZE", "6")),
            CACHE_TTL_SECONDS=int(os.environ.get("CACHE_TTL_SECONDS", "900")),
            REQUEST_TIMEOUT=int(os.environ.get("REQUEST_TIMEOUT", "10")),
        )


config = Config.from_env()
