"""
Hero-related API endpoints.
"""
from fastapi import APIRouter, HTTPException, Path
import httpx
import logging
from typing import Any

from app.config import settings
from app.core import cache, opendota_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/constants/heroes")
async def get_hero_constants() -> Any:
    """Get hero constants and metadata."""
    cache_key = "hero_constants"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        data = await opendota_client.get("constants/heroes")
        cache.set(cache_key, data, settings.cache_ttl_hero_constants)
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for hero constants: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for hero constants: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/heroStats")
async def get_hero_stats() -> Any:
    """Get hero statistics including win rates and pick rates."""
    try:
        data = await opendota_client.get("heroStats")
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for hero stats: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for hero stats: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/constants/items")
async def get_items_constants() -> Any:
    """Get item constants for popular items data."""
    try:
        data = await opendota_client.get("constants/items")
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for items constants: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for items constants: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )
