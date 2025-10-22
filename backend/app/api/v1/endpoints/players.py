"""
Player-related API endpoints.
"""
from fastapi import APIRouter, HTTPException, Path, Query
import httpx
import logging
from typing import Any

from app.config import settings
from app.core import cache, opendota_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/players/{account_id}")
async def get_player_profile(
    account_id: int = Path(..., title="The Account ID of the player", ge=1)
) -> Any:
    """Get player profile data from OpenDota."""
    cache_key = f"player_profile:{account_id}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        data = await opendota_client.get(f"players/{account_id}")
        cache.set(cache_key, data, settings.cache_ttl_player_profile)
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for player {account_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for player {account_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/players/{account_id}/wl")
async def get_player_winloss(
    account_id: int = Path(..., title="The Account ID for win/loss data", ge=1)
) -> Any:
    """Get player win/loss statistics."""
    cache_key = f"player_winloss:{account_id}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        data = await opendota_client.get(f"players/{account_id}/wl")
        cache.set(cache_key, data, settings.cache_ttl_player_winloss)
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for player WL {account_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for player WL {account_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/players/{account_id}/totals")
async def get_player_totals(
    account_id: int = Path(..., title="The Account ID for totals data", ge=1)
) -> Any:
    """Get player performance totals."""
    try:
        data = await opendota_client.get(f"players/{account_id}/totals")
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for player totals {account_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for player totals {account_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/players/{account_id}/heroes")
async def get_player_heroes(
    account_id: int = Path(..., title="The Account ID for heroes data", ge=1)
) -> Any:
    """Get player hero statistics."""
    cache_key = f"player_heroes:{account_id}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        data = await opendota_client.get(f"players/{account_id}/heroes")
        cache.set(cache_key, data, settings.cache_ttl_player_heroes)
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for player heroes {account_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for player heroes {account_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/players/{account_id}/matches")
async def get_player_matches(
    account_id: int = Path(..., title="The Account ID for matches data", ge=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> Any:
    """Get player match history."""
    try:
        data = await opendota_client.get(
            f"players/{account_id}/matches",
            params={"limit": limit, "offset": offset}
        )
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for player matches {account_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for player matches {account_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )


@router.get("/search")
async def search_players(q: str = Query("", min_length=1)) -> Any:
    """Search for players by name."""
    if not q:
        return []
    
    cache_key = f"search_results:{q}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        data = await opendota_client.get("search", params={"q": q})
        cache.set(cache_key, data, settings.cache_ttl_search_results)
        return data
    except Exception as e:
        logger.error(f"Error during player search '{q}': {str(e)}")
        return []
