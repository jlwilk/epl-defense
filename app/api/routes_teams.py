from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import ApiResponse, TeamStatisticsApiResponse
from app.services.api_client import ApiClientV3
from app.config import get_settings

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get(
    "/",
    summary="List Teams",
    description="Get teams with optional filtering by league, season, country, or search term. Returns comprehensive team information including venue details, founding year, and team codes.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with team data",
            "content": {
                "application/json": {
                    "example": {
                        "get": "teams",
                        "parameters": {"league": "39", "season": "2025"},
                        "errors": None,
                        "results": 20,
                        "paging": {"current": 1, "total": 1},
                        "response": [
                            {
                                "id": 40,
                                "name": "Liverpool",
                                "code": "LIV",
                                "country": "England",
                                "founded": 1892,
                                "national": False,
                                "logo": "https://media.api-sports.io/football/teams/40.png",
                                "venue_id": 550,
                                "venue_name": "Anfield",
                                "venue_address": "Anfield Road",
                                "venue_city": "Liverpool",
                                "venue_capacity": 53394,
                                "venue_surface": "grass",
                                "venue_image": "https://media.api-sports.io/football/venues/550.png"
                            },
                            {
                                "id": 33,
                                "name": "Manchester United",
                                "code": "MUN",
                                "country": "England",
                                "founded": 1878,
                                "national": False,
                                "logo": "https://media.api-sports.io/football/teams/33.png",
                                "venue_id": 556,
                                "venue_name": "Old Trafford",
                                "venue_address": "Sir Matt Busby Way",
                                "venue_city": "Manchester",
                                "venue_capacity": 74140,
                                "venue_surface": "grass",
                                "venue_image": "https://media.api-sports.io/football/venues/556.png"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Bad request - invalid parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid league ID or season parameter"
                    }
                }
            }
        },
        422: {
            "description": "Validation error - invalid parameter types",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "season"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def list_teams(
    season: int | None = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    country: str | None = Query(None, description="Country name"),
    search: str | None = Query(None, description="Search team by name"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get teams with optional filtering."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    # Use defaults if not provided
    if season is None:
        season = settings.season_default
    if league is None:
        league = settings.league_id_default
    
    params = {"season": season, "league": league}
    if country:
        params["country"] = country
    if search:
        params["search"] = search
    
    response = api_client.get("teams", params=params)
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    # Ensure parameters field is a dict (not empty list) to match ApiResponse schema
    if response.get("parameters") == []:
        response["parameters"] = {}
    
    return response


@router.get(
    "/search",
    summary="Search Teams",
    description="Search for teams by name with optional country filtering. Useful for finding teams when you know part of their name or want to filter by country.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful search response",
            "content": {
                "application/json": {
                    "example": {
                        "get": "teams",
                        "parameters": {"search": "Manchester", "country": "England"},
                        "errors": None,
                        "results": 2,
                        "paging": {"current": 1, "total": 1},
                        "response": [
                            {
                                "id": 33,
                                "name": "Manchester United",
                                "code": "MUN",
                                "country": "England",
                                "founded": 1878,
                                "national": False,
                                "logo": "https://media.api-sports.io/football/teams/33.png"
                            },
                            {
                                "id": 50,
                                "name": "Manchester City",
                                "code": "MCI",
                                "country": "England",
                                "founded": 1880,
                                "national": False,
                                "logo": "https://media.api-sports.io/football/teams/50.png"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Bad request - search parameter required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Search parameter is required"
                    }
                }
            }
        },
        422: {
            "description": "Validation error - invalid parameter types",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "search"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def search_teams(
    search: str = Query(..., description="Team name to search for"),
    country: str | None = Query(None, description="Filter by country"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Search for teams by name with optional country filtering."""
    api_client = ApiClientV3()
    
    params = {"search": search}
    if country:
        params["country"] = country
    
    response = api_client.get("teams", params=params)
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure parameters field is a dict (not empty list) to match ApiResponse schema
    if response.get("parameters") == []:
        response["parameters"] = {}
    
    return response


@router.get(
    "/{team_id}",
    summary="Get Team",
    description="Get detailed information about a specific team.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with team details",
            "content": {
                "application/json": {
                    "example": {
                        "get": "teams",
                        "parameters": {"id": "40"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": [
                            {
                                "id": 40,
                                "name": "Liverpool",
                                "code": "LIV",
                                "country": "England",
                                "founded": 1892,
                                "national": False,
                                "logo": "https://media.api-sports.io/football/teams/40.png",
                                "venue_id": 550,
                                "venue_name": "Anfield",
                                "venue_address": "Anfield Road",
                                "venue_city": "Liverpool",
                                "venue_capacity": 53394,
                                "venue_surface": "grass",
                                "venue_image": "https://media.api-sports.io/football/venues/550.png"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_team(
    team_id: int = Path(..., description="Team ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get detailed information about a specific team."""
    api_client = ApiClientV3()
    response = api_client.get("teams", params={"id": team_id})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    # Ensure parameters field is a dict (not empty list) to match ApiResponse schema
    if response.get("parameters") == []:
        response["parameters"] = {}
    
    return response


@router.get(
    "/{team_id}/statistics",
    summary="Get Team Statistics",
    description="Get team statistics for a specific season and league.",
    response_model=TeamStatisticsApiResponse,
    responses={
        200: {
            "description": "Successful response with team statistics",
            "content": {
                "application/json": {
                    "example": {
                        "get": "teams/statistics",
                        "parameters": {"team": "40", "league": "39", "season": "2025"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": {
                            "league": {
                                "id": 39,
                                "name": "Premier League",
                                "country": "England",
                                "logo": "https://media.api-sports.io/football/leagues/39.png",
                                "flag": "https://media.api-sports.io/flags/gb-eng.svg",
                                "season": 2025
                            },
                            "team": {
                                "id": 40,
                                "name": "Liverpool",
                                "logo": "https://media.api-sports.io/football/teams/40.png"
                            },
                            "form": "WWDWL",
                            "fixtures": {
                                "played": {"home": 10, "away": 10, "total": 20},
                                "wins": {"home": 8, "away": 6, "total": 14},
                                "draws": {"home": 1, "away": 2, "total": 3},
                                "loses": {"home": 1, "away": 2, "total": 3}
                            },
                            "goals": {
                                "for": {
                                    "total": {"home": 25, "away": 18, "total": 43},
                                    "average": {"home": "2.5", "away": "1.8", "total": "2.15"},
                                    "minute": {
                                        "0-15": {"total": 5, "percentage": "11.6%"},
                                        "16-30": {"total": 8, "percentage": "18.6%"},
                                        "31-45": {"total": 12, "percentage": "27.9%"},
                                        "46-60": {"total": 6, "percentage": "14.0%"},
                                        "61-75": {"total": 7, "percentage": "16.3%"},
                                        "76-90": {"total": 5, "percentage": "11.6%"}
                                    }
                                },
                                "against": {
                                    "total": {"home": 8, "away": 12, "total": 20},
                                    "average": {"home": "0.8", "away": "1.2", "total": "1.0"}
                                }
                            },
                            "biggest": {
                                "streak": {"wins": 5, "draws": 2, "loses": 1},
                                "wins": {"home": "3-0", "away": "2-1"},
                                "loses": {"home": "0-1", "away": "1-2"},
                                "goals": {"for": {"home": 4, "away": 3}, "against": {"home": 0, "away": 2}}
                            },
                            "clean_sheet": {"home": 5, "away": 3, "total": 8},
                            "failed_to_score": {"home": 1, "away": 2, "total": 3},
                            "penalty": {
                                "scored": {"total": 3, "percentage": "75%"},
                                "missed": {"total": 1, "percentage": "25%"},
                                "total": 4
                            },
                            "lineups": [
                                {"formation": "4-3-3", "played": 15},
                                {"formation": "4-2-3-1", "played": 5}
                            ],
                            "cards": {
                                "yellow": {
                                    "0-15": {"total": 2, "percentage": "10.0%"},
                                    "16-30": {"total": 3, "percentage": "15.0%"},
                                    "31-45": {"total": 5, "percentage": "25.0%"},
                                    "46-60": {"total": 4, "percentage": "20.0%"},
                                    "61-75": {"total": 3, "percentage": "15.0%"},
                                    "76-90": {"total": 3, "percentage": "15.0%"}
                                },
                                "red": {
                                    "0-15": {"total": 0, "percentage": "0%"},
                                    "16-30": {"total": 1, "percentage": "5.0%"},
                                    "31-45": {"total": 0, "percentage": "0%"},
                                    "46-60": {"total": 0, "percentage": "0%"},
                                    "61-75": {"total": 0, "percentage": "0%"},
                                    "76-90": {"total": 0, "percentage": "0%"}
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request - invalid team ID or parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid team ID or missing required parameters"
                    }
                }
            }
        },
        422: {
            "description": "Validation error - invalid parameter types",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "team_id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_team_statistics(
    team_id: int = Path(..., description="Team ID"),
    season: int | None = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    db: Session = Depends(get_db),
) -> TeamStatisticsApiResponse:
    """Get team statistics for a specific season and league."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    # Use defaults if not provided
    if season is None:
        season = settings.season_default
    if league is None:
        league = settings.league_id_default
    
    response = api_client.get("teams/statistics", params={"team": team_id, "season": season, "league": league})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    # Ensure parameters field is a dict (not empty list) to match ApiResponse schema
    if response.get("parameters") == []:
        response["parameters"] = {}
    
    return response


@router.get(
    "/{team_id}/seasons",
    summary="Get Team Seasons",
    description="Get all seasons available for a specific team.",
    response_model=ApiResponse
)
def get_team_seasons(
    team_id: int = Path(..., description="Team ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get all seasons available for a specific team."""
    api_client = ApiClientV3()
    response = api_client.get("teams/seasons", params={"team": team_id})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    return response


@router.get(
    "/{team_id}/countries",
    summary="Get Team Countries",
    description="Get countries where a team has played.",
    response_model=ApiResponse
)
def get_team_countries(
    team_id: int = Path(..., description="Team ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get countries where a team has played."""
    api_client = ApiClientV3()
    response = api_client.get("teams/countries", params={"team": team_id})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    return response


@router.get(
    "/{team_id}/leagues",
    summary="Get Team Leagues",
    description="Get leagues where a team has played, optionally filtered by season.",
    response_model=ApiResponse
)
def get_team_leagues(
    team_id: int = Path(..., description="Team ID"),
    season: int | None = Query(None, description="Season year (defaults to 2025)"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get leagues where a team has played, optionally filtered by season."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    params = {"team": team_id}
    if season is None:
        season = settings.season_default
    params["season"] = season
    
    response = api_client.get("teams/leagues", params=params)
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    return response


@router.get(
    "/{team_id}/fixtures",
    summary="Get Team Fixtures",
    description="Get fixtures for a specific team with various filtering options.",
    response_model=ApiResponse
)
def get_team_fixtures(
    team_id: int = Path(..., description="Team ID"),
    season: int | None = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id"),
    last: int | None = Query(None, description="Return last N fixtures"),
    next: int | None = Query(None, description="Return next N fixtures"),
    from_date: str | None = Query(None, description="From date (YYYY-MM-DD)"),
    to_date: str | None = Query(None, description="To date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get fixtures for a specific team with various filtering options."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    params = {"team": team_id}
    if season is None:
        season = settings.season_default
    params["season"] = season
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
    
    response = api_client.get("fixtures", params=params)
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    return response


@router.get(
    "/{team_id}/players",
    summary="Get Team Players",
    description="Get players for a specific team in a season.",
    response_model=ApiResponse
)
def get_team_players(
    team_id: int = Path(..., description="Team ID"),
    season: int | None = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id"),
    page: int | None = Query(1, description="Page number for pagination"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get players for a specific team in a season."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    params = {"team": team_id}
    if season is None:
        season = settings.season_default
    params["season"] = season
    if league:
        params["league"] = league
    if page:
        params["page"] = page
    
    response = api_client.get("players", params=params)
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    return response





