from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/")
def list_teams(
    season: int = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    country: str | None = Query(None, description="Country name"),
    search: str | None = Query(None, description="Search team by name"),
) -> Dict[str, Any]:
    """Get teams with optional filtering by league, season, country, or search term."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"season": season_id}
        if league_id:
            params["league"] = league_id
        if country:
            params["country"] = country
        if search:
            params["search"] = search
        data = client.get("/teams", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}")
def get_team(team_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific team."""
    try:
        client = ApiClientV3()
        data = client.get(f"/teams", params={"id": team_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/statistics")
def get_team_statistics(
    team_id: int,
    season: int = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    """Get team statistics for a specific season and league."""
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


@router.get("/{team_id}/seasons")
def get_team_seasons(team_id: int) -> Dict[str, Any]:
    """Get all seasons available for a specific team."""
    try:
        client = ApiClientV3()
        data = client.get("/teams/seasons", params={"team": team_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/countries")
def get_team_countries(team_id: int) -> Dict[str, Any]:
    """Get countries where a team has played."""
    try:
        client = ApiClientV3()
        data = client.get("/teams/countries", params={"team": team_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/leagues")
def get_team_leagues(
    team_id: int,
    season: int | None = Query(None, description="Season year (defaults to 2025)"),
) -> Dict[str, Any]:
    """Get leagues where a team has played, optionally filtered by season."""
    settings = get_settings()
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"team": team_id}
        if season_id:
            params["season"] = season_id
        data = client.get("/teams/leagues", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/fixtures")
def get_team_fixtures(
    team_id: int,
    season: int | None = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id"),
    last: int | None = Query(None, description="Return last N fixtures"),
    next: int | None = Query(None, description="Return next N fixtures"),
    from_date: str | None = Query(None, description="From date (YYYY-MM-DD)"),
    to_date: str | None = Query(None, description="To date (YYYY-MM-DD)"),
) -> Dict[str, Any]:
    """Get fixtures for a specific team with various filtering options."""
    settings = get_settings()
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"team": team_id}
        if season_id:
            params["season"] = season_id
        if league:
            params["league"] = league
        if last:
            params["last"] = last
        if next:
            params["next"] = next
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        data = client.get("/fixtures", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{team_id}/players")
def get_team_players(
    team_id: int,
    season: int = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id"),
    page: int | None = Query(1, description="Page number for pagination"),
) -> Dict[str, Any]:
    """Get players for a specific team in a season."""
    settings = get_settings()
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {
            "team": team_id,
            "season": season_id,
            "page": page or 1
        }
        if league:
            params["league"] = league
        data = client.get("/players", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/search")
def search_teams(
    search: str = Query(..., description="Team name to search for"),
    country: str | None = Query(None, description="Filter by country"),
) -> Dict[str, Any]:
    """Search for teams by name with optional country filtering."""
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"search": search}
        if country:
            params["country"] = country
        data = client.get("/teams", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


