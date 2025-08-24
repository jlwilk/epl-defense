from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.api_client import ApiClientV3
from app.schemas import ApiResponse, StandingResponse
from app.config import get_settings

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get(
    "/",
    summary="Get Standings",
    description="Get league standings for a specific season and league.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with standings data",
            "content": {
                "application/json": {
                    "example": {
                        "get": "standings",
                        "parameters": {"league": "39", "season": "2025"},
                        "errors": None,
                        "results": 20,
                        "paging": None,
                        "response": [
                            [
                                {
                                    "rank": 1,
                                    "team": {
                                        "id": 40,
                                        "name": "Liverpool",
                                        "logo": "https://media.api-sports.io/football/teams/40.png"
                                    },
                                    "points": 45,
                                    "goalsDiff": 23,
                                    "group": "Premier League",
                                    "form": "WWDWL",
                                    "status": "same",
                                    "description": "Champions League",
                                    "all": {
                                        "played": 20,
                                        "win": 14,
                                        "draw": 3,
                                        "lose": 3,
                                        "goals": {"for": 43, "against": 20}
                                    },
                                    "home": {
                                        "played": 10,
                                        "win": 8,
                                        "draw": 1,
                                        "lose": 1,
                                        "goals": {"for": 25, "against": 8}
                                    },
                                    "away": {
                                        "played": 10,
                                        "win": 6,
                                        "draw": 2,
                                        "lose": 2,
                                        "goals": {"for": 18, "against": 12}
                                    }
                                }
                            ]
                        ]
                    }
                }
            }
        }
    }
)
def get_standings(
    season: int | None = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get league standings for a specific season and league."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    # Use defaults if not provided
    if season is None:
        season = settings.season_default
    if league is None:
        league = settings.league_id_default
    
    response = api_client.get("standings", params={"league": league, "season": season})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    return response


@router.get(
    "/{league_id}",
    summary="Get Standings by League ID",
    description="Get league standings for a specific league ID with default season.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with standings data",
            "content": {
                "application/json": {
                    "example": {
                        "get": "standings",
                        "parameters": {"league": "39", "season": "2025"},
                        "errors": None,
                        "results": 20,
                        "paging": None,
                        "response": [
                            [
                                {
                                    "rank": 1,
                                    "team": {
                                        "id": 40,
                                        "name": "Liverpool",
                                        "logo": "https://media.api-sports.io/football/teams/40.png"
                                    },
                                    "points": 45,
                                    "goalsDiff": 23,
                                    "group": "Premier League",
                                    "form": "WWDWL",
                                    "status": "same",
                                    "description": "Champions League"
                                }
                            ]
                        ]
                    }
                }
            }
        }
    }
)
def get_standings_by_league_id(
    league_id: int = Path(..., description="League ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get league standings for a specific league ID with default season."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    # Use default season
    season = settings.season_default
    
    response = api_client.get("standings", params={"league": league_id, "season": season})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    return response


@router.get(
    "/{league_id}/{season}",
    summary="Get Standings by League ID and Season",
    description="Get league standings for a specific league ID and season.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with standings data",
            "content": {
                "application/json": {
                    "example": {
                        "get": "standings",
                        "parameters": {"league": "39", "season": "2024"},
                        "errors": None,
                        "results": 20,
                        "paging": None,
                        "response": [
                            [
                                {
                                    "rank": 1,
                                    "team": {
                                        "id": 40,
                                        "name": "Liverpool",
                                        "logo": "https://media.api-sports.io/football/teams/40.png"
                                    },
                                    "points": 45,
                                    "goalsDiff": 23,
                                    "group": "Premier League",
                                    "form": "WWDWL",
                                    "status": "same",
                                    "description": "Champions League"
                                }
                            ]
                        ]
                    }
                }
            }
        }
    }
)
def get_standings_by_league_id_and_season(
    league_id: int = Path(..., description="League ID"),
    season: int = Path(..., description="Season year"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get league standings for a specific league ID and season."""
    api_client = ApiClientV3()
    
    response = api_client.get("standings", params={"league": league_id, "season": season})
    
    # Ensure errors field is None (not empty list) to match ApiResponse schema
    if response.get("errors") == []:
        response["errors"] = None
    
    # Ensure paging field is None if it's an empty dict or empty list
    if response.get("paging") in [{}, []]:
        response["paging"] = None
    
    return response


