"""
Match-related API endpoints.
"""
from fastapi import APIRouter, HTTPException, Path
import httpx
import logging
from typing import Any

from app.core import opendota_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/matches/{match_id}")
async def get_match_details(
    match_id: int = Path(..., title="The Match ID to retrieve", ge=1)
) -> Any:
    """Get detailed match information."""
    try:
        data = await opendota_client.get(f"matches/{match_id}")
        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenDota API error for match {match_id}: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from OpenDota API: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error for match {match_id}: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to OpenDota API: {str(e)}"
        )
