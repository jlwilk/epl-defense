from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/team-stats", tags=["team-statistics"])


@router.get("/{team_id}/overview")
def get_team_overview(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get comprehensive team overview including fixtures, goals, and form."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/goals")
def get_team_goals(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get detailed goal statistics for a team."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        
        # Extract and format goal statistics
        response = data.get("response", {})
        goals_data = response.get("goals", {})
        
        return {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "goals": {
                "for": {
                    "total": goals_data.get("for", {}).get("total", {}),
                    "average": goals_data.get("for", {}).get("average", {}),
                    "minute": goals_data.get("for", {}).get("minute", {})
                },
                "against": {
                    "total": goals_data.get("against", {}).get("total", {}),
                    "average": goals_data.get("against", {}).get("average", {}),
                    "minute": goals_data.get("against", {}).get("minute", {})
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/fixtures-stats")
def get_team_fixtures_stats(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get team fixture statistics including wins, draws, losses, and form."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        
        # Extract and format fixture statistics
        response = data.get("response", {})
        fixtures_data = response.get("fixtures", {})
        
        return {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "fixtures": {
                "played": fixtures_data.get("played", {}),
                "wins": fixtures_data.get("wins", {}),
                "draws": fixtures_data.get("draws", {}),
                "loses": fixtures_data.get("loses", {}),
                "form": fixtures_data.get("form", "")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/cards")
def get_team_cards(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get team card statistics (yellow and red cards)."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        
        # Extract and format card statistics
        response = data.get("response", {})
        cards_data = response.get("cards", {})
        
        return {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "cards": {
                "yellow": cards_data.get("yellow", {}),
                "red": cards_data.get("red", {})
            }
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/lineups")
def get_team_lineups(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get team lineup statistics and formations used."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        
        # Extract and format lineup statistics
        response = data.get("response", {})
        lineups_data = response.get("lineups", [])
        
        return {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "lineups": lineups_data
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/comparison")
def compare_team_stats(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get comprehensive team statistics comparison and summary."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/teams/statistics", params={
            "team": team_id,
            "season": season_id,
            "league": league_id
        })
        
        # Extract and format comprehensive statistics
        response = data.get("response", {})
        
        return {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "summary": {
                "fixtures": response.get("fixtures", {}),
                "goals": response.get("goals", {}),
                "cards": response.get("cards", {}),
                "lineups": response.get("lineups", []),
                "league": response.get("league", {}),
                "team": response.get("team", {})
            }
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/league/{league_id}/season/{season_id}")
def get_league_team_stats(
    league_id: int,
    season_id: int,
    team: int | None = Query(None, description="Specific team ID (optional)"),
) -> Dict[str, Any]:
    """Get team statistics for all teams in a league/season or a specific team."""
    try:
        client = ApiClientV3()
        
        if team:
            # Get stats for specific team
            data = client.get("/teams/statistics", params={
                "team": team,
                "league": league_id,
                "season": season_id
            })
            return data
        else:
            # Get all teams in league/season first, then their stats
            teams_data = client.get("/teams", params={
                "league": league_id,
                "season": season_id
            })
            
            teams = teams_data.get("response", [])
            all_stats = []
            
            for team_info in teams:
                team_id = team_info.get("team", {}).get("id")
                if team_id:
                    try:
                        stats = client.get("/teams/statistics", params={
                            "team": team_id,
                            "league": league_id,
                            "season": season_id
                        })
                        all_stats.append(stats.get("response", {}))
                    except Exception:
                        # Skip teams with stats errors
                        continue
            
            return {
                "league": league_id,
                "season": season_id,
                "total_teams": len(teams),
                "teams_with_stats": len(all_stats),
                "statistics": all_stats
            }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/league/{league_id}/season/{season_id}/teams")
def get_league_teams(
    league_id: int,
    season_id: int,
) -> Dict[str, Any]:
    """Get all teams in a league/season without individual statistics (faster)."""
    try:
        client = ApiClientV3()
        data = client.get("/teams", params={
            "league": league_id,
            "season": season_id
        })
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
