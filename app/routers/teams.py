from fastapi import APIRouter, HTTPException

from app.services.livescore import fetch_teams

router = APIRouter(tags=["teams"])


# gets all the african teams (countries)
@router.get("/afcon/teams")
async def get_teams():
    try:
        data = await fetch_teams()
        return {"teams": data["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
