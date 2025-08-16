from __future__ import annotations

import os
from typing import Any, Dict

import httpx
from urllib.parse import urlparse

from app.config import get_settings


class ApiClientV3:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.base_url.rstrip("/")
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        headers: Dict[str, str] = {"Accept": "application/json"}
        if rapidapi_key:
            # Use RapidAPI headers
            host = urlparse(self.base_url).netloc or "v3.football.api-sports.io"
            headers.update({
                "x-rapidapi-key": rapidapi_key,
                "x-rapidapi-host": host,
                "User-Agent": "epl-fastapi/0.1",
            })
        else:
            # Use direct API-Football key
            headers.update({
                "x-apisports-key": settings.api_key or "",
                "User-Agent": "epl-fastapi/0.1",
            })
        self.headers = headers
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, timeout=30)

    def get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        resp = self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()


