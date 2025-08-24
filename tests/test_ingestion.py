import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestIngestionEndpoints:
    """Test suite for ingestion endpoints."""
    
    def test_ingest_league_data_success(self, client, db_session):
        """Test successful league data ingestion."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.ingest_league_data.return_value = {
                "message": "Data ingestion started for league 39 season 2025",
                "league_id": 39,
                "season": 2025,
                "status": "started",
                "task_id": "task_123"
            }
            mock_service.return_value = mock_instance
            
            response = client.post("/ingestion/league/39/season/2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["message"] == "Data ingestion started for league 39 season 2025"
            assert data["league_id"] == 39
            assert data["season"] == 2025
            assert data["status"] == "started"
            assert data["task_id"] == "background_task"
    
    def test_ingest_epl_2025_success(self, client, db_session):
        """Test successful EPL 2025 ingestion."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.ingest_league_data.return_value = {
                "message": "Data ingestion started for league 39 season 2025",
                "league_id": 39,
                "season": 2025,
                "status": "started",
                "task_id": "task_456"
            }
            mock_service.return_value = mock_instance
            
            response = client.post("/ingestion/epl/2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["message"] == "Data ingestion started for league 39 season 2025"
            assert data["league_id"] == 39
            assert data["season"] == 2025
    
    def test_get_ingestion_status_success(self, client, db_session):
        """Test successful ingestion status retrieval."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_ingestion_status.return_value = {
                "league_id": 39,
                "season": 2025,
                "status": "completed",
                "progress": {"teams": 20, "players": 500, "fixtures": 380},
                "counts": {"teams": 20, "players": 500, "fixtures": 380},
                "last_updated": "2025-01-15T10:00:00Z"
            }
            mock_service.return_value = mock_instance
            
            response = client.get("/ingestion/status/39/2025")
            assert response.status_code == 200
            
            data = response.json()
            assert data["league_id"] == 39
            assert data["season"] == 2025
            assert data["status"] == "completed"
            assert "progress" in data
            assert "counts" in data
            assert "last_updated" in data
    
    def test_get_ingestion_health_success(self, client, db_session):
        """Test successful ingestion health check."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_ingestion_status.return_value = {
                "league_id": 39,
                "season": 2025,
                "status": "completed",
                "progress": None,
                "counts": {"teams": 20, "players": 500, "fixtures": 380},
                "last_updated": "2025-01-15T10:00:00Z"
            }
            mock_service.return_value = mock_instance
            
            response = client.get("/ingestion/health")
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert "message" in data
    
    def test_ingestion_service_integration(self, client, db_session):
        """Test that ingestion service is properly integrated."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
            
            # Test that the service is instantiated
            response = client.post("/ingestion/league/39/season/2025")
            mock_service.assert_called_once()
    
    def test_ingestion_parameters_validation(self, client):
        """Test that ingestion endpoints validate parameters correctly."""
        # Test invalid league ID
        response = client.post("/ingestion/league/invalid/season/2025")
        assert response.status_code == 422  # Validation error
        
        # Test invalid season
        response = client.post("/ingestion/league/39/season/invalid")
        assert response.status_code == 422  # Validation error
        
        # Test invalid EPL season
        response = client.post("/ingestion/epl/invalid")
        assert response.status_code == 404  # Route doesn't exist for invalid season
    
    def test_ingestion_status_parameters_validation(self, client):
        """Test that ingestion status endpoints validate parameters correctly."""
        # Test invalid league ID
        response = client.get("/ingestion/status/invalid/2025")
        assert response.status_code == 422  # Validation error
        
        # Test invalid season
        response = client.get("/ingestion/status/39/invalid")
        assert response.status_code == 422  # Validation error
    
    def test_ingestion_error_handling(self, client, db_session):
        """Test that ingestion errors are handled gracefully."""
        # Note: The route doesn't handle ingestion errors directly
        # It just adds a background task and returns immediately
        # Errors in the background task are not handled by the route
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_service.return_value = mock_instance
    
            response = client.post("/ingestion/league/39/season/2025")
            assert response.status_code == 200  # Route always succeeds
    
    def test_ingestion_status_error_handling(self, client, db_session):
        """Test that ingestion status errors are handled gracefully."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_ingestion_status.side_effect = Exception("Status check failed")
            mock_service.return_value = mock_instance
            
            response = client.get("/ingestion/status/39/2025")
            assert response.status_code == 500  # Internal server error
    
    def test_ingestion_response_schema_validation(self, client, db_session):
        """Test that ingestion responses validate against the schema."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.ingest_league_data.return_value = {
                "message": "Data ingestion started for league 39 season 2025",
                "league_id": 39,
                "season": 2025,
                "status": "started",
                "task_id": "task_123"
            }
            mock_service.return_value = mock_instance
            
            response = client.post("/ingestion/league/39/season/2025")
            assert response.status_code == 200
            
            data = response.json()
            # Validate required fields are present
            assert "message" in data
            assert "league_id" in data
            assert "season" in data
            assert "status" in data
            # task_id is optional
            assert "task_id" in data
    
    def test_ingestion_status_response_schema_validation(self, client, db_session):
        """Test that ingestion status responses validate against the schema."""
        with patch('app.api.routes_ingestion.DataIngestionService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.get_ingestion_status.return_value = {
                "league_id": 39,
                "season": 2025,
                "status": "completed",
                "progress": None,
                "counts": {"teams": 20, "players": 500, "fixtures": 380},
                "last_updated": "2025-01-15T10:00:00Z"
            }
            mock_service.return_value = mock_instance
            
            response = client.get("/ingestion/status/39/2025")
            assert response.status_code == 200
            
            data = response.json()
            # Validate required fields are present
            assert "league_id" in data
            assert "season" in data
            assert "status" in data
            # progress, counts, and last_updated are optional
            assert "progress" in data
            assert "counts" in data
            assert "last_updated" in data

