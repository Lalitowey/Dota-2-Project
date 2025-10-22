"""
Cache management API endpoints.
"""
from fastapi import APIRouter
from typing import Any

from app.core import cache

router = APIRouter()


@router.get("/cache/stats")
async def get_cache_stats() -> Any:
    """Get cache statistics and expiration times."""
    return cache.get_stats()


@router.delete("/cache/clear")
async def clear_cache() -> dict:
    """Clear all cached entries."""
    count = cache.clear()
    return {
        "message": "Cache cleared successfully",
        "entries_removed": count
    }
