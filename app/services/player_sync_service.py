from __future__ import annotations

import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.player import Player
from app.models.team import Team
from app.models.league import League
from app.services.api_client import ApiClientV3

logger = logging.getLogger(__name__)


class PlayerSyncService:
    """Service for syncing player data from API-Football to local database."""
    
    def __init__(self):
        self.api_client = ApiClientV3()
    
    def sync_league_players(self, league_id: int, season: int, db: Session) -> Dict[str, Any]:
        """
        Sync all players for a specific league and season.
        
        Args:
            league_id: The league ID
            season: The season year
            db: Database session
            
        Returns:
            Dictionary with sync results
        """
        logger.info(f"Starting sync for league {league_id}, season {season}")
        
        try:
            # Get total pages from first API call
            first_page = self.api_client.get_player_statistics_by_league(league_id, season)
            total_pages = first_page.get("paging", {}).get("total", 1)
            
            total_players = 0
            new_players = 0
            updated_players = 0
            errors = 0
            
            # Sync all pages
            for page in range(1, total_pages + 1):
                logger.info(f"Syncing page {page}/{total_pages}")
                
                try:
                    page_data = self.api_client.get_player_statistics_by_league(league_id, season, page=page)
                    players_data = page_data.get("response", [])
                    
                    for player_data in players_data:
                        try:
                            result = self._sync_single_player(player_data, league_id, season, db)
                            if result == "new":
                                new_players += 1
                            elif result == "updated":
                                updated_players += 1
                            total_players += 1
                        except Exception as e:
                            logger.error(f"Error syncing player {player_data.get('player', {}).get('id')}: {e}")
                            errors += 1
                            
                except Exception as e:
                    logger.error(f"Error syncing page {page}: {e}")
                    errors += 1
                    continue
            
            # Commit all changes
            db.commit()
            
            logger.info(f"Sync completed: {total_players} total, {new_players} new, {updated_players} updated, {errors} errors")
            
            return {
                "success": True,
                "total_players": total_players,
                "new_players": new_players,
                "updated_players": updated_players,
                "errors": errors,
                "league_id": league_id,
                "season": season
            }
            
        except Exception as e:
            logger.error(f"Error during league sync: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "league_id": league_id,
                "season": season
            }
    
    def sync_team_players(self, team_id: int, season: int, league_id: int | None, db: Session) -> Dict[str, Any]:
        """
        Sync all players for a specific team and season.
        
        Args:
            team_id: The team ID
            season: The season year
            league_id: Optional league ID to filter by
            db: Database session
            
        Returns:
            Dictionary with sync results
        """
        logger.info(f"Starting team sync for team {team_id}, season {season}")
        
        try:
            # Get total pages from first API call
            first_page = self.api_client.get_player_statistics_by_team(team_id, season, league_id)
            total_pages = first_page.get("paging", {}).get("total", 1)
            
            total_players = 0
            new_players = 0
            updated_players = 0
            errors = 0
            
            # Sync all pages
            for page in range(1, total_pages + 1):
                logger.info(f"Syncing team page {page}/{total_pages}")
                
                try:
                    page_data = self.api_client.get_player_statistics_by_team(team_id, season, league_id, page=page)
                    players_data = page_data.get("response", [])
                    
                    for player_data in players_data:
                        try:
                            # For team sync, we need to determine the league from the data
                            player_league_id = league_id
                            if not player_league_id:
                                stats = player_data.get("statistics", [{}])[0] if player_data.get("statistics") else {}
                                player_league_id = stats.get("league", {}).get("id")
                            
                            if player_league_id:
                                result = self._sync_single_player(player_data, player_league_id, season, db)
                                if result == "new":
                                    new_players += 1
                                elif result == "updated":
                                    updated_players += 1
                                total_players += 1
                            else:
                                logger.warning(f"Could not determine league for player {player_data.get('player', {}).get('id')}")
                                errors += 1
                                
                        except Exception as e:
                            logger.error(f"Error syncing team player {player_data.get('player', {}).get('id')}: {e}")
                            errors += 1
                            
                except Exception as e:
                    logger.error(f"Error syncing team page {page}: {e}")
                    errors += 1
                    continue
            
            # Commit all changes
            db.commit()
            
            logger.info(f"Team sync completed: {total_players} total, {new_players} new, {updated_players} updated, {errors} errors")
            
            return {
                "success": True,
                "total_players": total_players,
                "new_players": new_players,
                "updated_players": updated_players,
                "errors": errors,
                "team_id": team_id,
                "season": season,
                "league_id": league_id
            }
            
        except Exception as e:
            logger.error(f"Error during team sync: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "team_id": team_id,
                "season": season,
                "league_id": league_id
            }
    
    def _sync_single_player(self, player_data: Dict[str, Any], league_id: int, season: int, db: Session) -> str:
        """
        Sync a single player's data.
        
        Args:
            player_data: Player data from API
            league_id: League ID
            season: Season year
            db: Database session
            
        Returns:
            "new" if player was created, "updated" if updated
        """
        player_info = player_data.get("player", {})
        stats = player_data.get("statistics", [{}])[0] if player_data.get("statistics") else {}
        
        # Check if player already exists
        existing_player = db.query(Player).filter(
            Player.id == player_info.get("id"),
            Player.league_id == league_id,
            Player.season == season
        ).first()
        
        if existing_player:
            # Update existing player
            self._update_player_data(existing_player, player_info, stats)
            return "updated"
        else:
            # Create new player
            self._create_player_data(player_info, stats, league_id, season, db)
            return "new"
    
    def _create_player_data(self, player_info: Dict[str, Any], stats: Dict[str, Any], league_id: int, season: int, db: Session):
        """Create a new player record."""
        games_stats = stats.get("games", {})
        goals_stats = stats.get("goals", {})
        cards_stats = stats.get("cards", {})
        shots_stats = stats.get("shots", {})
        passes_stats = stats.get("passes", {})
        tackles_stats = stats.get("tackles", {})
        duels_stats = stats.get("duels", {})
        dribbles_stats = stats.get("dribbles", {})
        fouls_stats = stats.get("fouls", {})
        
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
            position=games_stats.get("position"),
            number=games_stats.get("number"),
            captain=games_stats.get("captain", False),
            appearances=games_stats.get("appearences", 0),
            lineups=games_stats.get("lineups", 0),
            minutes=games_stats.get("minutes", 0),
            rating=games_stats.get("rating"),
            goals=goals_stats.get("total", 0),
            assists=goals_stats.get("assists", 0),
            yellow_cards=cards_stats.get("yellow", 0),
            red_cards=cards_stats.get("red", 0),
            shots_total=shots_stats.get("total"),
            shots_on_target=shots_stats.get("on"),
            passes_total=passes_stats.get("total"),
            passes_accuracy=passes_stats.get("accuracy"),
            tackles_total=tackles_stats.get("total"),
            blocks_total=tackles_stats.get("blocks"),
            interceptions_total=tackles_stats.get("interceptions"),
            duels_total=duels_stats.get("total"),
            duels_won=duels_stats.get("won"),
            dribbles_attempts=dribbles_stats.get("attempts"),
            dribbles_success=dribbles_stats.get("success"),
            fouls_drawn=fouls_stats.get("drawn"),
            fouls_committed=fouls_stats.get("committed")
        )
        
        db.add(player)
    
    def _update_player_data(self, player: Player, player_info: Dict[str, Any], stats: Dict[str, Any]):
        """Update an existing player record."""
        # Update basic info only if values are provided
        if player_info.get("name") is not None:
            player.name = player_info.get("name")
        if player_info.get("firstname") is not None:
            player.firstname = player_info.get("firstname")
        if player_info.get("lastname") is not None:
            player.lastname = player_info.get("lastname")
        if player_info.get("age") is not None:
            player.age = player_info.get("age")
        if player_info.get("injured") is not None:
            player.injured = player_info.get("injured")
        if player_info.get("photo") is not None:
            player.photo = player_info.get("photo")
        
        # Update statistics only if values are provided (not None)
        games_stats = stats.get("games", {})
        if games_stats.get("position") is not None:
            player.position = games_stats.get("position")
        if games_stats.get("number") is not None:
            player.number = games_stats.get("number")
        if games_stats.get("captain") is not None:
            player.captain = games_stats.get("captain")
        if games_stats.get("appearences") is not None:
            player.appearances = games_stats.get("appearences")
        if games_stats.get("lineups") is not None:
            player.lineups = games_stats.get("lineups")
        if games_stats.get("minutes") is not None:
            player.minutes = games_stats.get("minutes")
        if games_stats.get("rating") is not None:
            player.rating = games_stats.get("rating")
        
        goals_stats = stats.get("goals", {})
        if goals_stats.get("total") is not None:
            player.goals = goals_stats.get("total")
        if goals_stats.get("assists") is not None:
            player.assists = goals_stats.get("assists")
        
        cards_stats = stats.get("cards", {})
        if cards_stats.get("yellow") is not None:
            player.yellow_cards = cards_stats.get("yellow")
        if cards_stats.get("red") is not None:
            player.red_cards = cards_stats.get("red")
        
        shots_stats = stats.get("shots", {})
        if shots_stats.get("total") is not None:
            player.shots_total = shots_stats.get("total")
        if shots_stats.get("on") is not None:
            player.shots_on_target = shots_stats.get("on")
        
        passes_stats = stats.get("passes", {})
        if passes_stats.get("total") is not None:
            player.passes_total = passes_stats.get("total")
        if passes_stats.get("accuracy") is not None:
            player.passes_accuracy = passes_stats.get("accuracy")
        
        tackles_stats = stats.get("tackles", {})
        if tackles_stats.get("total") is not None:
            player.tackles_total = tackles_stats.get("total")
        if tackles_stats.get("blocks") is not None:
            player.blocks_total = tackles_stats.get("blocks")
        if tackles_stats.get("interceptions") is not None:
            player.interceptions_total = tackles_stats.get("interceptions")
        
        duels_stats = stats.get("duels", {})
        if duels_stats.get("total") is not None:
            player.duels_total = duels_stats.get("total")
        if duels_stats.get("won") is not None:
            player.duels_won = duels_stats.get("won")
        
        dribbles_stats = stats.get("dribbles", {})
        if dribbles_stats.get("attempts") is not None:
            player.dribbles_attempts = dribbles_stats.get("attempts")
        if dribbles_stats.get("success") is not None:
            player.dribbles_success = dribbles_stats.get("success")
        
        fouls_stats = stats.get("fouls", {})
        if fouls_stats.get("drawn") is not None:
            player.fouls_drawn = fouls_stats.get("drawn")
        if fouls_stats.get("committed") is not None:
            player.fouls_committed = fouls_stats.get("committed")
    
    def get_cached_league_data(self, league_id: int, season: int, page: int = 1, limit: int = 20, db: Session = None, 
                               team_filter: int | None = None, position_filter: str | None = None, 
                               sort_by: str = "lastname", sort_order: str = "asc") -> Optional[Dict[str, Any]]:
        """
        Get league player data from database with filtering and sorting.
        
        Args:
            league_id: League ID
            season: Season year
            page: Page number
            limit: Players per page
            db: Database session
            team_filter: Optional team ID filter
            position_filter: Optional position filter
            sort_by: Sort field
            sort_order: Sort order ('asc' or 'desc')
            
        Returns:
            Cached data or None if not available
        """
        if db is None:
            db = next(get_db())
            should_close = True
        else:
            should_close = False
            
        try:
            # Build base query
            query = db.query(Player).filter(
                Player.league_id == league_id,
                Player.season == season
            )
            
            # Apply filters
            if team_filter:
                query = query.filter(Player.team_id == team_filter)
            if position_filter:
                query = query.filter(Player.position == position_filter)
            
            # Get total count before sorting and pagination
            total_count = query.count()
            
            # Apply sorting BEFORE pagination to ensure correct order
            if sort_by == "lastname":
                if sort_order == "desc":
                    query = query.order_by(Player.lastname.desc().nullslast())
                else:
                    query = query.order_by(Player.lastname.asc().nullslast())
            elif sort_by == "firstname":
                if sort_order == "desc":
                    query = query.order_by(Player.firstname.desc().nullslast())
                else:
                    query = query.order_by(Player.firstname.asc().nullslast())
            elif sort_by == "name":
                if sort_order == "desc":
                    query = query.order_by(Player.name.desc().nullslast())
                else:
                    query = query.order_by(Player.name.asc().nullslast())
            elif sort_by == "age":
                if sort_order == "desc":
                    query = query.order_by(Player.age.desc().nullslast())
                else:
                    query = query.order_by(Player.age.asc().nullslast())
            elif sort_by == "goals":
                if sort_order == "desc":
                    query = query.order_by(Player.goals.desc().nullslast())
                else:
                    query = query.order_by(Player.goals.asc().nullslast())
            elif sort_by == "assists":
                if sort_order == "desc":
                    query = query.order_by(Player.assists.desc().nullslast())
                else:
                    query = query.order_by(Player.assists.asc().nullslast())
            elif sort_by == "rating":
                if sort_order == "desc":
                    query = query.order_by(Player.rating.desc().nullslast())
                else:
                    query = query.order_by(Player.rating.asc().nullslast())
            else:
                # Default to lastname asc
                query = query.order_by(Player.lastname.asc().nullslast())
            
            # Apply pagination AFTER sorting
            offset = (page - 1) * limit
            players = query.offset(offset).limit(limit).all()
            
            if not players:
                return None
            
            # Convert to API-like format
            response = []
            for player in players:
                player_data = {
                    "player": {
                        "id": player.id,
                        "name": player.name,
                        "firstname": player.firstname,
                        "lastname": player.lastname,
                        "age": player.age,
                        "birth": {
                            "date": player.birth_date,
                            "place": player.birth_place,
                            "country": player.birth_country
                        },
                        "nationality": player.nationality,
                        "height": player.height,
                        "weight": player.weight,
                        "injured": player.injured,
                        "photo": player.photo
                    },
                    "statistics": [{
                        "team": {
                            "id": player.team_id,
                            "name": player.team.name if player.team else None
                        },
                        "league": {
                            "id": player.league_id,
                            "name": player.league.name if player.league else None
                        },
                        "games": {
                            "position": player.position,
                            "number": player.number,
                            "captain": player.captain,
                            "appearences": player.appearances,
                            "lineups": player.lineups,
                            "minutes": player.minutes,
                            "rating": player.rating
                        },
                        "goals": {
                            "total": player.goals,
                            "assists": player.assists
                        },
                        "cards": {
                            "yellow": player.yellow_cards,
                            "red": player.red_cards
                        },
                        "shots": {
                            "total": player.shots_total,
                            "on": player.shots_on_target
                        },
                        "passes": {
                            "total": player.passes_total,
                            "accuracy": player.passes_accuracy
                        },
                        "tackles": {
                            "total": player.tackles_total,
                            "blocks": player.blocks_total,
                            "interceptions": player.interceptions_total
                        },
                        "duels": {
                            "total": player.duels_total,
                            "won": player.duels_won
                        },
                        "dribbles": {
                            "attempts": player.dribbles_attempts,
                            "success": player.dribbles_success
                        },
                        "fouls": {
                            "drawn": player.fouls_drawn,
                            "committed": player.fouls_committed
                        }
                    }]
                }
                response.append(player_data)
            
            # Build parameters
            parameters = {
                "league": str(league_id),
                "season": str(season),
                "page": str(page)
            }
            if team_filter:
                parameters["team"] = str(team_filter)
            if position_filter:
                parameters["position"] = position_filter
            if sort_by:
                parameters["sort_by"] = sort_by
            if sort_order:
                parameters["sort_order"] = sort_order
            
            return {
                "get": "players",
                "parameters": parameters,
                "errors": [],
                "results": total_count,
                "paging": {
                    "current": page,
                    "total": (total_count + limit - 1) // limit
                },
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error getting cached data: {e}")
            return None
        finally:
            if should_close:
                db.close()
    
    def get_cached_team_data(self, team_id: int, season: int, league_id: int | None, page: int = 1, limit: int = 20, db: Session = None,
                             position_filter: str | None = None, sort_by: str = "lastname", sort_order: str = "asc") -> Optional[Dict[str, Any]]:
        """
        Get team player data from database with filtering and sorting.
        
        Args:
            team_id: Team ID
            season: Season year
            league_id: Optional league ID
            page: Page number
            limit: Players per page
            db: Database session
            position_filter: Optional position filter
            sort_by: Sort field
            sort_order: Sort order ('asc' or 'desc')
            
        Returns:
            Cached data or None if not available
        """
        if db is None:
            db = next(get_db())
            should_close = True
        else:
            should_close = False
            
        try:
            # Build base query
            query = db.query(Player).filter(
                Player.team_id == team_id,
                Player.season == season
            )
            
            if league_id:
                query = query.filter(Player.league_id == league_id)
            
            # Apply position filter
            if position_filter:
                query = query.filter(Player.position == position_filter)
            
            # Get total count before sorting and pagination
            total_count = query.count()
            
            # Apply sorting BEFORE pagination to ensure correct order
            if sort_by == "lastname":
                if sort_order == "desc":
                    query = query.order_by(Player.lastname.desc().nullslast())
                else:
                    query = query.order_by(Player.lastname.asc().nullslast())
            elif sort_by == "firstname":
                if sort_order == "desc":
                    query = query.order_by(Player.firstname.desc().nullslast())
                else:
                    query = query.order_by(Player.firstname.asc().nullslast())
            elif sort_by == "name":
                if sort_order == "desc":
                    query = query.order_by(Player.name.desc().nullslast())
                else:
                    query = query.order_by(Player.name.asc().nullslast())
            elif sort_by == "age":
                if sort_order == "desc":
                    query = query.order_by(Player.age.desc().nullslast())
                else:
                    query = query.order_by(Player.age.asc().nullslast())
            elif sort_by == "goals":
                if sort_order == "desc":
                    query = query.order_by(Player.goals.desc().nullslast())
                else:
                    query = query.order_by(Player.goals.asc().nullslast())
            elif sort_by == "assists":
                if sort_order == "desc":
                    query = query.order_by(Player.assists.desc().nullslast())
                else:
                    query = query.order_by(Player.assists.asc().nullslast())
            elif sort_by == "rating":
                if sort_order == "desc":
                    query = query.order_by(Player.rating.desc().nullslast())
                else:
                    query = query.order_by(Player.rating.asc().nullslast())
            else:
                # Default to lastname asc
                query = query.order_by(Player.lastname.asc().nullslast())
            
            # Apply pagination AFTER sorting
            offset = (page - 1) * limit
            players = query.offset(offset).limit(limit).all()
            
            if not players:
                return None
            
            # Convert to API-like format
            response = []
            for player in players:
                player_data = {
                    "player": {
                        "id": player.id,
                        "name": player.name,
                        "firstname": player.firstname,
                        "lastname": player.lastname,
                        "age": player.age,
                        "birth": {
                            "date": player.birth_date,
                            "place": player.birth_place,
                            "country": player.birth_country
                        },
                        "nationality": player.nationality,
                        "height": player.height,
                        "weight": player.weight,
                        "injured": player.injured,
                        "photo": player.photo
                    },
                    "statistics": [{
                        "team": {
                            "id": player.team_id,
                            "name": player.team.name if player.team else None
                        },
                        "league": {
                            "id": player.league_id,
                            "name": player.league.name if player.league else None
                        },
                        "games": {
                            "position": player.position,
                            "number": player.number,
                            "captain": player.captain,
                            "appearences": player.appearances,
                            "lineups": player.lineups,
                            "minutes": player.minutes,
                            "rating": player.rating
                        },
                        "goals": {
                            "total": player.goals,
                            "assists": player.assists
                        },
                        "cards": {
                            "yellow": player.yellow_cards,
                            "red": player.red_cards
                        },
                        "shots": {
                            "total": player.shots_total,
                            "on": player.shots_on_target
                        },
                        "passes": {
                            "total": player.passes_total,
                            "accuracy": player.passes_accuracy
                        },
                        "tackles": {
                            "total": player.tackles_total,
                            "blocks": player.blocks_total,
                            "interceptions": player.interceptions_total
                        },
                        "duels": {
                            "total": player.duels_total,
                            "won": player.duels_won
                        },
                        "dribbles": {
                            "attempts": player.dribbles_attempts,
                            "success": player.dribbles_success
                        },
                        "fouls": {
                            "drawn": player.fouls_drawn,
                            "committed": player.fouls_committed
                        }
                    }]
                }
                response.append(player_data)
            
            # Build parameters
            parameters = {
                "team": str(team_id),
                "season": str(season),
                "page": str(page)
            }
            if league_id:
                parameters["league"] = str(league_id)
            if position_filter:
                parameters["position"] = position_filter
            if sort_by:
                parameters["sort_by"] = sort_by
            if sort_order:
                parameters["sort_order"] = sort_order
            
            return {
                "get": "players",
                "parameters": parameters,
                "errors": [],
                "results": total_count,
                "paging": {
                    "current": page,
                    "total": (total_count + limit - 1) // limit
                },
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error getting cached team data: {e}")
            return None
        finally:
            if should_close:
                db.close()
    
    def is_data_stale(self, league_id: int = None, season: int = None, team_id: int = None, db: Session = None, max_age_hours: int = 24) -> bool:
        """
        Check if cached data is stale.
        
        Args:
            league_id: Optional league ID
            season: Optional season year
            team_id: Optional team ID
            db: Database session
            max_age_hours: Maximum age in hours before data is considered stale
            
        Returns:
            True if data is stale, False otherwise
        """
        if db is None:
            db = next(get_db())
            should_close = True
        else:
            should_close = False
            
        try:
            # Check if we have any recent data
            from datetime import datetime, timedelta, timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
            
            query = db.query(Player).filter(Player.updated_at >= cutoff_time)
            
            if league_id:
                query = query.filter(Player.league_id == league_id)
            if season:
                query = query.filter(Player.season == season)
            if team_id:
                query = query.filter(Player.team_id == team_id)
            
            recent_player = query.first()
            
            return recent_player is None
            
        except Exception as e:
            logger.error(f"Error checking data staleness: {e}")
            return True  # Assume stale if we can't check
        finally:
            if should_close:
                db.close()
