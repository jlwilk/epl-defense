import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestFixtureEndpoints:
    """Test suite for fixture endpoints."""
    
    def test_list_fixtures_success(self, client, mock_api_response):
        """Test successful fixture listing."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"season": "2025", "league": "39"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/?season=2025&league=39")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures"
            assert data["parameters"]["season"] == "2025"
            assert data["parameters"]["league"] == "39"
    
    def test_list_fixtures_defaults(self, client, mock_api_response):
        """Test fixture listing with default parameters."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"season": "2025", "league": "39"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/")
            assert response.status_code == 200
            
            data = response.json()
            # Should use defaults from settings
            assert data["parameters"]["season"] == "2025"
            assert data["parameters"]["league"] == "39"
    
    def test_get_live_fixtures_success(self, client, mock_api_response):
        """Test successful live fixtures retrieval."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"season": "2025", "league": "39", "live": "all"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/live")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures"
            assert data["parameters"]["live"] == "all"
    
    def test_get_live_fixtures_defaults(self, client, mock_api_response):
        """Test live fixtures with default parameters."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"season": "2025", "league": "39", "live": "all"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/live")
            assert response.status_code == 200
            
            data = response.json()
            # Should use defaults from settings
            assert data["parameters"]["season"] == "2025"
            assert data["parameters"]["league"] == "39"
    
    def test_get_fixture_by_id_success(self, client, mock_api_response):
        """Test successful fixture retrieval by ID."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"id": "12345"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/12345")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures"
            assert data["parameters"]["id"] == "12345"
    
    def test_get_head_to_head_success(self, client, mock_api_response):
        """Test successful head-to-head fixture retrieval."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures/headtohead"
            mock_api_response["parameters"] = {"h2h": "33-40"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/head-to-head?h2h=33-40")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures/headtohead"
            assert data["parameters"]["h2h"] == "33-40"
    
    def test_get_fixtures_by_date_success(self, client, mock_api_response):
        """Test successful fixtures retrieval by date."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"date": "2025-01-15"}
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/date/2025-01-15")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures"
            assert data["parameters"]["date"] == "2025-01-15"
    
    def test_get_fixtures_by_team_success(self, client, mock_api_response):
        """Test successful fixtures retrieval by team."""
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_api_response["get"] = "fixtures"
            mock_api_response["parameters"] = {"team": "33"}
            mock_instance.get.return_value = mock_api_response
            mock_instance.get.return_value = mock_api_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/team/33")
            assert response.status_code == 200
            
            data = response.json()
            assert data["get"] == "fixtures"
            assert data["parameters"]["team"] == "33"
    
    def test_fixture_endpoint_errors_handling(self, client):
        """Test that empty errors and paging are converted to None."""
        mock_response = {
            "get": "fixtures",
            "parameters": {"season": "2025", "league": "39"},
            "errors": [],  # Empty list
            "results": 0,
            "paging": {},  # Empty dict
            "response": []
        }
        
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/")
            assert response.status_code == 200
            
            data = response.json()
            # Should be converted to None
            assert data["errors"] is None
            assert data["paging"] is None
    
    def test_invalid_fixture_id(self, client):
        """Test invalid fixture ID handling."""
        response = client.get("/fixtures/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_date_format(self, client):
        """Test invalid date format handling."""
        # Note: FastAPI doesn't validate date format for path parameters
        # The external API will handle validation
        response = client.get("/fixtures/date/invalid-date")
        assert response.status_code == 200  # FastAPI accepts any string
    
    def test_invalid_team_id_in_fixtures(self, client):
        """Test invalid team ID in fixtures endpoint."""
        response = client.get("/fixtures/team/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_fixtures_route_ordering(self, client):
        """Test that specific routes are matched before dynamic routes."""
        # This test ensures that /live comes before /{fixture_id}
        # The route ordering should prevent "live" from being parsed as a fixture ID
        
        # Test that /live works
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_response = {
                "get": "fixtures",
                "parameters": {"season": "2025", "league": "39", "live": "all"},
                "errors": None,
                "results": 0,
                "paging": None,
                "response": []
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/live")
            assert response.status_code == 200
            assert response.json()["parameters"]["live"] == "all"
    
    def test_fixtures_required_parameters(self, client):
        """Test that fixtures endpoints require necessary parameters."""
        # Test that /fixtures/live includes required parameters
        with patch('app.api.routes_fixtures.ApiClientV3') as mock_client:
            mock_instance = MagicMock()
            mock_response = {
                "get": "fixtures",
                "parameters": {"season": "2025", "league": "39", "live": "all"},
                "errors": None,
                "results": 0,
                "paging": None,
                "response": []
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value = mock_instance
            
            response = client.get("/fixtures/live")
            assert response.status_code == 200
            
            data = response.json()
            # Should always include season and league
            assert "season" in data["parameters"]
            assert "league" in data["parameters"]
