from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, Path, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ingestion import DataIngestionService
from app.schemas import IngestionResponse, IngestionStatusResponse
from app.config import get_settings

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post(
    "/league/{league_id}/season/{season}",
    summary="Ingest League Data",
    description="Trigger data ingestion for a specific league and season.",
    response_model=IngestionResponse,
    responses={
        200: {
            "description": "Ingestion started successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Data ingestion started for Premier League 2025",
                        "league_id": 39,
                        "season": 2025,
                        "status": "started",
                        "task_id": "task_12345"
                    }
                }
            }
        }
    }
)
def ingest_league_data(
    league_id: int = Path(..., description="League ID"),
    season: int = Path(..., description="Season"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    """Trigger data ingestion for a specific league and season."""
    ingestion_service = DataIngestionService()
    
    # Start ingestion in background
    background_tasks.add_task(ingestion_service.ingest_league_data, league_id, season)
    
    return IngestionResponse(
        message=f"Data ingestion started for league {league_id} season {season}",
        league_id=league_id,
        season=season,
        status="started",
        task_id="background_task"
    )


@router.get(
    "/status/{league_id}/{season}",
    summary="Get Ingestion Status",
    description="Get the current ingestion status for a league/season.",
    response_model=IngestionStatusResponse,
    responses={
        200: {
            "description": "Current ingestion status",
            "content": {
                "application/json": {
                    "example": {
                        "league_id": 39,
                        "season": 2025,
                        "status": "completed",
                        "progress": {
                            "current_step": "fixtures",
                            "total_steps": 4,
                            "step_progress": 100
                        },
                        "counts": {
                            "leagues": 1,
                            "teams": 20,
                            "players": 500,
                            "fixtures": 380
                        },
                        "last_updated": "2025-08-17T12:00:00Z"
                    }
                }
            }
        }
    }
)
def get_ingestion_status(
    league_id: int = Path(..., description="League ID"),
    season: int = Path(..., description="Season"),
    db: Session = Depends(get_db),
) -> IngestionStatusResponse:
    """Get the current ingestion status for a league/season."""
    try:
        ingestion_service = DataIngestionService()
        status = ingestion_service.get_ingestion_status(league_id, season)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/epl/2025",
    summary="Ingest EPL 2025",
    description="Quick endpoint to ingest EPL 2025 data.",
    response_model=IngestionResponse,
    responses={
        200: {
            "description": "EPL 2025 ingestion started",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Data ingestion started for Premier League 2025",
                        "league_id": 39,
                        "season": 2025,
                        "status": "started",
                        "task_id": "task_12345"
                    }
                }
            }
        }
    }
)
def ingest_epl_2025(
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
) -> IngestionResponse:
    """Quick endpoint to ingest EPL 2025 data."""
    return ingest_league_data(39, 2025, background_tasks, db)


@router.get(
    "/health",
    summary="Ingestion Health",
    description="Health check for ingestion service.",
    responses={
        200: {
            "description": "Ingestion service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "message": "Ingestion service is running",
                        "timestamp": "2025-08-17T12:00:00Z"
                    }
                }
            }
        }
    }
)
def ingestion_health() -> dict[str, Any]:
    """Health check for ingestion service."""
    from datetime import datetime
    return {
        "status": "healthy",
        "message": "Ingestion service is running",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
