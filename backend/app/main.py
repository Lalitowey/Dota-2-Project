# backend/app/main.py
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import asyncio

app = FastAPI()

# Simple in-memory cache
class SimpleCache:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry['expires']:
                return entry['data']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl_minutes: int = 60):
        expires = datetime.now() + timedelta(minutes=ttl_minutes)
        self.cache[key] = {
            'data': data,
            'expires': expires
        }
    
    def clear(self):
        self.cache.clear()
    
    def cleanup_expired(self):
        now = datetime.now()
        expired_keys = [key for key, entry in self.cache.items() if now >= entry['expires']]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)

# Global cache instance
cache = SimpleCache()

# Cache configuration for different endpoints
CACHE_CONFIG = {
    'hero_constants': 1440,  # 24 hours
    'player_profile': 30,    # 30 minutes
    'player_winloss': 60,    # 1 hour
    'player_heroes': 120,    # 2 hours
    'player_matches': 10,    # 10 minutes
    'search_results': 5,     # 5 minutes
}

# --- CORS Configuration ---
# List of origins that are allowed to make requests.
# For development, you can allow your Nuxt frontend's origin.
# For production, you'd list your actual frontend domain.
origins = [
    "http://localhost:3000", # Nuxt dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    # allow_origins=["*"], # Allows all origins (use with caution, less secure for production)
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)
# --- End CORS Configuration ---


@app.get("/")
async def read_root():
    return {"Hello": "World from FastAPI backend for Dota 2 Analytics"}

@app.get("/api/v1/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    cache.cleanup_expired()
    return {
        "total_items": len(cache.cache),
        "items": {key: entry['expires'].isoformat() for key, entry in cache.cache.items()}
    }

@app.delete("/api/v1/cache/clear")
async def clear_cache():
    """Clear all cache"""
    cache.clear()
    return {"message": "Cache cleared successfully"}

@app.get("/api/v1/opendota_proxy/players/{account_id}")
async def get_opendota_player_profile(
    account_id: int = Path(..., title="The Account ID of the player to retrieve", ge=1)
):
    cache_key = f"player_profile:{account_id}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"Cache hit for player profile: {account_id}")
        return cached_data
    
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}"
    async with httpx.AsyncClient() as client:
        try:
            print(f"Cache miss - Proxying request to OpenDota for account_id: {account_id} at URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            player_data = response.json()
            
            # Cache the response
            cache.set(cache_key, player_data, CACHE_CONFIG['player_profile'])
            print(f"Successfully fetched and cached data from OpenDota for account_id: {account_id}")
            return player_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error for account_id {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from OpenDota API: {e.response.text}"
            )
        except httpx.RequestError as e:
            print(f"Network error while contacting OpenDota for account_id {account_id}: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Could not connect to OpenDota API: {str(e)}"
            )
        except Exception as e:
            print(f"Unexpected error for account_id {account_id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )

@app.get("/api/v1/opendota_proxy/players/{account_id}/wl") # Route for Win/Loss
async def get_player_wl_from_opendota(
    account_id: int = Path(..., title="The Account ID of the player for WL data", ge=1)
):
    cache_key = f"player_winloss:{account_id}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"Cache hit for player winloss: {account_id}")
        return cached_data
    
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}/wl" # Correct OpenDota URL for WL
    async with httpx.AsyncClient() as client:
        try:
            print(f"Cache miss - Proxying WL request for account_id: {account_id} to URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            wl_data = response.json()
            
            # Cache the response
            cache.set(cache_key, wl_data, CACHE_CONFIG['player_winloss'])
            print(f"Successfully fetched and cached WL data for account_id: {account_id}")
            return wl_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (WL) for account_id {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (WL): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (WL) while contacting OpenDota for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (WL): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (WL) for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (WL): {str(e)}")

@app.get("/api/v1/opendota_proxy/players/{account_id}/totals")
async def get_player_totals(
        account_id: int = Path(..., title="The Account ID of the player for totals data", ge=1)
):
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}/totals"
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying totals request for account_id: {account_id} to URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            totals_data = response.json()
            print(f"Successfully fetched totals data for account_id: {account_id}")
            return totals_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (totals) for account_id {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (totals): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (totals) while contacting OpenDota for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (totals): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (totals) for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (totals): {str(e)}")

@app.get("/api/v1/opendota_proxy/players/{account_id}/heroes")
async def get_player_heroes_from_opendota(
    account_id: int = Path(..., title="The Account ID of the player for heroes data", ge=1)
):
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}/heroes"
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying heroes request for account_id: {account_id} to URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            heroes_data = response.json()
            print(f"Successfully fetched heroes data for account_id: {account_id}")
            return heroes_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (heroes) for account_id {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (heroes): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (heroes) while contacting OpenDota for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (heroes): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (heroes) for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (heroes): {str(e)}")

@app.get("/api/v1/opendota_proxy/constants/heroes")
async def get_opendota_hero_constants():
    cache_key = "hero_constants"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        print("Cache hit for hero constants")
        return cached_data
    
    opendota_api_url = "https://api.opendota.com/api/constants/heroes" # VERIFIED THIS URL IS CORRECT
    async with httpx.AsyncClient() as client:
        try:
            print(f"Cache miss - CONSTANTS PROXY: Proxying request to OpenDota for heroes at URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status() #
            heroes_data = response.json()
            
            # Cache the response
            cache.set(cache_key, heroes_data, CACHE_CONFIG['hero_constants'])
            print("CONSTANTS PROXY: Successfully fetched and cached heroes data from OpenDota")
            return heroes_data
        except httpx.HTTPStatusError as e:
            # This block would have been hit if OpenDota returned 404
            print(f"CONSTANTS PROXY: OpenDota API error for heroes: STATUS={e.response.status_code} - TEXT={e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (constants/heroes): {e.response.text}")
        except httpx.RequestError as e:
            print(f"CONSTANTS PROXY: Network error while contacting OpenDota for heroes: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (constants/heroes): {str(e)}")
        except Exception as e:
            print(f"CONSTANTS PROXY: Unexpected error for heroes: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (constants/heroes): {str(e)}")

@app.get("/api/v1/opendota_proxy/search")
async def get_opendota_players(q: str):
    if not q: # If the query is empty, return an empty list
        return []
    
    cache_key = f"search_results:{q}"
    
    # Try cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"Cache hit for search query: '{q}'")
        return cached_data
    
    opendota_api_url = f"https://api.opendota.com/api/search"
    params = {"q": q} # Use the query parameter to search for players
    async with httpx.AsyncClient() as client:
        try:
            print(f"Cache miss - Proxying SEARCH request for query: '{q}'") # Log the search query
            response = await client.get(opendota_api_url, params=params) # Pass the query as a parameter
            response.raise_for_status()
            search_data = response.json()
            
            # Cache the response
            cache.set(cache_key, search_data, CACHE_CONFIG['search_results'])
            print(f"Successfully fetched and cached search results for query: '{q}'")
            return search_data
        except Exception as e:
            print(f"Error during player search '{q}': {str(e)}")
            return []

@app.get("/api/v1/opendota_proxy/players/{account_id}/matches")
async def get_player_matches(
    account_id: int = Path(..., title="The Account ID of the player for matches data", ge=1),
    limit: int = 20,
    offset: int = 0
):
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}/matches"
    params = {"limit": limit, "offset": offset}
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying matches request for account_id: {account_id} with limit: {limit}, offset: {offset}")
            response = await client.get(opendota_api_url, params=params)
            response.raise_for_status()
            matches_data = response.json()
            print(f"Successfully fetched {len(matches_data)} matches for account_id: {account_id}")
            return matches_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (matches) for account_id {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (matches): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (matches) while contacting OpenDota for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (matches): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (matches) for account_id {account_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (matches): {str(e)}")

@app.get("/api/v1/opendota_proxy/matches/{match_id}")
async def get_match_details(
    match_id: int = Path(..., title="The Match ID to retrieve details for", ge=1)
):
    opendota_api_url = f"https://api.opendota.com/api/matches/{match_id}"
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying match details request for match_id: {match_id}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            match_data = response.json()
            print(f"Successfully fetched match details for match_id: {match_id}")
            return match_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (match details) for match_id {match_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (match details): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (match details) while contacting OpenDota for match_id {match_id}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (match details): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (match details) for match_id {match_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (match details): {str(e)}")

@app.get("/api/v1/opendota_proxy/heroStats")
async def get_hero_stats():
    """Get hero statistics including win rates, pick rates, etc."""
    opendota_api_url = "https://api.opendota.com/api/heroStats"
    async with httpx.AsyncClient() as client:
        try:
            print("Proxying hero stats request")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            hero_stats_data = response.json()
            print(f"Successfully fetched hero stats for {len(hero_stats_data)} heroes")
            return hero_stats_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (hero stats): {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (hero stats): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (hero stats) while contacting OpenDota: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (hero stats): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (hero stats): {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (hero stats): {str(e)}")

@app.get("/api/v1/opendota_proxy/constants/items")
async def get_items_constants():
    """Get item constants for popular items data"""
    opendota_api_url = "https://api.opendota.com/api/constants/items"
    async with httpx.AsyncClient() as client:
        try:
            print("Proxying items constants request")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            items_data = response.json()
            print("Successfully fetched items constants")
            return items_data
        except httpx.HTTPStatusError as e:
            print(f"OpenDota API error (items constants): {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from OpenDota API (items constants): {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error (items constants) while contacting OpenDota: {str(e)}")
            raise HTTPException(status_code=503, detail=f"Could not connect to OpenDota API (items constants): {str(e)}")
        except Exception as e:
            print(f"Unexpected error (items constants): {str(e)}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred (items constants): {str(e)}")
