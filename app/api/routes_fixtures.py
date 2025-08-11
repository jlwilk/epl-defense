from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("/")
def list_fixtures(
    season: int = Query(..., description="Season year, e.g. 2024"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    last: int | None = Query(None, description="Return last N fixtures"),
) -> Dict[str, Any]:
    settings = get_settings()
    league_id = league or settings.league_id_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"season": season, "league": league_id}
        if last is not None:
            params["last"] = last
        data = client.get("/fixtures", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


