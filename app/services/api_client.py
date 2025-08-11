from __future__ import annotations

import httpx
from typing import Any, Dict

from app.config import get_settings


class ApiClientV3:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.base_url.rstrip("/")
        self.headers = {"x-apisports-key": settings.api_key or "", "Accept": "application/json"}
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers, timeout=30)

    def get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        resp = self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()


