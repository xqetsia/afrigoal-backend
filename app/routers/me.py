from fastapi import APIRouter, Depends

from app.db import get_db
from app.models import User, UserTeam
from app.schemas.me import FollowResponse, MyTeamsResponse, UnfollowResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/me", tags=["me"])

# Handlers below are plain `def` because SQLAlchemy calls are blocking.
# FastAPI runs plain `def` handlers in a thread pool so they don't freeze the event loop.


# retrieve the user from the database. if the user does not exist, add them to the database
# check if user already follows this team, if not add it
@router.post("/teams/{team_id}", response_model=FollowResponse)
def follow_team(
    team_id: str,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    db_user = db.query(User).filter(User.id == user["uid"]).first()
    if not db_user:
        db.add(User(id=user["uid"], email=user.get("email")))
        db.commit()

    existing = db.query(UserTeam).filter_by(user_id=user["uid"], team_id=team_id).first()
    if not existing:
        db.add(UserTeam(user_id=user["uid"], team_id=team_id))
        db.commit()

    return {"followed": team_id}


# gets the user and deletes the team from their followed teams
@router.delete("/teams/{team_id}", response_model=UnfollowResponse)
def unfollow_team(
    team_id: str,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    db.query(UserTeam).filter_by(user_id=user["uid"], team_id=team_id).delete()
    db.commit()
    return {"unfollowed": team_id}


# gets all the teams followed by the user
@router.get("/teams", response_model=MyTeamsResponse)
def get_my_teams(
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    follows = db.query(UserTeam).filter_by(user_id=user["uid"]).all()
    return {"team_ids": [f.team_id for f in follows]}
