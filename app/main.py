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
from app.api.routes_player_stats import router as player_stats_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EPL Defense API",
        description="""
        # 🏆 English Premier League Statistics & Data API
        
        A comprehensive API for accessing English Premier League statistics, team data, player information, fixtures, and standings.
        
        ## 🚀 Features
        
        - **Teams**: Complete team information, statistics, and search functionality
        - **Fixtures**: Match schedules, results, and live game data
        - **Standings**: League tables and team rankings
        - **Players**: Individual player statistics and performance data
        - **Leagues**: League information and coverage details
        - **Data Ingestion**: Bulk data import from external sources
        
        ## 📊 Data Sources
        
        Powered by [API-Football](https://www.api-football.com/) with comprehensive caching and local database storage.
        
        ## 🔑 Authentication
        
        API key required for external data access. Set your `RAPIDAPI_KEY` or `APIFOOTBALL_API_KEY` in environment variables.
        
        ## 📈 Rate Limiting
        
        - **Free Tier**: 100 requests/day
        - **Premium Tier**: 7,500 requests/day
        
        ## 🗄️ Database
        
        Local SQLite database with automatic data ingestion and caching for improved performance.
        
        ## 📝 API Response Format
        
        All endpoints return standardized responses with the following structure:
        
        ```json
        {
          "get": "endpoint_name",
          "parameters": {"param": "value"},
          "errors": null,
          "results": 1,
          "paging": {"current": 1, "total": 1},
          "response": [...]
        }
        ```
        
        ## 🎯 Quick Start
        
        1. **Health Check**: `GET /health`
        2. **List Teams**: `GET /teams/?league=39&season=2025`
        3. **Team Statistics**: `GET /teams/40/statistics?season=2025`
        4. **Fixtures**: `GET /fixtures/?season=2025&league=39`
        5. **Standings**: `GET /standings/?league=39&season=2025`
        
        ## 🔗 External Links
        
        - [API Documentation](https://www.api-football.com/documentation-v3)
        - [EPL Official Site](https://www.premierleague.com/)
        """,
        version="1.0.0",
        contact={
            "name": "EPL Defense API Support",
            "url": "https://github.com/your-repo/epl-defense",
            "email": "support@epldefense.com"
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        servers=[
            {
                "url": "http://127.0.0.1:8001",
                "description": "Development server"
            },
            {
                "url": "https://api.epldefense.com",
                "description": "Production server"
            }
        ],
        tags_metadata=[
            {
                "name": "teams",
                "description": "Team-related operations including search, statistics, and player rosters."
            },
            {
                "name": "fixtures",
                "description": "Match fixtures, schedules, and live game data."
            },
            {
                "name": "standings",
                "description": "League tables, team rankings, and position data."
            },
            {
                "name": "leagues",
                "description": "League information, coverage details, and metadata."
            },
            {
                "name": "players",
                "description": "Individual player statistics, performance data, and rankings."
            },
            {
                "name": "ingestion",
                "description": "Data ingestion operations for bulk data import and synchronization."
            },
            {
                "name": "defense",
                "description": "Defensive statistics and analysis for teams and players."
            }
        ]
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
    app.include_router(player_stats_router)

    @app.get(
        "/health",
        summary="Health Check",
        description="Check the health status of the EPL Defense API service.",
        responses={
            200: {
                "description": "Service is healthy and running",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "ok",
                            "message": "EPL Defense API is running",
                            "timestamp": "2025-08-17T12:00:00Z",
                            "version": "1.0.0"
                        }
                    }
                }
            }
        }
    )
    def health_check():
        """Health check endpoint to verify API service status."""
        from datetime import datetime
        return {
            "status": "ok",
            "message": "EPL Defense API is running",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0"
        }

    return app


app = create_app()


def run() -> None:
    import uvicorn

    app = create_app()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)


