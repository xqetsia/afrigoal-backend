from app.main import app
from app.models import User, UserTeam
from app.services.auth import get_current_user

from tests.conftest import TEST_USER


def test_my_teams_starts_empty(auth_client):
    response = auth_client.get("/me/teams")

    assert response.status_code == 200
    assert response.json() == {"team_ids": []}


def test_follow_team_creates_user_and_follow(auth_client, db):
    response = auth_client.post("/me/teams/1435")

    assert response.status_code == 200
    assert response.json() == {"followed": "1435"}
    assert db.get(User, TEST_USER["uid"]).email == TEST_USER["email"]
    assert auth_client.get("/me/teams").json() == {"team_ids": ["1435"]}


def test_follow_same_team_twice_is_idempotent(auth_client, db):
    auth_client.post("/me/teams/1435")
    auth_client.post("/me/teams/1435")

    assert db.query(UserTeam).count() == 1


def test_unfollow_team(auth_client):
    auth_client.post("/me/teams/1435")
    auth_client.post("/me/teams/1530")

    response = auth_client.delete("/me/teams/1435")

    assert response.status_code == 200
    assert response.json() == {"unfollowed": "1435"}
    assert auth_client.get("/me/teams").json() == {"team_ids": ["1530"]}


def test_users_only_see_their_own_teams(auth_client):
    auth_client.post("/me/teams/1435")

    app.dependency_overrides[get_current_user] = lambda: {"uid": "other-user"}

    assert auth_client.get("/me/teams").json() == {"team_ids": []}


def test_missing_token_is_401(client):
    assert client.get("/me/teams").status_code == 401


def test_malformed_token_is_401(client):
    response = client.get("/me/teams", headers={"Authorization": "Token abc"})

    assert response.status_code == 401
