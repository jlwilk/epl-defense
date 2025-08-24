from __future__ import annotations

from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class League(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)  # Made nullable
    type: Mapped[str | None] = mapped_column(String(32))
    country: Mapped[str | None] = mapped_column(String(64))
    country_code: Mapped[str | None] = mapped_column(String(3))
    logo: Mapped[str | None] = mapped_column(Text)
    flag: Mapped[str | None] = mapped_column(Text)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    season_start: Mapped[str | None] = mapped_column(String(10))  # YYYY-MM-DD
    season_end: Mapped[str | None] = mapped_column(String(10))    # YYYY-MM-DD
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    coverage: Mapped[str | None] = mapped_column(Text)  # JSON string of coverage data
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    
    # Relationships
    teams = relationship("Team", back_populates="league")
    fixtures = relationship("Fixture", back_populates="league")


