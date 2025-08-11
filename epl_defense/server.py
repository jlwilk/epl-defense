from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .api_client import ApiClient, ApiError, EPL_LEAGUE_ID


class HealthResponse(BaseModel):
    status: Any


def create_app() -> FastAPI:
    app = FastAPI(title="EPL Defense API", version="0.1.0")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        try:
            client = ApiClient.from_env()
            data = client.health()
            return HealthResponse(status=data.get("response"))
        except ApiError as e:
            raise HTTPException(status_code=429, detail=str(e))

    @app.get("/standings")
    def standings(
        season: int = Query(..., description="Season year, e.g. 2024"),
        league: int = Query(EPL_LEAGUE_ID, description="League id, EPL=39"),
    ) -> Dict[str, Any]:
        try:
            client = ApiClient.from_env()
            return client.standings(league=league, season=season)
        except ApiError as e:
            raise HTTPException(status_code=429, detail=str(e))

    @app.get("/defense-table")
    def defense_table(
        season: int = Query(..., description="Season year, e.g. 2024"),
        league: int = Query(EPL_LEAGUE_ID, description="League id, EPL=39"),
    ) -> Dict[str, Any]:
        try:
            client = ApiClient.from_env()
            teams_resp = client.teams(league=league, season=season)
            teams = teams_resp.get("response", [])
            rows = []
            for t in teams:
                team_id = t.get("team", {}).get("id")
                name = t.get("team", {}).get("name") or str(team_id)
                if not team_id:
                    continue
                stats = client.team_statistics(league=league, season=season, team=team_id)
                conceded = (
                    stats.get("response", {})
                    .get("goals", {})
                    .get("against", {})
                    .get("total", {})
                    .get("total")
                )
                rows.append({"team": name, "conceded": conceded})
            rows.sort(key=lambda r: (r["conceded"] is None, r["conceded"]))
            return {"season": season, "league": league, "rows": rows}
        except ApiError as e:
            raise HTTPException(status_code=429, detail=str(e))

    return app


def run() -> None:
    import uvicorn

    app = create_app()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


