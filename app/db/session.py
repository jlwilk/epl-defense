from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings

settings = get_settings()

# Create SQLite database URL if it's just a filename
database_url = f"sqlite:///{settings.database_url}" if not settings.database_url.startswith(("sqlite://", "postgresql://", "mysql://")) else settings.database_url

engine = create_engine(
    database_url,
    future=True,
    echo=False,  # Set to True for SQL debugging if needed
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


