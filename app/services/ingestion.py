from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.session import SessionLocal
from app.models import League, Team, Venue, Player, Fixture
from app.services.api_client import ApiClientV3
from app.config import get_settings

logger = logging.getLogger(__name__)


class DataIngestionService:
    """Service for ingesting data from API-Football into local database."""
    
    def __init__(self):
        self.api_client = ApiClientV3()
        self.settings = get_settings()
    
    def get_db(self) -> Session:
        """Get database session."""
        return SessionLocal()
    
    async def ingest_league_data(self, league_id: int, season: int) -> Dict[str, Any]:
        """Ingest all data for a specific league and season."""
        logger.info(f"Starting ingestion for league {league_id}, season {season}")
        
        try:
            # 1. Ingest league information
            league_data = await self._ingest_league(league_id, season)
            
            # 2. Ingest teams
            teams_data = await self._ingest_teams(league_id, season)
            
            # 3. Ingest players (with pagination)
            players_data = await self._ingest_players(league_id, season)
            
            # 4. Ingest fixtures
            fixtures_data = await self._ingest_fixtures(league_id, season)
            
            return {
                "league": league_data,
                "teams": teams_data,
                "players": players_data,
                "fixtures": fixtures_data,
                "ingestion_time": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
            raise
    
    async def _ingest_league(self, league_id: int, season: int) -> Dict[str, Any]:
        """Ingest league information."""
        logger.info(f"Ingesting league {league_id} for season {season}")
        
        try:
            # Get league data from API
            response = self.api_client.get("/leagues", params={"id": league_id})
            logger.info(f"API Response: {response}")
            
            league_info = response.get("response", [{}])[0]
            logger.info(f"League info: {league_info}")
            
            # Validate required fields
            if not league_info:
                raise ValueError(f"No league data returned for ID {league_id}")
            
            # Extract league name with fallback
            league_name = league_info.get("name")
            if not league_name:
                logger.warning(f"League name is None for ID {league_id}, using fallback")
                league_name = f"League {league_id}"  # Fallback name
            
            db = self.get_db()
            
            # Check if league already exists
            existing_league = db.query(League).filter(
                and_(League.id == league_id, League.season == season)
            ).first()
            
            if existing_league:
                # Update existing league
                logger.info(f"Updating existing league {league_id}")
                for key, value in league_info.items():
                    if hasattr(existing_league, key):
                        setattr(existing_league, key, value)
                existing_league.name = league_name  # Ensure name is set
                existing_league.updated_at = datetime.utcnow()
                league = existing_league
            else:
                # Create new league
                logger.info(f"Creating new league {league_id}: {league_name}")
                league = League(
                    id=league_id,
                    name=league_name,
                    type=league_info.get("type"),
                    country=league_info.get("country", {}).get("name"),
                    country_code=league_info.get("country", {}).get("code"),
                    logo=league_info.get("logo"),
                    flag=league_info.get("flag"),
                    season=season,
                    season_start=league_info.get("seasons", [{}])[0].get("start"),
                    season_end=league_info.get("seasons", [{}])[0].get("end"),
                    is_current=league_info.get("seasons", [{}])[0].get("current", False),
                    coverage=json.dumps(league_info.get("coverage", {}))
                )
                db.add(league)
            
            db.commit()
            db.refresh(league)
            
            logger.info(f"League {league_id} ingested successfully: {league.name}")
            return {"id": league.id, "name": league.name, "teams_count": 0}
            
        except Exception as e:
            logger.error(f"Error ingesting league: {e}")
            if 'db' in locals():
                db.rollback()
            raise
        finally:
            if 'db' in locals():
                db.close()
    
    async def _ingest_teams(self, league_id: int, season: int) -> Dict[str, Any]:
        """Ingest all teams for a league/season."""
        logger.info(f"Ingesting teams for league {league_id}, season {season}")
        
        try:
            # Get teams from API
            response = self.api_client.get("/teams", params={
                "league": league_id,
                "season": season
            })
            
            teams = response.get("response", [])
            logger.info(f"Found {len(teams)} teams to ingest")
            
            db = self.get_db()
            ingested_teams = []
            
            for team_data in teams:
                team_info = team_data.get("team", {})
                venue_info = team_data.get("venue", {})
                
                # Check if team already exists for this season
                existing_team = db.query(Team).filter(
                    and_(Team.id == team_info.get("id"), Team.season == season)
                ).first()
                
                if existing_team:
                    # Update existing team
                    for key, value in team_info.items():
                        if hasattr(existing_team, key) and key != "id":
                            setattr(existing_team, key, value)
                    existing_team.updated_at = datetime.utcnow()
                    team = existing_team
                else:
                    # Create new team
                    team = Team(
                        id=team_info.get("id"),
                        name=team_info.get("name"),
                        code=team_info.get("code"),
                        country=team_info.get("country"),
                        founded=team_info.get("founded"),
                        national=team_info.get("national", False),
                        logo=team_info.get("logo"),
                        league_id=league_id,
                        season=season
                    )
                    db.add(team)
                    db.flush()  # Get the team ID
                
                # Handle venue
                if venue_info:
                    existing_venue = db.query(Venue).filter(
                        Venue.team_id == team.id
                    ).first()
                    
                    if existing_venue:
                        # Update existing venue
                        for key, value in venue_info.items():
                            if hasattr(existing_venue, key) and key != "id":
                                setattr(existing_venue, key, value)
                    else:
                        # Create new venue
                        venue = Venue(
                            id=venue_info.get("id"),
                            name=venue_info.get("name"),
                            address=venue_info.get("address"),
                            city=venue_info.get("city"),
                            capacity=venue_info.get("capacity"),
                            surface=venue_info.get("surface"),
                            image=venue_info.get("image"),
                            team_id=team.id
                        )
                        db.add(venue)
                
                ingested_teams.append(team.id)
            
            db.commit()
            logger.info(f"Successfully ingested {len(ingested_teams)} teams")
            
            return {
                "total_teams": len(teams),
                "ingested_teams": len(ingested_teams),
                "team_ids": ingested_teams
            }
            
        except Exception as e:
            logger.error(f"Error ingesting teams: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    async def _ingest_players(self, league_id: int, season: int) -> Dict[str, Any]:
        """Ingest all players for a league/season with pagination."""
        logger.info(f"Ingesting players for league {league_id}, season {season}")
        
        try:
            db = self.get_db()
            all_players = []
            page = 1
            total_pages = 1
            
            while page <= total_pages:
                logger.info(f"Fetching players page {page}")
                
                # Get players from API with pagination
                response = self.api_client.get("/players", params={
                    "league": league_id,
                    "season": season,
                    "page": page
                })
                
                players = response.get("response", [])
                paging = response.get("paging", {})
                
                if page == 1:
                    total_pages = paging.get("total", 1)
                    logger.info(f"Total pages to fetch: {total_pages}")
                
                logger.info(f"Page {page}: Found {len(players)} players")
                
                for player_data in players:
                    player_info = player_data.get("player", {})
                    stats = player_data.get("statistics", [{}])[0]
                    
                    # Check if player already exists for this team/season
                    existing_player = db.query(Player).filter(
                        and_(
                            Player.id == player_info.get("id"),
                            Player.team_id == stats.get("team", {}).get("id"),
                            Player.season == season
                        )
                    ).first()
                    
                    if existing_player:
                        # Update existing player
                        self._update_player_data(existing_player, player_info, stats)
                        existing_player.updated_at = datetime.utcnow()
                        player = existing_player
                    else:
                        # Create new player
                        player = Player(
                            id=player_info.get("id"),
                            name=player_info.get("name"),
                            firstname=player_info.get("firstname"),
                            lastname=player_info.get("lastname"),
                            age=player_info.get("age"),
                            birth_date=player_info.get("birth", {}).get("date"),
                            birth_place=player_info.get("birth", {}).get("place"),
                            birth_country=player_info.get("birth", {}).get("country"),
                            nationality=player_info.get("nationality"),
                            height=player_info.get("height"),
                            weight=player_info.get("weight"),
                            injured=player_info.get("injured", False),
                            photo=player_info.get("photo"),
                            team_id=stats.get("team", {}).get("id"),
                            league_id=league_id,
                            season=season,
                            position=stats.get("games", {}).get("position"),
                            number=stats.get("games", {}).get("number"),
                            captain=stats.get("games", {}).get("captain", False),
                            appearances=stats.get("games", {}).get("appearences", 0),
                            lineups=stats.get("games", {}).get("lineups", 0),
                            minutes=stats.get("games", {}).get("minutes", 0),
                            rating=str(stats.get("games", {}).get("rating")) if stats.get("games", {}).get("rating") else None,
                            goals=stats.get("goals", {}).get("total", 0),
                            assists=stats.get("goals", {}).get("assists", 0),
                            yellow_cards=stats.get("cards", {}).get("yellow", 0),
                            red_cards=stats.get("cards", {}).get("red", 0),
                            shots_total=stats.get("shots", {}).get("total", 0),
                            shots_on_target=stats.get("shots", {}).get("on", 0),
                            passes_total=stats.get("passes", {}).get("total", 0),
                            passes_accuracy=stats.get("passes", {}).get("accuracy", 0),
                            tackles_total=stats.get("tackles", {}).get("total", 0),
                            blocks_total=stats.get("tackles", {}).get("blocks", 0),
                            interceptions_total=stats.get("tackles", {}).get("interceptions", 0),
                            duels_total=stats.get("duels", {}).get("total", 0),
                            duels_won=stats.get("duels", {}).get("won", 0),
                            dribbles_attempts=stats.get("dribbles", {}).get("attempts", 0),
                            dribbles_success=stats.get("dribbles", {}).get("success", 0),
                            fouls_drawn=stats.get("fouls", {}).get("drawn", 0),
                            fouls_committed=stats.get("fouls", {}).get("committed", 0)
                        )
                        db.add(player)
                    
                    all_players.append(player.id)
                
                page += 1
                
                # Rate limiting: sleep every other page to avoid hitting limits
                if page % 2 == 1 and page < total_pages:
                    await asyncio.sleep(1)
            
            db.commit()
            logger.info(f"Successfully ingested {len(all_players)} players")
            
            return {
                "total_players": len(all_players),
                "ingested_players": len(all_players),
                "player_ids": all_players
            }
            
        except Exception as e:
            logger.error(f"Error ingesting players: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    def _update_player_data(self, player: Player, player_info: Dict, stats: Dict) -> None:
        """Update existing player with new data."""
        # Update basic info
        for key, value in player_info.items():
            if hasattr(player, key) and key != "id":
                setattr(player, key, value)
        
        # Update statistics
        if stats.get("games"):
            games = stats["games"]
            if hasattr(player, "position"):
                player.position = games.get("position")
            if hasattr(player, "number"):
                player.number = games.get("number")
            if hasattr(player, "captain"):
                player.captain = games.get("captain", False)
            if hasattr(player, "appearances"):
                player.appearances = games.get("appearences", 0)
            if hasattr(player, "lineups"):
                player.lineups = games.get("lineups", 0)
            if hasattr(player, "minutes"):
                player.minutes = games.get("minutes", 0)
            if hasattr(player, "rating"):
                player.rating = str(games.get("rating")) if games.get("rating") else None
        
        # Update goals and cards
        if stats.get("goals"):
            goals = stats["goals"]
            if hasattr(player, "goals"):
                player.goals = goals.get("total", 0)
            if hasattr(player, "assists"):
                player.assists = goals.get("assists", 0)
        
        if stats.get("cards"):
            cards = stats["cards"]
            if hasattr(player, "yellow_cards"):
                player.yellow_cards = cards.get("yellow", 0)
            if hasattr(player, "red_cards"):
                player.red_cards = cards.get("red", 0)
    
    async def _ingest_fixtures(self, league_id: int, season: int) -> Dict[str, Any]:
        """Ingest fixtures for a league/season."""
        logger.info(f"Ingesting fixtures for league {league_id}, season {season}")
        
        try:
            # Get fixtures from API
            response = self.api_client.get("/fixtures", params={
                "league": league_id,
                "season": season
            })
            
            fixtures = response.get("response", [])
            logger.info(f"Found {len(fixtures)} fixtures to ingest")
            
            db = self.get_db()
            ingested_fixtures = []
            
            for fixture_data in fixtures:
                fixture_info = fixture_data.get("fixture", {})
                teams_info = fixture_data.get("teams", {})
                goals_info = fixture_data.get("goals", {})
                score_info = fixture_data.get("score", {})
                
                # Check if fixture already exists
                existing_fixture = db.query(Fixture).filter(
                    Fixture.id == fixture_info.get("id")
                ).first()
                
                if existing_fixture:
                    # Update existing fixture
                    self._update_fixture_data(existing_fixture, fixture_info, teams_info, goals_info, score_info)
                    existing_fixture.updated_at = datetime.utcnow()
                    fixture = existing_fixture
                else:
                    # Create new fixture
                    fixture = Fixture(
                        id=fixture_info.get("id"),
                        date=datetime.fromisoformat(fixture_info.get("date").replace("Z", "+00:00")),
                        timestamp=fixture_info.get("timestamp"),
                        timezone=fixture_info.get("timezone"),
                        status_short=fixture_info.get("status", {}).get("short"),
                        status_long=fixture_info.get("status", {}).get("long"),
                        elapsed=fixture_info.get("status", {}).get("elapsed"),
                        home_team_id=teams_info.get("home", {}).get("id"),
                        away_team_id=teams_info.get("away", {}).get("id"),
                        league_id=league_id,
                        season=season,
                        round=fixture_data.get("league", {}).get("round"),
                        referee=fixture_data.get("league", {}).get("referee"),
                        goals_home=goals_info.get("home"),
                        goals_away=goals_info.get("away"),
                        score_halftime_home=score_info.get("halftime", {}).get("home"),
                        score_halftime_away=score_info.get("halftime", {}).get("away"),
                        score_fulltime_home=score_info.get("fulltime", {}).get("home"),
                        score_fulltime_away=score_info.get("fulltime", {}).get("away"),
                        score_extratime_home=score_info.get("extratime", {}).get("home"),
                        score_extratime_away=score_info.get("extratime", {}).get("away"),
                        score_penalty_home=score_info.get("penalty", {}).get("home"),
                        score_penalty_away=score_info.get("penalty", {}).get("away")
                    )
                    db.add(fixture)
                
                ingested_fixtures.append(fixture.id)
            
            db.commit()
            logger.info(f"Successfully ingested {len(ingested_fixtures)} fixtures")
            
            return {
                "total_fixtures": len(fixtures),
                "ingested_fixtures": len(ingested_fixtures),
                "fixture_ids": ingested_fixtures
            }
            
        except Exception as e:
            logger.error(f"Error ingesting fixtures: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    def _update_fixture_data(self, fixture: Fixture, fixture_info: Dict, teams_info: Dict, goals_info: Dict, score_info: Dict) -> None:
        """Update existing fixture with new data."""
        # Update fixture status and scores
        if fixture_info.get("status"):
            status = fixture_info["status"]
            if hasattr(fixture, "status_short"):
                fixture.status_short = status.get("short")
            if hasattr(fixture, "status_long"):
                fixture.status_long = status.get("long")
            if hasattr(fixture, "elapsed"):
                fixture.elapsed = status.get("elapsed")
        
        # Update goals
        if hasattr(fixture, "goals_home"):
            fixture.goals_home = goals_info.get("home")
        if hasattr(fixture, "goals_away"):
            fixture.goals_away = goals_info.get("away")
        
        # Update scores
        if score_info.get("halftime"):
            halftime = score_info["halftime"]
            if hasattr(fixture, "score_halftime_home"):
                fixture.score_halftime_home = halftime.get("home")
            if hasattr(fixture, "score_halftime_away"):
                fixture.score_halftime_away = halftime.get("away")
        
        if score_info.get("fulltime"):
            fulltime = score_info["fulltime"]
            if hasattr(fixture, "score_fulltime_home"):
                fixture.score_fulltime_home = fulltime.get("home")
            if hasattr(fixture, "score_fulltime_away"):
                fixture.score_fulltime_away = fulltime.get("away")
    
    async def get_ingestion_status(self, league_id: int, season: int) -> Dict[str, Any]:
        """Get the current ingestion status for a league/season."""
        db = self.get_db()
        
        try:
            league_count = db.query(League).filter(
                and_(League.id == league_id, League.season == season)
            ).count()
            
            team_count = db.query(Team).filter(
                and_(Team.league_id == league_id, Team.season == season)
            ).count()
            
            player_count = db.query(Player).filter(
                and_(Player.league_id == league_id, Player.season == season)
            ).count()
            
            fixture_count = db.query(Fixture).filter(
                and_(Fixture.league_id == league_id, Fixture.season == season)
            ).count()
            
            return {
                "league_id": league_id,
                "season": season,
                "has_league": league_count > 0,
                "teams_count": team_count,
                "players_count": player_count,
                "fixtures_count": fixture_count,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        finally:
            db.close()
