from pydantic import BaseModel


# One team as returned by LiveScore. Extra fields from LiveScore are dropped.
class Team(BaseModel):
    id: str
    name: str
    country_id: str | None = None
    stadium: str | None = None
    location: str | None = None


class TeamsResponse(BaseModel):
    teams: list[Team]
