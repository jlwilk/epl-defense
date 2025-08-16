from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/")
def get_standings(
    season: int = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        data = client.get("/standings", params={"season": season_id, "league": league_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


