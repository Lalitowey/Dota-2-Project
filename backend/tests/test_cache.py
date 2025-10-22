"""
Tests for cache implementation.
"""
import pytest
from datetime import datetime, timedelta
from app.core.cache import SimpleCache


@pytest.fixture
def cache():
    """Provide a fresh cache instance for each test."""
    return SimpleCache()


@pytest.mark.unit
def test_cache_set_and_get(cache: SimpleCache):
    """Test basic cache set and get operations."""
    cache.set("test_key", {"data": "test_value"}, ttl_minutes=10)
    result = cache.get("test_key")
    assert result == {"data": "test_value"}


@pytest.mark.unit
def test_cache_miss(cache: SimpleCache):
    """Test cache returns None for missing keys."""
    result = cache.get("nonexistent_key")
    assert result is None


@pytest.mark.unit
def test_cache_expiration(cache: SimpleCache):
    """Test cache entries expire after TTL."""
    # Set with negative TTL to immediately expire
    cache.cache["test_key"] = {
        'data': "test_value",
        'expires': datetime.now() - timedelta(minutes=1)
    }
    result = cache.get("test_key")
    assert result is None
    assert "test_key" not in cache.cache


@pytest.mark.unit
def test_cache_clear(cache: SimpleCache):
    """Test clearing all cache entries."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    count = cache.clear()
    assert count == 3
    assert len(cache.cache) == 0


@pytest.mark.unit
def test_cache_cleanup_expired(cache: SimpleCache):
    """Test cleanup removes only expired entries."""
    # Set one valid entry
    cache.set("valid_key", "valid_value", ttl_minutes=10)
    
    # Set one expired entry
    cache.cache["expired_key"] = {
        'data': "expired_value",
        'expires': datetime.now() - timedelta(minutes=1)
    }
    
    count = cache.cleanup_expired()
    assert count == 1
    assert cache.get("valid_key") == "valid_value"
    assert "expired_key" not in cache.cache


@pytest.mark.unit
def test_cache_stats(cache: SimpleCache):
    """Test cache statistics retrieval."""
    cache.set("key1", "value1", ttl_minutes=10)
    cache.set("key2", "value2", ttl_minutes=20)
    
    stats = cache.get_stats()
    assert stats["total_items"] == 2
    assert "key1" in stats["items"]
    assert "key2" in stats["items"]


@pytest.mark.unit
def test_cache_overwrite(cache: SimpleCache):
    """Test overwriting existing cache entries."""
    cache.set("test_key", "old_value", ttl_minutes=10)
    cache.set("test_key", "new_value", ttl_minutes=10)
    
    result = cache.get("test_key")
    assert result == "new_value"


@pytest.mark.unit
def test_cache_different_ttls(cache: SimpleCache):
    """Test cache entries with different TTLs."""
    cache.set("short_ttl", "value1", ttl_minutes=1)
    cache.set("long_ttl", "value2", ttl_minutes=100)
    
    # Both should be accessible immediately
    assert cache.get("short_ttl") == "value1"
    assert cache.get("long_ttl") == "value2"
