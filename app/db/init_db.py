from __future__ import annotations

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.models.base import Base
from app.models import League, Team, Venue, Player, Fixture, FixtureEvent, FixtureLineup, FixtureLineupPlayer, FixtureStatistics

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the database with all tables."""
    settings = get_settings()
    
    # Create SQLite database URL
    database_url = f"sqlite:///{settings.database_url}"
    
    logger.info(f"Initializing database: {database_url}")
    
    # Create engine
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database tables created successfully")
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return SessionLocal


def drop_db() -> None:
    """Drop all database tables (use with caution!)."""
    settings = get_settings()
    database_url = f"sqlite:///{settings.database_url}"
    
    logger.warning(f"Dropping all tables from database: {database_url}")
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )
    
    Base.metadata.drop_all(bind=engine)
    
    logger.info("All database tables dropped successfully")


if __name__ == "__main__":
    # Initialize database when run directly
    init_db()
