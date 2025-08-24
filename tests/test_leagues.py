import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestLeagueEndpoints:
    """Test suite for league endpoints."""
    
    def test_list_leagues_success(self, client, mock_api_response):
        """Test successful league listing."""
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "leagues"
            mock_api_response["parameters"] = {"season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/?season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "leagues"
            assert data["parameters"]["season"] == "2025"
    
    def test_list_leagues_defaults(self, client, mock_api_response):
        """Test league listing with default parameters."""
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "leagues"
            mock_api_response["parameters"] = {"season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/")
            assert response.status_code == 200
            
            data = response.json()
            # Should use defaults from settings
            assert data["parameters"]["season"] == "2025"
    
    def test_get_league_by_id_success(self, client, mock_api_response):
        """Test successful league retrieval by ID."""
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "leagues"
            mock_api_response["parameters"] = {"id": "39"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/39")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "leagues"
            assert data["parameters"]["id"] == "39"
    
    def test_get_league_by_country_success(self, client, mock_api_response):
        """Test successful league retrieval by country."""
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "leagues"
            mock_api_response["parameters"] = {"country": "England"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/country/England")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "leagues"
            assert data["parameters"]["country"] == "England"
    
    def test_parameters_field_validation_fix(self, client):
        """Test that empty parameters list is converted to empty dict."""
        # This simulates the API-Football response where parameters is an empty list
        mock_response = {
            "get": "leagues",
            "parameters": [],  # Empty list - this was causing the error
            "errors": None,
            "results": 1189,
            "paging": {"current": 1, "total": 1},
            "response": []
        }
        
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/")
            assert response.status_code == 200
            
            data = response.json()
            # The fix should convert [] to {}
            assert data["parameters"] == {}
            assert isinstance(data["parameters"], dict)
    
    def test_all_league_endpoints_handle_empty_parameters(self, client):
        """Test that all league endpoints handle empty parameters correctly."""
        # Test data with empty parameters list
        mock_response = {
            "get": "leagues",
            "parameters": [],  # Empty list
            "errors": None,
            "results": 1,
            "paging": None,
            "response": []
        }
        
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            # Test all endpoints
            endpoints = [
                "/leagues/",
                "/leagues/39",
                "/leagues/country/England",
                "/leagues/name/Premier League"
            ]
            
            for endpoint in endpoints:
                response = client.get(endpoint)
                assert response.status_code == 200
                
                data = response.json()
                # All should convert [] to {}
                assert data["parameters"] == {}
                assert isinstance(data["parameters"], dict)
    
    def test_get_league_by_name_success(self, client, mock_api_response):
        """Test successful league retrieval by name."""
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "leagues"
            mock_api_response["parameters"] = {"name": "Premier League"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/name/Premier League")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "leagues"
            assert data["parameters"]["name"] == "Premier League"
    
    def test_league_endpoint_errors_handling(self, client):
        """Test that empty errors and paging are converted to None."""
        mock_response = {
            "get": "leagues",
            "parameters": {"season": "2025"},
            "errors": [],  # Empty list
            "results": 0,
            "paging": {},  # Empty dict
            "response": []
        }
        
        with patch('app.api.routes_leagues.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/leagues/")
            assert response.status_code == 200
            
            data = response.json()
            # Should be converted to None
            assert data["errors"] is None
            assert data["paging"] is None
    
    def test_invalid_league_id(self, client):
        """Test invalid league ID handling."""
        response = client.get("/leagues/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_season_parameter(self, client):
        """Test invalid season parameter handling."""
        response = client.get("/standings/?season=invalid")
        assert response.status_code == 422  # Validation error


class TestStandingsEndpoints:
    """Test suite for standings endpoints."""
    
    def test_get_standings_success(self, client, mock_api_response):
        """Test successful standings retrieval."""
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "standings"
            mock_api_response["parameters"] = {"league": "39", "season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/?league=39&season=2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "standings"
            assert data["parameters"]["league"] == "39"
            assert data["parameters"]["season"] == "2025"
    
    def test_get_standings_defaults(self, client, mock_api_response):
        """Test standings with default parameters."""
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "standings"
            mock_api_response["parameters"] = {"league": "39", "season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/?league=39")
            assert response.status_code == 200
            
            data = response.json()
            # Should use defaults from settings
            assert data["parameters"]["season"] == "2025"
    
    def test_get_standings_by_league_id_success(self, client, mock_api_response):
        """Test successful standings retrieval by league ID."""
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "standings"
            mock_api_response["parameters"] = {"league": "39", "season": "2025"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/39")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "standings"
            assert data["parameters"]["league"] == "39"
            assert data["parameters"]["season"] == "2025"
    
    def test_get_standings_by_league_id_and_season_success(self, client, mock_api_response):
        """Test successful standings retrieval by league ID and season."""
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "standings"
            mock_api_response["parameters"] = {"league": "39", "season": "2024"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/39/2024")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "standings"
            assert data["parameters"]["league"] == "39"
            assert data["parameters"]["season"] == "2024"
    
    def test_standings_endpoint_errors_handling(self, client):
        """Test that empty errors and paging are converted to None."""
        mock_response = {
            "get": "standings",
            "parameters": {"league": "39", "season": "2025"},
            "errors": [],  # Empty list
            "results": 0,
            "paging": {},  # Empty dict
            "response": []
        }
        
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/?league=39&season=2025")
            assert response.status_code == 200
            
            data = response.json()
            # Should be converted to None
            assert data["errors"] is None
            assert data["paging"] is None
    
    def test_invalid_league_id_in_standings(self, client):
        """Test invalid league ID handling in standings."""
        response = client.get("/standings/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_season_in_standings(self, client):
        """Test invalid season parameter handling in standings."""
        response = client.get("/standings/?season=invalid")
        assert response.status_code == 422  # Validation error
    
    def test_standings_required_parameters(self, client):
        """Test that standings endpoints require necessary parameters."""
        # Test that standings require league parameter
        with patch('app.api.routes_standings.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_response = {
                "get": "standings",
                "parameters": {"league": "39", "season": "2025"},
                "errors": None,
                "results": 0,
                "paging": None,
                "response": []
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/standings/?league=39")
            assert response.status_code == 200
            
            data = response.json()
            # Should always include league
            assert "league" in data["parameters"]
            # Should use default season
            assert data["parameters"]["season"] == "2025"

