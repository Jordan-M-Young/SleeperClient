from pathlib import Path

import pytest
from dotenv import dotenv_values

from sleeperclient import SleeperClient

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
config = dotenv_values(ENV_PATH)


class FakeGet:
    """Stands in for ``requests.get`` and records each call instead of sending it."""

    def __init__(self):
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return "fake-response"

    @property
    def last(self):
        return self.calls[-1]


@pytest.fixture
def client():
    return SleeperClient()


@pytest.fixture
def fake_get(monkeypatch):
    fake = FakeGet()
    monkeypatch.setattr("sleeperclient.main.requests.get", fake)
    return fake


@pytest.fixture
def user_id():
    value = config.get("ID")
    if not value:
        pytest.skip("ID is not set in .env")
    return value


@pytest.fixture
def league_id():
    value = config.get("LEAGUE_ID")
    if not value:
        pytest.skip("LEAGUE_ID is not set in .env")
    return value
