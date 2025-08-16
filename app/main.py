from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_leagues import router as leagues_router
from app.api.routes_teams import router as teams_router
from app.api.routes_standings import router as standings_router
from app.api.routes_fixtures import router as fixtures_router
from app.api.routes_defense import router as defense_router
from app.api.routes_team_stats import router as team_stats_router
from app.api.routes_ingestion import router as ingestion_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EPL Defense API",
        description="English Premier League statistics and data API",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(leagues_router)
    app.include_router(teams_router)
    app.include_router(standings_router)
    app.include_router(fixtures_router)
    app.include_router(defense_router)
    app.include_router(team_stats_router)
    app.include_router(ingestion_router)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


def run() -> None:
    import uvicorn

    app = create_app()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)


