"""
Tests for configuration management.
"""
import pytest
from app.config import Settings


@pytest.mark.unit
def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    assert settings.app_name == "Dota 2 Analytics API"
    assert settings.app_version == "1.0.0"
    assert settings.debug is False
    assert settings.opendota_base_url == "https://api.opendota.com/api"
    assert settings.cors_origins == ["http://localhost:3000"]
    assert settings.log_level == "INFO"


@pytest.mark.unit
def test_settings_override():
    """Test settings can be overridden."""
    settings = Settings(
        app_name="Custom App",
        debug=True,
        log_level="DEBUG"
    )
    assert settings.app_name == "Custom App"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"


@pytest.mark.unit
def test_cache_ttl_settings():
    """Test cache TTL configuration values."""
    settings = Settings()
    assert settings.cache_ttl_hero_constants == 1440  # 24 hours
    assert settings.cache_ttl_player_profile == 30
    assert settings.cache_ttl_player_winloss == 60
    assert settings.cache_ttl_player_heroes == 120
    assert settings.cache_ttl_player_matches == 10
    assert settings.cache_ttl_search_results == 5


@pytest.mark.unit
def test_optional_settings():
    """Test optional settings default to None."""
    settings = Settings()
    assert settings.opendota_api_key is None
    assert settings.github_token is None


@pytest.mark.unit
def test_database_url_default():
    """Test database URL has correct default."""
    settings = Settings()
    assert "postgresql://" in settings.database_url
    assert "dota_db" in settings.database_url
