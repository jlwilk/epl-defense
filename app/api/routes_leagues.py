from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/")
def list_leagues() -> Dict[str, Any]:
    try:
        client = ApiClientV3()
        data = client.get("/leagues")
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


