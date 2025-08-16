from __future__ import annotations

from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Player(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    firstname: Mapped[str | None] = mapped_column(String(64))
    lastname: Mapped[str | None] = mapped_column(String(64))
    age: Mapped[int | None] = mapped_column(Integer)
    birth_date: Mapped[str | None] = mapped_column(String(10))  # YYYY-MM-DD
    birth_place: Mapped[str | None] = mapped_column(String(128))
    birth_country: Mapped[str | None] = mapped_column(String(64))
    nationality: Mapped[str | None] = mapped_column(String(64))
    height: Mapped[str | None] = mapped_column(String(16))  # e.g., "188 cm"
    weight: Mapped[str | None] = mapped_column(String(16))  # e.g., "76 kg"
    injured: Mapped[bool] = mapped_column(Boolean, default=False)
    photo: Mapped[str | None] = mapped_column(Text)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    league_id: Mapped[int] = mapped_column(Integer, ForeignKey("league.id"), nullable=False)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[str | None] = mapped_column(String(32))
    number: Mapped[int | None] = mapped_column(Integer)
    captain: Mapped[bool] = mapped_column(Boolean, default=False)
    appearances: Mapped[int] = mapped_column(Integer, default=0)
    lineups: Mapped[int] = mapped_column(Integer, default=0)
    minutes: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float | None] = mapped_column(String(8))  # Store as string to handle nulls
    goals: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    yellow_cards: Mapped[int] = mapped_column(Integer, default=0)
    red_cards: Mapped[int] = mapped_column(Integer, default=0)
    shots_total: Mapped[int] = mapped_column(Integer, default=0)
    shots_on_target: Mapped[int] = mapped_column(Integer, default=0)
    passes_total: Mapped[int] = mapped_column(Integer, default=0)
    passes_accuracy: Mapped[int] = mapped_column(Integer, default=0)
    tackles_total: Mapped[int] = mapped_column(Integer, default=0)
    blocks_total: Mapped[int] = mapped_column(Integer, default=0)
    interceptions_total: Mapped[int] = mapped_column(Integer, default=0)
    duels_total: Mapped[int] = mapped_column(Integer, default=0)
    duels_won: Mapped[int] = mapped_column(Integer, default=0)
    dribbles_attempts: Mapped[int] = mapped_column(Integer, default=0)
    dribbles_success: Mapped[int] = mapped_column(Integer, default=0)
    fouls_drawn: Mapped[int] = mapped_column(Integer, default=0)
    fouls_committed: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="players")
    league = relationship("League")
