"""
In-memory cache implementation with TTL support.
TODO: Replace with Redis or PostgreSQL for production persistence.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SimpleCache:
    """Simple in-memory cache with time-to-live support."""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data if valid, None if expired or not found
        """
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry['expires']:
                logger.debug(f"Cache hit: {key}")
                return entry['data']
            else:
                del self.cache[key]
                logger.debug(f"Cache expired: {key}")
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    def set(self, key: str, data: Any, ttl_minutes: int = 60) -> None:
        """
        Store data in cache with TTL.
        
        Args:
            key: Cache key
            data: Data to cache
            ttl_minutes: Time-to-live in minutes
        """
        expires = datetime.now() + timedelta(minutes=ttl_minutes)
        self.cache[key] = {
            'data': data,
            'expires': expires
        }
        logger.debug(f"Cache set: {key} (TTL: {ttl_minutes}m)")
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"Cache cleared: {count} entries removed")
        return count
    
    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.
        
        Returns:
            Number of expired entries removed
        """
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items() 
            if now >= entry['expires']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cache cleanup: {len(expired_keys)} expired entries removed")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        self.cleanup_expired()
        return {
            "total_items": len(self.cache),
            "items": {
                key: entry['expires'].isoformat() 
                for key, entry in self.cache.items()
            }
        }


# Global cache instance
cache = SimpleCache()
