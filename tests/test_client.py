"""Offline unit tests. ``requests.get`` is replaced by the ``fake_get`` fixture."""

import pytest

from sleeperclient import SleeperClient, __version__

BASE = "https://api.sleeper.app/v1"


def test_client():
    client = SleeperClient()
    assert client.timeout == 10
    assert client.base_url == BASE
    assert isinstance(client, SleeperClient)


def test_custom_timeout():
    assert SleeperClient(timeout=30).timeout == 30


def test_headers_identify_the_library(client):
    assert client.headers["User-Agent"] == f"sleeperclient/{__version__}"
    assert client.headers["Accept"] == "application/json"


@pytest.mark.parametrize(
    ("method", "kwargs", "expected_url"),
    [
        ("get_user", {"user_id": "123"}, f"{BASE}/user/123"),
        ("get_user", {"username": "alice"}, f"{BASE}/user/alice"),
        (
            "get_user_leagues",
            {"user_id": "123", "season": "2026"},
            f"{BASE}/user/123/leagues/nfl/2026",
        ),
        ("get_avatar", {"avatar_id": "abc"}, "https://sleepercdn.com/avatars/abc"),
        (
            "get_avatar",
            {"avatar_id": "abc", "thumbnail": True},
            "https://sleepercdn.com/avatars/thumbs/abc",
        ),
        ("get_league", {"league_id": "L1"}, f"{BASE}/league/L1"),
        ("get_league_rosters", {"league_id": "L1"}, f"{BASE}/league/L1/rosters"),
        ("get_league_users", {"league_id": "L1"}, f"{BASE}/league/L1/users"),
        (
            "get_league_matchups",
            {"league_id": "L1", "week": "3"},
            f"{BASE}/league/L1/matchups/3",
        ),
        (
            "get_league_playoff_bracket",
            {"league_id": "L1"},
            f"{BASE}/league/L1/winners_bracket",
        ),
        (
            "get_league_playoff_bracket",
            {"league_id": "L1", "winner": False},
            f"{BASE}/league/L1/losers_bracket",
        ),
        (
            "get_league_transactions",
            {"league_id": "L1", "week": "3"},
            f"{BASE}/league/L1/transactions/3",
        ),
        ("get_traded_picks", {"league_id": "L1"}, f"{BASE}/league/L1/traded_picks"),
        ("get_state", {"sport": "nfl"}, f"{BASE}/state/nfl"),
        (
            "get_drafts_for_user",
            {"user_id": "123", "season": "2026"},
            f"{BASE}/user/123/drafts/nfl/2026",
        ),
        (
            "get_drafts_for_user",
            {"user_id": "123", "season": "2026", "sport": "nba"},
            f"{BASE}/user/123/drafts/nba/2026",
        ),
        ("get_drafts_for_league", {"league_id": "L1"}, f"{BASE}/league/L1/drafts"),
    ],
)
def test_method_requests_expected_url(client, fake_get, method, kwargs, expected_url):
    result = getattr(client, method)(**kwargs)

    assert result == "fake-response"
    assert len(fake_get.calls) == 1
    assert fake_get.last["url"] == expected_url
    assert fake_get.last["headers"] == client.headers
    assert fake_get.last["timeout"] == client.timeout


def test_custom_timeout_is_sent_with_requests(fake_get):
    SleeperClient(timeout=2.5).get_state("nfl")
    assert fake_get.last["timeout"] == 2.5


def test_get_user_prefers_user_id_over_username(client, fake_get):
    client.get_user(user_id="123", username="alice")
    assert fake_get.last["url"] == f"{BASE}/user/123"


def test_get_user_requires_an_identifier(client, fake_get):
    with pytest.raises(ValueError):
        client.get_user()
    assert fake_get.calls == []


@pytest.mark.parametrize(
    ("kwargs", "expected_params"),
    [
        ({}, {"active": "true"}),
        ({"active": False}, {}),
        ({"position": "QB"}, {"position": "QB", "active": "true"}),
        ({"position": "QB", "active": False}, {"position": "QB"}),
    ],
)
def test_get_all_players_params(client, fake_get, kwargs, expected_params):
    client.get_all_players(**kwargs)

    assert fake_get.last["url"] == f"{BASE}/players/nfl"
    assert fake_get.last["params"] == expected_params
    assert fake_get.last["timeout"] == client.timeout
