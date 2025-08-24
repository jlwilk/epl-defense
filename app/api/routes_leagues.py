from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.api_client import ApiClientV3
from app.schemas import ApiResponse, LeagueResponse
from app.config import get_settings

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get(
    "/",
    summary="List Leagues",
    description="Get leagues with optional filtering by country or search term.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with league data",
            "content": {
                "application/json": {
                    "example": {
                        "get": "leagues",
                        "parameters": {"country": "England"},
                        "errors": None,
                        "results": 1,
                        "paging": {"current": 1, "total": 1},
                        "response": [
                            {
                                "id": 39,
                                "name": "Premier League",
                                "type": "League",
                                "country": "England",
                                "country_code": "GB",
                                "logo": "https://media.api-sports.io/football/leagues/39.png",
                                "flag": "https://media.api-sports.io/flags/gb.svg",
                                "season": 2025,
                                "season_start": "2025-08-16",
                                "season_end": "2026-05-25",
                                "is_current": True,
                                "coverage": {
                                    "fixtures": {"events": True, "lineups": True, "statistics": True},
                                    "standings": True,
                                    "players": True,
                                    "top_scorers": True,
                                    "top_assists": True,
                                    "top_cards": True,
                                    "injuries": False,
                                    "predictions": True,
                                    "odds": False
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
)
def list_leagues(
    country: str | None = Query(None, description="Filter by country name"),
    search: str | None = Query(None, description="Search league by name"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get leagues with optional filtering."""
    settings = get_settings()
    api_client = ApiClientV3()
    
    params = {}
    if country:
        params["country"] = country
    if search:
        params["search"] = search
    
    response = api_client.get("leagues", params=params)
    
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
    "/{league_id}",
    summary="Get League by ID",
    description="Get detailed information about a specific league by ID.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with league details",
            "content": {
                "application/json": {
                    "example": {
                        "get": "leagues",
                        "parameters": {"id": "39"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": [
                            {
                                "id": 39,
                                "name": "Premier League",
                                "type": "League",
                                "country": "England",
                                "country_code": "GB",
                                "logo": "https://media.api-sports.io/football/leagues/39.png",
                                "flag": "https://media.api-sports.io/flags/gb.svg",
                                "season": 2025
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_league_by_id(
    league_id: int = Path(..., description="League ID"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get detailed information about a specific league by ID."""
    api_client = ApiClientV3()
    response = api_client.get("leagues", params={"id": league_id})
    
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
    "/country/{country}",
    summary="Get Leagues by Country",
    description="Get leagues for a specific country.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with leagues for the country",
            "content": {
                "application/json": {
                    "example": {
                        "get": "leagues",
                        "parameters": {"country": "England"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": [
                            {
                                "id": 39,
                                "name": "Premier League",
                                "type": "League",
                                "country": "England",
                                "country_code": "GB",
                                "logo": "https://media.api-sports.io/football/leagues/39.png",
                                "flag": "https://media.api-sports.io/flags/gb.svg",
                                "season": 2025
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_leagues_by_country(
    country: str = Path(..., description="Country name"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get leagues for a specific country."""
    api_client = ApiClientV3()
    response = api_client.get("leagues", params={"country": country})
    
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
    "/name/{name}",
    summary="Get League by Name",
    description="Get leagues by name search.",
    response_model=ApiResponse,
    responses={
        200: {
            "description": "Successful response with leagues matching the name",
            "content": {
                "application/json": {
                    "example": {
                        "get": "leagues",
                        "parameters": {"name": "Premier League"},
                        "errors": None,
                        "results": 1,
                        "paging": None,
                        "response": [
                            {
                                "id": 39,
                                "name": "Premier League",
                                "type": "League",
                                "country": "England",
                                "country_code": "GB",
                                "logo": "https://media.api-sports.io/football/leagues/39.png",
                                "flag": "https://media.api-sports.io/flags/gb.svg",
                                "season": 2025
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_leagues_by_name(
    name: str = Path(..., description="League name"),
    db: Session = Depends(get_db),
) -> ApiResponse:
    """Get leagues by name search."""
    api_client = ApiClientV3()
    response = api_client.get("leagues", params={"name": name})
    
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


