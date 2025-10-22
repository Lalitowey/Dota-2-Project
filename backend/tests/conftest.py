"""
Pytest configuration and shared fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from typing import AsyncGenerator, Generator

from app.main_new import app
from app.config import Settings


@pytest.fixture
def test_settings() -> Settings:
    """Provide test-specific settings."""
    return Settings(
        app_name="Dota 2 Analytics API Test",
        debug=True,
        database_url="postgresql://dota_user:dota_password@localhost:5432/dota_db_test",
        opendota_base_url="https://api.opendota.com/api",
        cors_origins=["http://localhost:3000"],
        log_level="DEBUG"
    )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a synchronous test client for FastAPI."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an asynchronous test client for FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_opendota_response():
    """Provide mock OpenDota API responses."""
    return {
        "player": {
            "account_id": 123456789,
            "profile": {
                "personaname": "TestPlayer",
                "avatar": "https://example.com/avatar.jpg",
                "profileurl": "https://example.com/profile"
            }
        },
        "wl": {
            "win": 100,
            "lose": 50
        },
        "heroes": [
            {
                "hero_id": 1,
                "games": 50,
                "win": 30
            }
        ],
        "hero_constants": {
            "1": {
                "id": 1,
                "name": "npc_dota_hero_antimage",
                "localized_name": "Anti-Mage"
            }
        }
    }


@pytest.fixture
def sample_account_id() -> int:
    """Provide a sample account ID for testing."""
    return 123456789
