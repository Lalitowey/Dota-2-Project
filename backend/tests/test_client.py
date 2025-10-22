"""
Tests for OpenDota HTTP client.
"""
import pytest
from unittest.mock import AsyncMock, patch
import httpx
from app.core.client import OpenDotaClient


@pytest.mark.unit
def test_client_initialization():
    """Test client initializes with correct base URL."""
    client = OpenDotaClient()
    assert client.base_url == "https://api.opendota.com/api"
    assert client.api_key is None  # Default


@pytest.mark.unit
def test_get_headers_without_api_key():
    """Test headers when no API key is set."""
    client = OpenDotaClient()
    headers = client._get_headers()
    assert headers == {}


@pytest.mark.unit
def test_get_headers_with_api_key():
    """Test headers include Authorization when API key is set."""
    with patch('app.core.client.settings') as mock_settings:
        mock_settings.opendota_base_url = "https://api.opendota.com/api"
        mock_settings.opendota_api_key = "test_api_key"
        
        client = OpenDotaClient()
        headers = client._get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_api_key"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_success():
    """Test successful GET request."""
    client = OpenDotaClient()
    
    mock_response = AsyncMock()
    mock_response.json.return_value = {"data": "test_value"}
    mock_response.raise_for_status = AsyncMock()
    
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_async_client.return_value = mock_client_instance
        
        result = await client.get("test/endpoint")
        
        assert result == {"data": "test_value"}
        mock_client_instance.get.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_with_params():
    """Test GET request with query parameters."""
    client = OpenDotaClient()
    
    mock_response = AsyncMock()
    mock_response.json.return_value = {"data": "test_value"}
    mock_response.raise_for_status = AsyncMock()
    
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_async_client.return_value = mock_client_instance
        
        params = {"query": "test"}
        result = await client.get("search", params=params)
        
        assert result == {"data": "test_value"}
        call_args = mock_client_instance.get.call_args
        assert call_args[1]["params"] == params


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_http_error():
    """Test GET request handles HTTP errors."""
    client = OpenDotaClient()
    
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found", request=AsyncMock(), response=AsyncMock(status_code=404)
    )
    
    with patch('httpx.AsyncClient') as mock_async_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_async_client.return_value = mock_client_instance
        
        with pytest.raises(httpx.HTTPStatusError):
            await client.get("nonexistent/endpoint")
