import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.schemas import ApiResponse, TeamStatisticsApiResponse


class TestTeamEndpoints:
    """Test suite for team endpoints."""
    
    def test_list_teams_success(self, client, mock_api_response):
        """Test successful team listing."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "test_endpoint"
            assert data["results"] == 1
            assert len(data["response"]) == 1
            assert data["response"][0]["name"] == "Test"
    
    def test_list_teams_with_season(self, client, mock_api_response):
        """Test team listing with season parameter."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["parameters"] = {"season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/?season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["parameters"]["season"] == "2025"
    
    def test_get_team_success(self, client, mock_api_response):
        """Test successful team retrieval."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["parameters"] = {"id": "33"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33")
            assert response.status_code == 200
            
            data = response.json()
            assert data["parameters"]["id"] == "33"
    
    def test_get_team_statistics_success(self, client, mock_team_statistics_response):
        """Test successful team statistics retrieval."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_team_statistics_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/statistics?season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/statistics"
            assert data["parameters"]["team"] == "33"
            assert data["parameters"]["season"] == "2025"
            
            # Validate response structure
            team_stats = data["response"]
            assert "league" in team_stats
            assert "team" in team_stats
            assert "fixtures" in team_stats
            assert "goals" in team_stats
            assert team_stats["team"]["name"] == "Manchester United"
    
    def test_get_team_statistics_defaults(self, client, mock_team_statistics_response):
        """Test team statistics with default season and league."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_team_statistics_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/statistics")
            assert response.status_code == 200
            
            data = response.json()
            # Should use defaults from settings
            assert data["parameters"]["season"] == "2025"
            assert data["parameters"]["league"] == "39"
    
    def test_get_team_statistics_validation(self, client, mock_team_statistics_response):
        """Test that team statistics response validates against schema."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_team_statistics_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/statistics?season=2025")
            assert response.status_code == 200
            
            # This should not raise validation errors
            data = response.json()
            # Validate the response structure matches our schema
            assert "response" in data
            assert isinstance(data["response"], dict)
            assert "league" in data["response"]
            assert "team" in data["response"]
    
    def test_get_team_seasons(self, client, mock_api_response):
        """Test team seasons endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams/seasons"
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/seasons")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/seasons"
    
    def test_get_team_countries(self, client, mock_api_response):
        """Test team countries endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams/countries"
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/countries")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/countries"
    
    def test_get_team_leagues(self, client, mock_api_response):
        """Test team leagues endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams/leagues"
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/leagues")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/leagues"
    
    def test_get_team_fixtures(self, client, mock_api_response):
        """Test team fixtures endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams/fixtures"
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/fixtures?season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/fixtures"
    
    def test_get_team_players(self, client, mock_api_response):
        """Test team players endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams/players"
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/33/players?season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams/players"
    
    def test_search_teams(self, client, mock_api_response):
        """Test team search endpoint."""
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "teams"
            mock_api_response["parameters"] = {"search": "Manchester"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/search?search=Manchester")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "teams"
            assert data["parameters"]["search"] == "Manchester"
    
    def test_team_endpoint_errors_handling(self, client):
        """Test that empty errors and paging are converted to None."""
        mock_response = {
            "get": "teams",
            "parameters": {},
            "errors": [],  # Empty list
            "results": 0,
            "paging": {},  # Empty dict
            "response": []
        }
        
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/")
            assert response.status_code == 200
            
            data = response.json()
            # Should be converted to None
            assert data["errors"] is None
            assert data["paging"] is None
    
    def test_parameters_field_validation_fix(self, client):
        """Test that empty parameters list is converted to empty dict."""
        # This simulates the API-Football response where parameters is an empty list
        mock_response = {
            "get": "teams",
            "parameters": [],  # Empty list - this was causing the error
            "errors": None,
            "results": 20,
            "paging": {"current": 1, "total": 1},
            "response": []
        }
        
        with patch('app.api.routes_teams.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/teams/")
            assert response.status_code == 200
            
            data = response.json()
            # The fix should convert [] to {}
            assert data["parameters"] == {}
            assert isinstance(data["parameters"], dict)
    
    def test_invalid_team_id(self, client):
        """Test invalid team ID handling."""
        response = client.get("/teams/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_team_statistics_invalid_season(self, client):
        """Test invalid season parameter handling."""
        response = client.get("/teams/33/statistics?season=invalid")
        assert response.status_code == 422  # Validation error

