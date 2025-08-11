from __future__ import annotations

import os
from fastapi import FastAPI

from app.api.routes_leagues import router as leagues_router
from app.api.routes_teams import router as teams_router
from app.api.routes_standings import router as standings_router
from app.api.routes_fixtures import router as fixtures_router
from app.api.routes_defense import router as defense_router


def create_app() -> FastAPI:
    app = FastAPI(title="EPL Fantasy Backend", version="0.1.0")
    
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}
    
    app.include_router(leagues_router)
    app.include_router(teams_router)
    app.include_router(standings_router)
    app.include_router(fixtures_router)
    app.include_router(defense_router)
    return app


def run() -> None:
    import uvicorn

    app = create_app()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)


