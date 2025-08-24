from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.services.api_client import ApiClientV3
from app.services.player_sync_service import PlayerSyncService
from app.db.session import get_db

router = APIRouter(prefix="/player-stats", tags=["player-statistics"])


@router.get("/player/{player_id}")
def get_player_statistics(
    player_id: int,
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    league: int | None = Query(None, description="League ID (defaults to environment setting)")
) -> Dict[str, Any]:
    """Get comprehensive statistics for a specific player in a season.
    
    This endpoint provides detailed season-long performance metrics for a player,
    including goals, assists, cards, shots, passes, tackles, and other statistics.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        client = ApiClientV3()
        data = client.get_player_statistics(player_id, season_id, league_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/sync/league/{league_id}")
def sync_league_players(
    league_id: int,
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Sync all players for a league and season from API-Football to local database.
    
    This endpoint fetches all player data from the external API and stores it locally
    for faster access and reduced API calls.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        
        sync_service = PlayerSyncService()
        result = sync_service.sync_league_players(league_id, season_id, db)
        
        if result["success"]:
            return {
                "message": "League players synced successfully",
                "data": result
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/league/{league_id}")
def get_league_player_statistics(
    league_id: int,
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    team: int | None = Query(None, description="Team ID to filter by"),
    position: str | None = Query(None, description="Position to filter by (e.g., 'Attacker', 'Midfielder', 'Defender', 'Goalkeeper')"),
    sort_by: str = Query("lastname", description="Sort field: 'lastname', 'firstname', 'name', 'goals', 'assists', 'rating', 'age'", regex="^(lastname|firstname|name|goals|assists|rating|age)$"),
    sort_order: str = Query("asc", description="Sort order: 'asc' or 'desc'", regex="^(asc|desc)$"),
    page: int = Query(1, description="Page number", ge=1),
    use_cache: bool = Query(True, description="Use cached data if available")
) -> Dict[str, Any]:
    """Get comprehensive player statistics across an entire league.
    
    This endpoint provides comprehensive player statistics across an entire league,
    useful for creating league-wide player rankings and comparisons.
    
    Supports pagination, sorting, filtering by team/position, and can use cached 
    database data for faster responses.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        
        # Try to get cached data first if requested
        if use_cache:
            db = next(get_db())
            try:
                sync_service = PlayerSyncService()
                cached_data = sync_service.get_cached_league_data(
                    league_id, season_id, page, 20, db,
                    team_filter=team,
                    position_filter=position,
                    sort_by=sort_by,
                    sort_order=sort_order
                )
                
                if cached_data and not sync_service.is_data_stale(league_id=league_id, season=season_id, db=db):
                    return cached_data
            except Exception as e:
                # Log error but continue with API call
                print(f"Cache error: {e}")
            finally:
                db.close()
        
        # Fall back to API call
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league_id, season_id, team, page)
        
        # Apply client-side filtering and sorting if needed
        if position or sort_by != "lastname" or sort_order != "asc":
            data = _apply_client_side_filters(data, position, sort_by, sort_order)
        
        return data
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.post("/sync/team/{team_id}")
def sync_team_players(
    team_id: int,
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Sync all players for a team and season from API-Football to local database.
    
    This endpoint fetches all player data for a specific team from the external API
    and stores it locally for faster access and reduced API calls.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        sync_service = PlayerSyncService()
        result = sync_service.sync_team_players(team_id, season_id, league_id, db)
        
        if result["success"]:
            return {
                "message": "Team players synced successfully",
                "data": result
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/team/{team_id}")
def get_team_player_statistics(
    team_id: int,
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    position: str | None = Query(None, description="Position to filter by (e.g., 'Attacker', 'Midfielder', 'Defender', 'Goalkeeper')"),
    sort_by: str = Query("lastname", description="Sort field: 'lastname', 'firstname', 'name', 'goals', 'assists', 'rating', 'age'", regex="^(lastname|firstname|name|goals|assists|rating|age)$"),
    sort_order: str = Query("asc", description="Sort order: 'asc' or 'desc'", regex="^(asc|desc)$"),
    page: int = Query(1, description="Page number", ge=1),
    use_cache: bool = Query(True, description="Use cached data if available")
) -> Dict[str, Any]:
    """Get comprehensive player statistics for a team.
    
    This endpoint provides comprehensive player statistics for a team,
    useful for team analysis and player performance comparison within the team.
    
    Supports pagination, sorting, filtering by position, and can use cached 
    database data for faster responses.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        # Try to get cached data first if requested
        if use_cache:
            db = next(get_db())
            try:
                sync_service = PlayerSyncService()
                cached_data = sync_service.get_cached_team_data(
                    team_id, season_id, league_id, page, 20, db,
                    position_filter=position,
                    sort_by=sort_by,
                    sort_order=sort_order
                )
                
                if cached_data and not sync_service.is_data_stale(team_id=team_id, season=season_id, league_id=league_id, db=db):
                    return cached_data
            except Exception as e:
                # Log error but continue with API call
                print(f"Cache error: {e}")
            finally:
                db.close()
        
        # Fall back to API call
        client = ApiClientV3()
        data = client.get_player_statistics_by_team(team_id, season_id, league_id, page)
        
        # Apply client-side filtering and sorting if needed
        if position or sort_by != "lastname" or sort_order != "asc":
            data = _apply_client_side_filters(data, position, sort_by, sort_order)
        
        return data
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/player/{player_id}/seasons")
def get_player_seasons(player_id: int) -> Dict[str, Any]:
    """Get all seasons a player has participated in.
    
    This endpoint shows all seasons a player has participated in,
    useful for tracking player career progression and availability.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_seasons(player_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/countries")
def get_player_countries() -> Dict[str, Any]:
    """Get list of all countries where players come from.
    
    This endpoint provides a list of all countries where players come from,
    useful for filtering and analysis by nationality.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_countries()
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/search")
def search_players(
    search: str = Query(..., description="Player name to search for"),
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    season: int | None = Query(None, description="Season year (defaults to environment setting)")
) -> Dict[str, Any]:
    """Search for players by name with optional filtering.
    
    This endpoint allows searching for players by name with optional
    filtering by league and season for more targeted results.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        client = ApiClientV3()
        data = client.search_players(search, league_id, season_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/top-scorers")
def get_top_scorers(
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    limit: int = Query(10, description="Number of top scorers to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top goal scorers for a league/season.
    
    This endpoint provides the top goal scorers in a league,
    useful for creating goal-scoring leaderboards and analysis.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        client = ApiClientV3()
        data = client.get_top_scorers(league_id, season_id, limit)
        
        # The API already returns sorted data, just limit the results
        if data.get("response"):
            data["response"] = data["response"][:limit]
            data["results"] = len(data["response"])
            data["top_scorers"] = True
        
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/top-assists")
def get_top_assists(
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    limit: int = Query(10, description="Number of top assist providers to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top assist providers for a league/season.
    
    This endpoint provides the top assist providers in a league,
    useful for creating assist leaderboards and playmaker analysis.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        client = ApiClientV3()
        data = client.get_top_assists(league_id, season_id, limit)
        
        # The API already returns sorted data, just limit the results
        if data.get("response"):
            data["response"] = data["response"][:limit]
            data["results"] = len(data["response"])
            data["top_assists"] = True
        
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/defensive-leaders")
def get_defensive_leaders(
    league: int | None = Query(None, description="League ID (defaults to environment setting)"),
    season: int | None = Query(None, description="Season year (defaults to environment setting)"),
    stat_type: str = Query("tackles", description="Defensive stat to rank by: tackles, interceptions, blocks, clean_sheets"),
    limit: int = Query(10, description="Number of top defensive players to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top defensive players for a league/season.
    
    This endpoint provides the top defensive players based on various metrics,
    useful for analyzing defensive performance and creating defensive leaderboards.
    """
    try:
        settings = get_settings()
        season_id = season or settings.season_default
        league_id = league or settings.league_id_default
        
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league_id, season_id)
        
        if data.get("response"):
            players = data["response"]
            
            # Map stat types to their API paths
            stat_mapping = {
                "tackles": ("tackles", "total"),
                "interceptions": ("tackles", "interceptions"),
                "blocks": ("tackles", "blocks"),
                "clean_sheets": ("goals", "conceded")  # Will be inverted for ranking
            }
            
            if stat_type in stat_mapping:
                category, field = stat_mapping[stat_type]
                
                # Sort players by the specified defensive stat
                if stat_type == "clean_sheets":
                    # For clean sheets, we want to sort by goals conceded (ascending)
                    sorted_players = sorted(
                        players,
                        key=lambda x: x.get("statistics", [{}])[0].get(category, {}).get(field, 999) or 999
                    )
                else:
                    # For other stats, sort by value (descending)
                    sorted_players = sorted(
                        players,
                        key=lambda x: x.get("statistics", [{}])[0].get(category, {}).get(field, 0) or 0,
                        reverse=True
                    )
                
                # Return top N defensive players
                top_defenders = sorted_players[:limit]
                data["response"] = top_defenders
                data["results"] = len(top_defenders)
                data["defensive_stat"] = stat_type
                data["top_defenders"] = True
            
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


def _apply_client_side_filters(data: Dict[str, Any], position: str | None, sort_by: str, sort_order: str) -> Dict[str, Any]:
    """
    Apply client-side filtering and sorting to API response data.
    
    Args:
        data: API response data
        position: Position filter
        sort_by: Sort field
        sort_order: Sort order ('asc' or 'desc')
        
    Returns:
        Filtered and sorted data
    """
    if not data.get("response"):
        return data
    
    response = data["response"]
    
    # Apply position filter
    if position:
        response = [
            player for player in response 
            if player.get("statistics", [{}])[0].get("games", {}).get("position") == position
        ]
    
    # Apply sorting
    if sort_by and sort_order:
        reverse = sort_order.lower() == "desc"
        
        def get_sort_key(player):
            if sort_by == "lastname":
                return player.get("player", {}).get("lastname", "").lower()
            elif sort_by == "firstname":
                return player.get("player", {}).get("firstname", "").lower()
            elif sort_by == "name":
                return player.get("player", {}).get("name", "").lower()
            elif sort_by == "age":
                age = player.get("player", {}).get("age")
                return age if age is not None else 999
            elif sort_by in ["goals", "assists"]:
                stats = player.get("statistics", [{}])[0]
                value = stats.get("goals", {}).get(sort_by, 0)
                return value if value is not None else 0
            elif sort_by == "rating":
                stats = player.get("statistics", [{}])[0]
                rating = stats.get("games", {}).get("rating")
                if rating is None:
                    return 0.0
                try:
                    return float(rating)
                except (ValueError, TypeError):
                    return 0.0
            else:
                return ""
        
        response.sort(key=get_sort_key, reverse=reverse)
    
    # Update the response and results count
    data["response"] = response
    data["results"] = len(response)
    
    # Update parameters to reflect applied filters
    if "parameters" not in data:
        data["parameters"] = {}
    
    if position:
        data["parameters"]["position"] = position
    if sort_by:
        data["parameters"]["sort_by"] = sort_by
    if sort_order:
        data["parameters"]["sort_order"] = sort_order
    
    return data
