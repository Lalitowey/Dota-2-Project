"""
HTTP client for OpenDota API interactions.
"""
import httpx
from typing import Any, Dict, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class OpenDotaClient:
    """Client for making requests to the OpenDota API."""
    
    def __init__(self):
        self.base_url = settings.opendota_base_url
        self.api_key = settings.opendota_api_key
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests including optional API key."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make a GET request to OpenDota API.
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPStatusError: If API returns error status
            httpx.RequestError: If network error occurs
        """
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            logger.info(f"OpenDota API request: {endpoint}")
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"OpenDota API response received: {endpoint}")
            return data


# Global client instance
opendota_client = OpenDotaClient()
