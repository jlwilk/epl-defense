from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/")
def get_standings(
    season: int = Query(..., description="Season year, e.g. 2024"),
    league: int = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    settings = get_settings()
    league_id = league or settings.league_id_default
    try:
        client = ApiClientV3()
        data = client.get("/standings", params={"season": season, "league": league_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


