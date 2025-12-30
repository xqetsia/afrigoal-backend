from fastapi import FastAPI, HTTPException, Depends
from services.livescore import fetch_teams
from services.auth import get_current_user
from services.db import SessionLocal, User, UserTeam

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/afcon/teams")
async def get_teams():
    try:
        data = await fetch_teams()
        return {"teams": data["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/me/teams/{team_id}")
async def follow_team(
        team_id: str,
        user: dict = Depends(get_current_user),
        db = Depends(get_db),
):
    # get the user. if the user does not exist, add them to the database
    db_user = db.query(User).filter(User.id == user["uid"]).first()
    if not db_user:
        db.add(User(id=user["uid"], email=user.get("email")))
        db.commit()

    # check if user already follows this team, if not add it
    existing = db.query(UserTeam).filter_by(user_id=user["uid"], team_id=team_id).first()
    if not existing:
        db.add(UserTeam(user_id=user["uid"], team_id=team_id))
        db.commit()

    return {"followed": team_id}

@app.post("/me/teams")
async def get_my_teams(
        user: dict = Depends(get_current_user),
        db = Depends(get_db)
):
    follows = db.query(UserTeam).filter_by(user_id=user["uid"]).all()
    return {"team_ids": [f.teams_id for f in follows]}

