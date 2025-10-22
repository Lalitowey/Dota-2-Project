"""
Integration tests for hero API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
def test_get_hero_constants_success(client: TestClient, mock_opendota_response):
    """Test successful hero constants retrieval."""
    with patch('app.api.v1.endpoints.heroes.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["hero_constants"])
        
        response = client.get("/api/v1/opendota_proxy/constants/heroes")
        
        assert response.status_code == 200
        data = response.json()
        assert "1" in data
        assert data["1"]["localized_name"] == "Anti-Mage"


@pytest.mark.integration
def test_get_hero_constants_caching(client: TestClient, mock_opendota_response):
    """Test that hero constants endpoint uses caching."""
    with patch('app.api.v1.endpoints.heroes.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["hero_constants"])
        
        # First request
        response1 = client.get("/api/v1/opendota_proxy/constants/heroes")
        assert response1.status_code == 200
        
        # Second request - should use cache
        response2 = client.get("/api/v1/opendota_proxy/constants/heroes")
        assert response2.status_code == 200
        
        # Verify API was called only once due to caching
        assert mock_client.get.call_count == 1


@pytest.mark.integration
def test_get_hero_stats_success(client: TestClient):
    """Test successful hero statistics retrieval."""
    with patch('app.api.v1.endpoints.heroes.opendota_client') as mock_client:
        mock_stats = [
            {
                "id": 1,
                "name": "npc_dota_hero_antimage",
                "localized_name": "Anti-Mage",
                "pro_win": 100,
                "pro_pick": 200
            }
        ]
        mock_client.get = AsyncMock(return_value=mock_stats)
        
        response = client.get("/api/v1/opendota_proxy/heroStats")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


@pytest.mark.integration
def test_get_items_constants_success(client: TestClient):
    """Test successful items constants retrieval."""
    with patch('app.api.v1.endpoints.heroes.opendota_client') as mock_client:
        mock_items = {
            "blink": {
                "id": 1,
                "name": "item_blink",
                "cost": 2250
            }
        }
        mock_client.get = AsyncMock(return_value=mock_items)
        
        response = client.get("/api/v1/opendota_proxy/constants/items")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
