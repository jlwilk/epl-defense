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

    def get_fixture_players(self, fixture_id: int) -> Dict[str, Any]:
        """Get player statistics for a specific fixture.
        
        Args:
            fixture_id: The ID of the fixture
            
        Returns:
            Dictionary containing player statistics for both teams
        """
        return self.get(f"/fixtures/players", params={"fixture": fixture_id})

    def get_player_statistics(self, player_id: int, season: int, league: int | None = None) -> Dict[str, Any]:
        """Get player statistics for a specific player and season.
        
        Args:
            player_id: The ID of the player
            season: The season year
            league: Optional league ID to filter by
            
        Returns:
            Dictionary containing player statistics for the season
        """
        params = {"player": player_id, "season": season}
        if league:
            params["league"] = league
        return self.get("/players", params=params)

    def get_player_statistics_by_league(self, league: int, season: int, team: int | None = None) -> Dict[str, Any]:
        """Get player statistics for a league and season, optionally filtered by team.
        
        Args:
            league: The league ID
            season: The season year
            team: Optional team ID to filter by
            
        Returns:
            Dictionary containing player statistics for the league/season
        """
        params = {"league": league, "season": season}
        if team:
            params["team"] = team
        return self.get("/players", params=params)

    def get_player_statistics_by_team(self, team: int, season: int, league: int | None = None) -> Dict[str, Any]:
        """Get player statistics for a specific team and season.
        
        Args:
            team: The team ID
            season: The season year
            league: Optional league ID to filter by
            
        Returns:
            Dictionary containing player statistics for the team
        """
        params = {"team": team, "season": season}
        if league:
            params["league"] = league
        return self.get("/players", params=params)

    def get_player_seasons(self, player_id: int) -> Dict[str, Any]:
        """Get all seasons for a specific player.
        
        Args:
            player_id: The ID of the player
            
        Returns:
            Dictionary containing all seasons the player has participated in
        """
        return self.get("/players/seasons", params={"player": player_id})

    def get_player_countries(self) -> Dict[str, Any]:
        """Get all available player countries.
        
        Returns:
            Dictionary containing all available player countries
        """
        return self.get("/players/countries")

    def search_players(self, search: str, league: int | None = None, season: int | None = None) -> Dict[str, Any]:
        """Search for players by name.
        
        Args:
            search: Player name to search for
            league: Optional league ID to filter by
            season: Optional season year to filter by
            
        Returns:
            Dictionary containing matching players
        """
        params = {"search": search}
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        return self.get("/players", params=params)


