"""
Integration tests for cache management API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


@pytest.mark.integration
def test_get_cache_stats(client: TestClient):
    """Test cache statistics endpoint."""
    with patch('app.api.v1.endpoints.cache.cache') as mock_cache:
        mock_cache.get_stats.return_value = {
            "total_items": 5,
            "items": {
                "test_key": "2024-01-01T00:00:00"
            }
        }
        
        response = client.get("/api/v1/opendota_proxy/cache/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert "items" in data


@pytest.mark.integration
def test_clear_cache(client: TestClient):
    """Test cache clearing endpoint."""
    with patch('app.api.v1.endpoints.cache.cache') as mock_cache:
        mock_cache.clear.return_value = 10
        
        response = client.delete("/api/v1/opendota_proxy/cache/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Cache cleared successfully"
        assert data["entries_removed"] == 10
        mock_cache.clear.assert_called_once()
