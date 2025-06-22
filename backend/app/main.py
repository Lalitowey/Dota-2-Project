# backend/app/main.py
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
import httpx

app = FastAPI()

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

@app.get("/api/v1/opendota_proxy/players/{account_id}")
async def get_opendota_player_profile(
    account_id: int = Path(..., title="The Account ID of the player to retrieve", ge=1)
):
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}"
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying request to OpenDota for account_id: {account_id} at URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            player_data = response.json()
            print(f"Successfully fetched data from OpenDota for account_id: {account_id}")
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
    opendota_api_url = f"https://api.opendota.com/api/players/{account_id}/wl" # Correct OpenDota URL for WL
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying WL request for account_id: {account_id} to URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status()
            wl_data = response.json()
            print(f"Successfully fetched WL data for account_id: {account_id}")
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
async def get_opendota_hero_constants(): # Using a clear, unique function name
    opendota_api_url = "https://api.opendota.com/api/constants/heroes" # VERIFIED THIS URL IS CORRECT
    async with httpx.AsyncClient() as client:
        try:
            print(f"CONSTANTS PROXY: Proxying request to OpenDota for heroes at URL: {opendota_api_url}")
            response = await client.get(opendota_api_url)
            response.raise_for_status() # This will raise an error if OpenDota returns 4xx/5xx
            heroes_data = response.json()
            print("CONSTANTS PROXY: Successfully fetched heroes data from OpenDota")
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