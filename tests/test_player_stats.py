import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.schemas import ApiResponse


class TestPlayerStatsEndpoints:
    """Test suite for player statistics endpoints."""
    
    def test_get_player_statistics_success(self, client, mock_player_stats_response):
        """Test successful player statistics retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            assert data["parameters"]["player"] == "152982"
            # Season should use default from settings
    
    def test_get_player_statistics_with_season(self, client, mock_player_stats_response):
        """Test player statistics with explicit season parameter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982?season=2024")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2024, 39)  # 39 is default league
    
    def test_get_player_statistics_with_league(self, client, mock_player_stats_response):
        """Test player statistics with league parameter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982?league=40")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2025, 40)  # 2025 is default season
    
    def test_get_player_statistics_with_both_params(self, client, mock_player_stats_response):
        """Test player statistics with both season and league parameters."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982?season=2024&league=40")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2024, 40)
    
    def test_get_player_statistics_defaults(self, client, mock_player_stats_response):
        """Test that player statistics uses environment defaults when no parameters provided."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982")
            assert response.status_code == 200
            
            # Verify that the API client was called with the default parameters
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2025, 39)  # Defaults from settings
    
    def test_get_player_statistics_invalid_player_id(self, client):
        """Test with invalid player ID format."""
        response = client.get("/player-stats/player/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_get_player_statistics_api_error(self, client):
        """Test handling of API errors."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.side_effect = Exception("API Error")
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982")
            assert response.status_code == 502
            assert "API Error" in response.json()["detail"]
    
    def test_get_league_player_statistics_success(self, client, mock_league_player_stats_response):
        """Test successful league player statistics retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_league_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/league/39")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_league.assert_called_once_with(39, 2025, None)  # 2025 is default season
    
    def test_get_league_player_statistics_with_season(self, client, mock_league_player_stats_response):
        """Test league player statistics with explicit season parameter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_league_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/league/39?season=2024")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_league.assert_called_once_with(39, 2024, None)
    
    def test_get_league_player_statistics_with_team(self, client, mock_league_player_stats_response):
        """Test league player statistics with team filter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_league_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/league/39?team=33")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_league.assert_called_once_with(39, 2025, 33)  # 2025 is default season
    
    def test_get_team_player_statistics_success(self, client, mock_team_player_stats_response):
        """Test successful team player statistics retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_team.return_value = mock_team_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/team/33")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_team.assert_called_once_with(33, 2025, 39)  # Defaults from settings
    
    def test_get_team_player_statistics_with_league(self, client, mock_team_player_stats_response):
        """Test team player statistics with league filter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_team.return_value = mock_team_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/team/33?league=40")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_team.assert_called_once_with(33, 2025, 40)  # 2025 is default season
    
    def test_get_team_player_statistics_with_season(self, client, mock_team_player_stats_response):
        """Test team player statistics with season filter."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_team.return_value = mock_team_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/team/33?season=2024")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_team.assert_called_once_with(33, 2024, 39)  # 39 is default league
    
    def test_get_team_player_statistics_with_both_params(self, client, mock_team_player_stats_response):
        """Test team player statistics with both season and league filters."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_team.return_value = mock_team_player_stats_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/team/33?season=2024&league=40")
            assert response.status_code == 200
            
            # Verify that the API client was called with the correct parameters
            mock_instance.get_player_statistics_by_team.assert_called_once_with(33, 2024, 40)
    
    def test_get_player_seasons_success(self, client, mock_player_seasons_response):
        """Test successful player seasons retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_seasons.return_value = mock_player_seasons_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/player/152982/seasons")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players/seasons"
            assert data["parameters"]["player"] == "152982"
    
    def test_get_player_countries_success(self, client, mock_player_countries_response):
        """Test successful player countries retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_countries.return_value = mock_player_countries_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/countries")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players/countries"
    
    def test_search_players_success(self, client, mock_player_search_response):
        """Test successful player search."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.search_players.return_value = mock_player_search_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/search?search=Haaland")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            assert data["parameters"]["search"] == "Haaland"
    
    def test_search_players_with_filters(self, client, mock_player_search_response):
        """Test player search with league and season filters."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.search_players.return_value = mock_player_search_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/search?search=Haaland&league=39&season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["parameters"]["search"] == "Haaland"
            assert data["parameters"]["league"] == "39"
            assert data["parameters"]["season"] == "2025"
    
    def test_search_players_defaults(self, client, mock_player_search_response):
        """Test that player search uses environment defaults when no season/league provided."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.search_players.return_value = mock_player_search_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/search?search=Haaland")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            assert data["parameters"]["search"] == "Haaland"
            # Should use defaults from settings for season and league
    
    def test_get_top_scorers_success(self, client, mock_top_scorers_response):
        """Test successful top scorers retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_top_scorers_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/top-scorers")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            # Should use defaults from settings for league and season
    
    def test_get_top_scorers_with_limit(self, client, mock_top_scorers_response):
        """Test top scorers with custom limit."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_top_scorers_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/top-scorers?limit=5")
            assert response.status_code == 200
            
            data = response.json()
            # The endpoint processes the data and returns the processed result
            # so we check that the response has the expected structure
            assert "response" in data
            assert "top_scorers" in data
    
    def test_get_top_scorers_invalid_limit(self, client):
        """Test top scorers with invalid limit."""
        response = client.get("/player-stats/top-scorers?limit=0")
        assert response.status_code == 422  # Validation error
        
        response = client.get("/player-stats/top-scorers?limit=51")
        assert response.status_code == 422  # Validation error
    
    def test_get_top_assists_success(self, client, mock_top_assists_response):
        """Test successful top assists retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_top_assists_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/top-assists")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            # Should use defaults from settings for league and season
    
    def test_get_defensive_leaders_success(self, client, mock_defensive_leaders_response):
        """Test successful defensive leaders retrieval."""
        with patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get_player_statistics_by_league.return_value = mock_defensive_leaders_response
            mock_client.return_value = mock_instance
            
            response = client.get("/player-stats/defensive-leaders")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "players"
            # Should use defaults from settings for league and season
    
    def test_environment_defaults_usage(self, client, mock_player_stats_response):
        """Test that environment defaults are actually used when parameters aren't provided."""
        with patch('app.api.routes_player_stats.get_settings') as mock_get_settings, \
             patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            
            # Mock settings to return specific defaults
            mock_settings = MagicMock()
            mock_settings.season_default = 2024
            mock_settings.league_id_default = 40
            mock_get_settings.return_value = mock_settings
            
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            # Call endpoint without parameters
            response = client.get("/player-stats/player/152982")
            assert response.status_code == 200
            
            # Verify that the mocked settings were used
            mock_get_settings.assert_called_once()
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2024, 40)
    
    def test_environment_defaults_with_explicit_params(self, client, mock_player_stats_response):
        """Test that explicit parameters override environment defaults."""
        with patch('app.api.routes_player_stats.get_settings') as mock_get_settings, \
             patch('app.api.routes_player_stats.ApiClientV3') as mock_client:
            
            # Mock settings to return specific defaults
            mock_settings = MagicMock()
            mock_settings.season_default = 2024
            mock_settings.league_id_default = 40
            mock_get_settings.return_value = mock_settings
            
            mock_instance = MagicMock()
            mock_instance.get_player_statistics.return_value = mock_player_stats_response
            mock_client.return_value = mock_instance
            
            # Call endpoint with explicit parameters
            response = client.get("/player-stats/player/152982?season=2023&league=39")
            assert response.status_code == 200
            
            # Verify that explicit parameters were used instead of defaults
            mock_instance.get_player_statistics.assert_called_once_with(152982, 2023, 39)
