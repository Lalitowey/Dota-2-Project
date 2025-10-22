"""
Integration tests for player API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
def test_get_player_profile_success(client: TestClient, mock_opendota_response, sample_account_id):
    """Test successful player profile retrieval."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["player"])
        
        response = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["account_id"] == sample_account_id


@pytest.mark.integration
def test_get_player_profile_invalid_id(client: TestClient):
    """Test player profile with invalid account ID."""
    response = client.get("/api/v1/opendota_proxy/players/0")
    assert response.status_code == 422  # Validation error


@pytest.mark.integration
def test_get_player_winloss_success(client: TestClient, mock_opendota_response, sample_account_id):
    """Test successful win/loss statistics retrieval."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["wl"])
        
        response = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}/wl")
        
        assert response.status_code == 200
        data = response.json()
        assert "win" in data
        assert "lose" in data
        assert data["win"] == 100
        assert data["lose"] == 50


@pytest.mark.integration
def test_get_player_totals_success(client: TestClient, sample_account_id):
    """Test successful player totals retrieval."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=[{"field": "kills", "sum": 1000}])
        
        response = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}/totals")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
def test_get_player_heroes_success(client: TestClient, mock_opendota_response, sample_account_id):
    """Test successful player hero statistics retrieval."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["heroes"])
        
        response = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}/heroes")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["hero_id"] == 1


@pytest.mark.integration
def test_get_player_matches_success(client: TestClient, sample_account_id):
    """Test successful player match history retrieval."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=[{"match_id": 123456, "hero_id": 1}])
        
        response = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}/matches")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
def test_get_player_matches_with_params(client: TestClient, sample_account_id):
    """Test player match history with limit and offset parameters."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=[])
        
        response = client.get(
            f"/api/v1/opendota_proxy/players/{sample_account_id}/matches?limit=10&offset=5"
        )
        
        assert response.status_code == 200
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[1]["params"]["limit"] == 10
        assert call_args[1]["params"]["offset"] == 5


@pytest.mark.integration
def test_search_players_success(client: TestClient):
    """Test successful player search."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=[{"account_id": 123, "personaname": "Test"}])
        
        response = client.get("/api/v1/opendota_proxy/search?q=TestPlayer")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.integration
def test_search_players_empty_query(client: TestClient):
    """Test player search with empty query returns empty list."""
    response = client.get("/api/v1/opendota_proxy/search?q=")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
def test_player_endpoint_caching(client: TestClient, mock_opendota_response, sample_account_id):
    """Test that player endpoints use caching."""
    with patch('app.api.v1.endpoints.players.opendota_client') as mock_client:
        mock_client.get = AsyncMock(return_value=mock_opendota_response["player"])
        
        # First request - should call API
        response1 = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}")
        assert response1.status_code == 200
        
        # Second request - should use cache (not call API again)
        response2 = client.get(f"/api/v1/opendota_proxy/players/{sample_account_id}")
        assert response2.status_code == 200
        
        # Verify API was called only once due to caching
        assert mock_client.get.call_count == 1
