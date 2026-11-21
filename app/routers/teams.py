import logging

import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.team import TeamsResponse
from app.services.livescore import fetch_teams

logger = logging.getLogger(__name__)

router = APIRouter(tags=["teams"])


# gets all the african teams (countries)
@router.get("/afcon/teams", response_model=TeamsResponse)
async def get_teams():
    try:
        data = await fetch_teams()
    except httpx.HTTPError as e:
        # Don't log or return str(e): httpx includes the request URL, which holds the API key and secret.
        status = e.response.status_code if isinstance(e, httpx.HTTPStatusError) else None
        logger.error("LiveScore request failed: %s (status %s)", type(e).__name__, status)
        raise HTTPException(status_code=502, detail="Failed to fetch teams")
    return {"teams": data["data"]}
