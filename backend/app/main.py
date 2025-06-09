from fastapi import FastAPI, HTTPException, Path
import httpx

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI backend for Dota 2 app"}


@app.get("/api/v1/opendota_proxy/players/{account_id}")
async def get_opendota_player_profile(
        account_id: int = Path(..., title="Account ID", ge=1)
):
    "Proxies request to OpenDota API to get player profile by account ID"
    url = f"https://api.opendota.com/api/players/{account_id}"

    async with httpx.AsyncClient() as client:
        try:
            print(f"Fetching player profile for account ID: {account_id} at URL: {url}") # Debug log
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            player_data = response.json()
            print(f"Successfully fetched player data: {player_data}")
            return player_data
        except httpx.HTTPStatusError as e:
            # if the account ID is not found, OpenDota returns a 404
            print(f"OpenDota API error for account_ID {account_id}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"OpenDota API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            # Handle network-related errors
            print(f"Network error while fetching player profile for account ID {account_id}: {str(e)}") # Debug log
            raise HTTPException(
                status_code=503,
                detail="Network error while fetching player profile"
            )
        except Exception as e:
            # Unexpected errors
            print(f"Unexpected error while fetching player profile for account ID {account_id}: {str(e)}") # Debug log
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )