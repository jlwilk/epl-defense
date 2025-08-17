from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse

from app.services.ingestion import DataIngestionService
from app.config import get_settings

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/league/{league_id}/season/{season}")
async def ingest_league_data(
    league_id: int,
    season: int,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Trigger data ingestion for a specific league and season."""
    try:
        # Start ingestion in background
        ingestion_service = DataIngestionService()
        background_tasks.add_task(
            ingestion_service.ingest_league_data,
            league_id,
            season
        )
        
        return {
            "message": f"Data ingestion started for league {league_id}, season {season}",
            "league_id": league_id,
            "season": season,
            "status": "started",
            "note": "Check /ingestion/status/{league_id}/{season} for progress"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start ingestion: {str(e)}")


@router.get("/status/{league_id}/{season}")
async def get_ingestion_status(
    league_id: int,
    season: int
) -> Dict[str, Any]:
    """Get the current ingestion status for a league/season."""
    try:
        ingestion_service = DataIngestionService()
        status = ingestion_service.get_ingestion_status(league_id, season)
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.post("/epl/2025")
async def ingest_epl_2025(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Quick endpoint to ingest EPL 2025 data."""
    settings = get_settings()
    league_id = settings.league_id_default
    season = settings.season_default
    
    try:
        # Start ingestion in background
        ingestion_service = DataIngestionService()
        background_tasks.add_task(
            ingestion_service.ingest_league_data,
            league_id,
            season
        )
        
        return {
            "message": f"EPL 2025 data ingestion started",
            "league_id": league_id,
            "season": season,
            "status": "started",
            "note": "Check /ingestion/status/{league_id}/{season} for progress"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start EPL ingestion: {str(e)}")


@router.get("/health")
async def ingestion_health() -> Dict[str, Any]:
    """Health check for ingestion service."""
    return {
        "status": "healthy",
        "service": "data-ingestion",
        "timestamp": "2025-01-14T11:00:00Z"
    }
