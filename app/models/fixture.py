from __future__ import annotations

from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Fixture(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer)  # Unix timestamp
    timezone: Mapped[str | None] = mapped_column(String(32))
    status_short: Mapped[str | None] = mapped_column(String(8))  # TBD, NS, 1H, HT, 2H, FT, etc.
    status_long: Mapped[str | None] = mapped_column(String(32))
    elapsed: Mapped[int | None] = mapped_column(Integer)  # Minutes elapsed in match
    home_team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    league_id: Mapped[int] = mapped_column(Integer, ForeignKey("league.id"), nullable=False)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    round: Mapped[str | None] = mapped_column(String(64))
    venue_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("venue.id"))
    referee: Mapped[str | None] = mapped_column(String(128))
    goals_home: Mapped[int | None] = mapped_column(Integer)
    goals_away: Mapped[int | None] = mapped_column(Integer)
    score_halftime_home: Mapped[int | None] = mapped_column(Integer)
    score_halftime_away: Mapped[int | None] = mapped_column(Integer)
    score_fulltime_home: Mapped[int | None] = mapped_column(Integer)
    score_fulltime_away: Mapped[int | None] = mapped_column(Integer)
    score_extratime_home: Mapped[int | None] = mapped_column(Integer)
    score_extratime_away: Mapped[int | None] = mapped_column(Integer)
    score_penalty_home: Mapped[int | None] = mapped_column(Integer)
    score_penalty_away: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_fixtures")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_fixtures")
    league = relationship("League", back_populates="fixtures")
    venue = relationship("Venue")
    events = relationship("FixtureEvent", back_populates="fixture")
    lineups = relationship("FixtureLineup", back_populates="fixture")
    statistics = relationship("FixtureStatistics", back_populates="fixture")


class FixtureEvent(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fixture_id: Mapped[int] = mapped_column(Integer, ForeignKey("fixture.id"), nullable=False)
    time_elapsed: Mapped[int | None] = mapped_column(Integer)
    time_extra: Mapped[int | None] = mapped_column(Integer)
    team_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("team.id"))
    player_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("player.id"))
    assist_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("player.id"))
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # Goal, Card, Subst, etc.
    detail: Mapped[str | None] = mapped_column(String(64))  # Normal Goal, Yellow Card, etc.
    comments: Mapped[str | None] = mapped_column(Text)
    
    # Relationships
    fixture = relationship("Fixture", back_populates="events")
    team = relationship("Team")
    player = relationship("Player", foreign_keys=[player_id])
    assist = relationship("Player", foreign_keys=[assist_id])


class FixtureLineup(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fixture_id: Mapped[int] = mapped_column(Integer, ForeignKey("fixture.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    formation: Mapped[str | None] = mapped_column(String(16))  # e.g., "4-3-3"
    coach_id: Mapped[int | None] = mapped_column(Integer)
    coach_name: Mapped[str | None] = mapped_column(String(128))
    
    # Relationships
    fixture = relationship("Fixture", back_populates="lineups")
    team = relationship("Team")
    players = relationship("FixtureLineupPlayer", back_populates="lineup")


class FixtureLineupPlayer(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lineup_id: Mapped[int] = mapped_column(Integer, ForeignKey("fixturelineup.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), nullable=False)
    position: Mapped[str | None] = mapped_column(String(32))  # GK, DEF, MID, FWD
    grid: Mapped[str | None] = mapped_column(String(8))  # Position on field
    number: Mapped[int | None] = mapped_column(Integer)
    is_starter: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    lineup = relationship("FixtureLineup", back_populates="players")
    player = relationship("Player")


class FixtureStatistics(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fixture_id: Mapped[int] = mapped_column(Integer, ForeignKey("fixture.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    shots_on_goal: Mapped[int | None] = mapped_column(Integer)
    shots_off_goal: Mapped[int | None] = mapped_column(Integer)
    total_shots: Mapped[int | None] = mapped_column(Integer)
    blocked_shots: Mapped[int | None] = mapped_column(Integer)
    shots_inside_box: Mapped[int | None] = mapped_column(Integer)
    shots_outside_box: Mapped[int | None] = mapped_column(Integer)
    fouls: Mapped[int | None] = mapped_column(Integer)
    corner_kicks: Mapped[int | None] = mapped_column(Integer)
    offsides: Mapped[int | None] = mapped_column(Integer)
    ball_possession: Mapped[int | None] = mapped_column(Integer)  # Percentage
    yellow_cards: Mapped[int | None] = mapped_column(Integer)
    red_cards: Mapped[int | None] = mapped_column(Integer)
    goalkeeper_saves: Mapped[int | None] = mapped_column(Integer)
    total_passes: Mapped[int | None] = mapped_column(Integer)
    passes_accurate: Mapped[int | None] = mapped_column(Integer)
    passes_percentage: Mapped[int | None] = mapped_column(Integer)
    
    # Relationships
    fixture = relationship("Fixture", back_populates="statistics")
    team = relationship("Team")
