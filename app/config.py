from __future__ import annotations

import os
from typing import Optional
from pydantic_settings import BaseSettings

import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()


class Settings(BaseSettings):
    # API Configuration
    api_key: Optional[str] = None
    rapidapi_key: Optional[str] = None
    base_url: str = "https://v3.football.api-sports.io"
    
    # League and Season defaults
    league_id_default: int = 39  # EPL
    season_default: int = 2025
    
    # Database Configuration
    database_url: str = "epl_defense.db"
    
    # Cache Configuration
    cache_ttl_default: int = 3600  # 1 hour
    
    # Ingestion Configuration
    ingestion_batch_size: int = 100
    ingestion_rate_limit_delay: float = 1.0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load from environment variables
        self.api_key = os.getenv("APIFOOTBALL_API_KEY")
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        self.league_id_default = int(os.getenv("LEAGUE_ID", "39"))
        self.season_default = int(os.getenv("SEASON_DEFAULT", "2025"))
        self.database_url = os.getenv("DATABASE_URL", "epl_defense.db")
        self.ingestion_batch_size = int(os.getenv("INGESTION_BATCH_SIZE", "100"))
        self.ingestion_rate_limit_delay = float(os.getenv("INGESTION_RATE_LIMIT_DELAY", "1.0"))
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


