"""
Tests for main application endpoints.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_read_root(client: TestClient):
    """Test root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Dota 2 Analytics API"
    assert "version" in data
    assert data["docs"] == "/docs"
    assert data["status"] == "operational"


@pytest.mark.unit
def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.unit
def test_cors_headers(client: TestClient):
    """Test CORS middleware is configured."""
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200


@pytest.mark.unit
def test_docs_accessible(client: TestClient):
    """Test OpenAPI documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.unit
def test_openapi_json(client: TestClient):
    """Test OpenAPI JSON schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Dota 2 Analytics API"
