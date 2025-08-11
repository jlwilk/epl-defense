from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel
from requests import Response
from requests_cache import CachedSession
from requests_cache.backends import FileCache

DEFAULT_BASE_URL = "https://v3.football.api-sports.io"
EPL_LEAGUE_ID = 39


class ApiError(Exception):
    pass


class RateLimitBudget(BaseModel):
    max_per_day: int = 100
    state_file: str = ".cache/budget.json"

    def _now_day(self) -> str:
        return time.strftime("%Y-%m-%d", time.gmtime())

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.state_file):
            return {"day": self._now_day(), "count": 0}
        try:
            import json

            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("day") != self._now_day():
                return {"day": self._now_day(), "count": 0}
            return data
        except Exception:
            return {"day": self._now_day(), "count": 0}

    def _save(self, data: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        import json

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def try_consume(self, cost: int = 1) -> bool:
        data = self._load()
        if data["count"] + cost > self.max_per_day:
            return False
        data["count"] += cost
        self._save(data)
        return True

    def refund(self, cost: int = 1) -> None:
        data = self._load()
        data["count"] = max(0, data.get("count", 0) - cost)
        self._save(data)

    def remaining(self) -> int:
        data = self._load()
        return max(0, self.max_per_day - data.get("count", 0))


@dataclass
class ApiClient:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    cache_name: str = ".cache/epl_cache"
    cache_expire_seconds: int = 24 * 60 * 60
    budget: RateLimitBudget = field(default_factory=RateLimitBudget)

    def __post_init__(self) -> None:
        os.makedirs(os.path.dirname(self.cache_name), exist_ok=True)
        backend = FileCache(self.cache_name)
        self.session: CachedSession = CachedSession(
            cache_name=self.cache_name,
            backend=backend,
            expire_after=self.cache_expire_seconds,
            allowable_methods=("GET",),
        )
        self.session.headers.update({
            "x-apisports-key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "epl-defense/0.1",
        })

    @classmethod
    def from_env(cls) -> "ApiClient":
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("APIFOOTBALL_API_KEY")
        if not api_key:
            raise ApiError("APIFOOTBALL_API_KEY is not set in environment or .env")
        base_url = os.getenv("APIFOOTBALL_BASE_URL", DEFAULT_BASE_URL)
        cache_name = os.getenv("CACHE_NAME", ".cache/epl_cache")
        cache_expire = int(os.getenv("CACHE_EXPIRE", str(24 * 60 * 60)))
        budget_max = int(os.getenv("BUDGET_MAX", "100"))
        budget_file = os.getenv("BUDGET_FILE", ".cache/budget.json")
        budget = RateLimitBudget(max_per_day=budget_max, state_file=budget_file)
        return cls(
            api_key=api_key,
            base_url=base_url,
            cache_name=cache_name,
            cache_expire_seconds=cache_expire,
            budget=budget,
        )

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        if method.upper() != "GET":
            raise ApiError("Only GET is supported")

        # Pre-consume budget, refund if served from cache
        if not self.budget.try_consume(1):
            raise ApiError(
                f"Daily request budget exceeded. Remaining={self.budget.remaining()}"
            )

        resp: Response = self.session.get(url, params=params)
        try:
            # requests-cache adds 'from_cache' attribute
            if getattr(resp, "from_cache", False):
                self.budget.refund(1)
        except Exception:
            pass
        if resp.status_code >= 400:
            raise ApiError(f"HTTP {resp.status_code}: {resp.text}")
        data = resp.json()
        # API-Football wraps data in { response: [], results: n, errors, paging }
        if "errors" in data and data["errors"]:
            raise ApiError(str(data["errors"]))
        return data

    # Convenience endpoint wrappers (documented at https://www.api-football.com/documentation-v3)
    # Leagues
    def leagues(self, **params: Any) -> Dict[str, Any]:
        return self._request("GET", "/leagues", params)

    def teams(self, **params: Any) -> Dict[str, Any]:
        return self._request("GET", "/teams", params)

    def fixtures(self, **params: Any) -> Dict[str, Any]:
        return self._request("GET", "/fixtures", params)

    def standings(self, league: int, season: int) -> Dict[str, Any]:
        return self._request("GET", "/standings", {"league": league, "season": season})

    def players(self, **params: Any) -> Dict[str, Any]:
        return self._request("GET", "/players", params)

    def health(self) -> Dict[str, Any]:
        # Simple lightweight endpoint; use status or time zone as a proxy health
        return self._request("GET", "/status")

    def team_statistics(self, league: int, season: int, team: int) -> Dict[str, Any]:
        return self._request(
            "GET",
            "/teams/statistics",
            {"league": league, "season": season, "team": team},
        )


