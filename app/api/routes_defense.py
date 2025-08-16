from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/defense", tags=["defense"])


@router.get("/table")
def defense_table(
    season: int = Query(None, description="Season year, e.g. 2025 (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
) -> Dict[str, Any]:
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        teams = client.get("/teams", params={"season": season_id, "league": league_id}).get("response", [])
        rows: List[Dict[str, Any]] = []
        for t in teams:
            team_id = t.get("team", {}).get("id")
            name = t.get("team", {}).get("name") or str(team_id)
            if not team_id:
                continue
            stats = client.get("/teams/statistics", params={"season": season_id, "league": league_id, "team": team_id})
            conceded = (
                stats.get("response", {})
                .get("goals", {})
                .get("against", {})
                .get("total", {})
                .get("total")
            )
            rows.append({"team": name, "conceded": conceded})
        rows.sort(key=lambda r: (r["conceded"] is None, r["conceded"]))
        return {"season": season_id, "league": league_id, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


