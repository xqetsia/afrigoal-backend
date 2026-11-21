import httpx

from app.routers import teams

FAKE_TEAMS = [
    {"id": "1435", "name": "Morocco", "country_id": "118", "stadium": "Stade Mohamed V", "location": "Rabat"},
]


def test_get_teams_returns_teams(client, monkeypatch):
    async def fake_fetch_teams():
        return {"success": True, "data": FAKE_TEAMS}

    # Patch the name the router uses, not app.services.livescore.fetch_teams.
    monkeypatch.setattr(teams, "fetch_teams", fake_fetch_teams)

    response = client.get("/afcon/teams")

    assert response.status_code == 200
    assert response.json() == {"teams": FAKE_TEAMS}


def test_get_teams_drops_unknown_fields(client, monkeypatch):
    async def fake_fetch_teams():
        return {"data": [{**FAKE_TEAMS[0], "internal_field": "x"}]}

    monkeypatch.setattr(teams, "fetch_teams", fake_fetch_teams)

    team = client.get("/afcon/teams").json()["teams"][0]

    assert "internal_field" not in team


def test_get_teams_upstream_error_does_not_leak_secrets(client, monkeypatch):
    async def failing_fetch_teams():
        request = httpx.Request("GET", "https://livescore.example/api?key=SECRET_KEY&secret=SECRET")
        raise httpx.HTTPStatusError("401", request=request, response=httpx.Response(401, request=request))

    monkeypatch.setattr(teams, "fetch_teams", failing_fetch_teams)

    response = client.get("/afcon/teams")

    assert response.status_code == 502
    assert "SECRET" not in response.text
