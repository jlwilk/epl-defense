from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/player-stats", tags=["player-statistics"])


@router.get("/player/{player_id}")
def get_player_statistics(
    player_id: int,
    season: int = Query(..., description="Season year"),
    league: int | None = Query(None, description="League ID to filter by")
) -> Dict[str, Any]:
    """Get comprehensive statistics for a specific player in a season.
    
    This endpoint provides detailed season-long performance metrics for a player,
    including goals, assists, cards, shots, passes, tackles, and other statistics.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics(player_id, season, league)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/league/{league_id}")
def get_league_player_statistics(
    league_id: int,
    season: int = Query(..., description="Season year"),
    team: int | None = Query(None, description="Team ID to filter by")
) -> Dict[str, Any]:
    """Get player statistics for all players in a league/season.
    
    This endpoint provides comprehensive player statistics across an entire league,
    useful for creating league-wide player rankings and comparisons.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league_id, season, team)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/team/{team_id}")
def get_team_player_statistics(
    team_id: int,
    season: int = Query(..., description="Season year"),
    league: int | None = Query(None, description="League ID to filter by")
) -> Dict[str, Any]:
    """Get player statistics for all players in a specific team.
    
    This endpoint provides comprehensive player statistics for a team,
    useful for team analysis and player performance comparison within the team.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics_by_team(team_id, season, league)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/player/{player_id}/seasons")
def get_player_seasons(player_id: int) -> Dict[str, Any]:
    """Get all seasons for a specific player.
    
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
    """Get all available player countries.
    
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
    league: int | None = Query(None, description="League ID to filter by"),
    season: int | None = Query(None, description="Season year to filter by")
) -> Dict[str, Any]:
    """Search for players by name.
    
    This endpoint allows searching for players by name with optional
    filtering by league and season for more targeted results.
    """
    try:
        client = ApiClientV3()
        data = client.search_players(search, league, season)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/top-scorers")
def get_top_scorers(
    league: int = Query(..., description="League ID"),
    season: int = Query(..., description="Season year"),
    limit: int = Query(10, description="Number of top scorers to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top goal scorers for a league/season.
    
    This endpoint provides the top goal scorers in a league,
    useful for creating goal-scoring leaderboards and analysis.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league, season)
        
        if data.get("response"):
            # Sort players by goals scored (descending)
            players = data["response"]
            sorted_players = sorted(
                players,
                key=lambda x: x.get("statistics", [{}])[0].get("goals", {}).get("total", 0) or 0,
                reverse=True
            )
            
            # Return top N scorers
            top_scorers = sorted_players[:limit]
            data["response"] = top_scorers
            data["results"] = len(top_scorers)
            data["top_scorers"] = True
        
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/top-assists")
def get_top_assists(
    league: int = Query(..., description="League ID"),
    season: int = Query(..., description="Season year"),
    limit: int = Query(10, description="Number of top assist providers to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top assist providers for a league/season.
    
    This endpoint provides the top assist providers in a league,
    useful for creating assist leaderboards and playmaker analysis.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league, season)
        
        if data.get("response"):
            # Sort players by assists (descending)
            players = data["response"]
            sorted_players = sorted(
                players,
                key=lambda x: x.get("statistics", [{}])[0].get("goals", {}).get("assists", 0) or 0,
                reverse=True
            )
            
            # Return top N assist providers
            top_assists = sorted_players[:limit]
            data["response"] = top_assists
            data["results"] = len(top_assists)
            data["top_assists"] = True
        
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/defensive-leaders")
def get_defensive_leaders(
    league: int = Query(..., description="League ID"),
    season: int = Query(..., description="Season year"),
    stat_type: str = Query("tackles", description="Defensive stat to rank by: tackles, interceptions, blocks, clean_sheets"),
    limit: int = Query(10, description="Number of top defensive players to return", ge=1, le=50)
) -> Dict[str, Any]:
    """Get top defensive players for a league/season.
    
    This endpoint provides the top defensive players based on various metrics,
    useful for analyzing defensive performance and creating defensive leaderboards.
    """
    try:
        client = ApiClientV3()
        data = client.get_player_statistics_by_league(league, season)
        
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
                    # For clean sheets, we want players with 0 goals conceded (more clean sheets)
                    sorted_players = sorted(
                        players,
                        key=lambda x: x.get("statistics", [{}])[0].get(category, {}).get(field, 999) or 999
                    )
                else:
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
