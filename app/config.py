from __future__ import annotations

import os
from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv


class Settings(BaseModel):
    api_key: str | None = os.getenv("APIFOOTBALL_API_KEY")
    base_url: str = os.getenv("APIFOOTBALL_BASE_URL", "https://v3.football.api-sports.io")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./epl.db")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    league_id_default: int = int(os.getenv("LEAGUE_ID", "39"))


@lru_cache
def get_settings() -> Settings:
    # Load .env on first call
    load_dotenv()
    return Settings()


