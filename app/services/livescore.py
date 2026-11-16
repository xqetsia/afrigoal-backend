import httpx
from app.config import LIVESCORE_API_KEY, LIVESCORE_API_SECRET


BASE_URL = "https://livescore-api.com/api-client"

async def fetch_teams():
    url = f"{BASE_URL}/competitions/participants.json"
    params = {
        "key": LIVESCORE_API_KEY,
        "secret": LIVESCORE_API_SECRET,
        "competition_id": 227,
        "season": 2025
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
