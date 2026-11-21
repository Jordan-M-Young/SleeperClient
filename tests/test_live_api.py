"""Integration tests against the real Sleeper API.

These need network access and the ``ID`` and ``LEAGUE_ID`` values in ``.env``;
a test skips itself if a value it needs is missing. Skip them all with:

    poetry run pytest -m "not integration"
"""

import pytest

pytestmark = pytest.mark.integration


def test_get_state(client):
    resp = client.get_state("nfl")
    assert resp.status_code == 200
    assert "season" in resp.json()


def test_get_user(client, user_id):
    resp = client.get_user(user_id=user_id)
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user_id


def test_get_user_leagues(client, user_id):
    season = client.get_state("nfl").json()["season"]
    resp = client.get_user_leagues(user_id, season=season)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_league(client, league_id):
    resp = client.get_league(league_id)
    assert resp.status_code == 200
    assert resp.json()["league_id"] == league_id


@pytest.mark.parametrize(
    "method",
    [
        "get_league_rosters",
        "get_league_users",
        "get_traded_picks",
        "get_drafts_for_league",
    ],
)
def test_league_list_endpoints(client, league_id, method):
    resp = getattr(client, method)(league_id)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_league_matchups(client, league_id):
    resp = client.get_league_matchups(league_id, week="1")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.parametrize("action_type", ["add", "drop"])
def test_get_trending_players_limit(client, action_type):
    resp = client.get_trending_players(action_type, limit=3)
    assert resp.status_code == 200
    players = resp.json()
    assert len(players) == 3
    assert {"player_id", "count"} <= players[0].keys()


def test_get_trending_players_lookback_hours(client):
    last_hour = client.get_trending_players("add", hours=1, limit=1).json()
    last_week = client.get_trending_players("add", hours=168, limit=1).json()
    assert last_week[0]["count"] > last_hour[0]["count"]
