from pydantic import BaseModel


class FollowResponse(BaseModel):
    followed: str


class UnfollowResponse(BaseModel):
    unfollowed: str


class MyTeamsResponse(BaseModel):
    team_ids: list[str]
