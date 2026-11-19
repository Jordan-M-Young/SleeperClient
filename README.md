# SleeperClient

A small Python client library for the [Sleeper](https://sleeper.com) fantasy football API.

It wraps Sleeper's public, read only endpoints. The API needs no authentication or API key. Each method returns the a `requests.Response` object, so you'll have to handle status codes and JSON decoding yourself.

## Installation

Requires Python 3.10+.

```bash
pip install sleeperclient
```

## Usage

```python
from sleeperclient import SleeperClient

client = SleeperClient()  # or SleeperClient(timeout=30); the default is 10 seconds

# Look up a user by username (or by user_id)
resp = client.get_user(username="some_username")
user = resp.json()

# List that user's NFL leagues for a season
leagues = client.get_user_leagues(user["user_id"], season="2026").json()

# Get the rosters in the first league
rosters = client.get_league_rosters(leagues[0]["league_id"]).json()
```

## Available methods

| Method | Endpoint |
| --- | --- |
| `get_user(user_id=None, username=None)` | `GET /user/<user_id or username>` |
| `get_user_leagues(user_id, season)` | `GET /user/<user_id>/leagues/nfl/<season>` |
| `get_avatar(avatar_id, thumbnail=False)` | `GET https://sleepercdn.com/avatars[/thumbs]/<avatar_id>` (returns image data) |
| `get_league(league_id)` | `GET /league/<league_id>` |
| `get_league_rosters(league_id)` | `GET /league/<league_id>/rosters` |
| `get_league_users(league_id)` | `GET /league/<league_id>/users` |
| `get_league_matchups(league_id, week)` | `GET /league/<league_id>/matchups/<week>` |
| `get_league_playoff_bracket(league_id, winner=True)` | `GET /league/<league_id>/winners_bracket` or `/losers_bracket` |
| `get_league_transactions(league_id, week)` | `GET /league/<league_id>/transactions/<week>` |
| `get_traded_picks(league_id)` | `GET /league/<league_id>/traded_picks` |
| `get_state(sport)` | `GET /state/<sport>` |
| `get_drafts_for_user(user_id, season, sport="nfl")` | `GET /user/<user_id>/drafts/<sport>/<season>` |
| `get_drafts_for_league(league_id)` | `GET /league/<league_id>/drafts` |

All endpoints except `get_avatar` are relative to `https://api.sleeper.app/v1`. See the [Sleeper API docs](https://docs.sleeper.com/) for the shape of each response.

## Development

You'll need [Poetry](https://python-poetry.org/).

```bash
git clone https://github.com/Jordan-M-Young/SleeperClient.git
cd SleeperClient
poetry install
```

To try the client against the live API:

```bash
poetry run python examples/basic_usage.py <league_id>
```

Lint and format with [Ruff](https://docs.astral.sh/ruff/):

```bash
poetry run ruff check .
poetry run ruff format .
```

## License

Apache 2.0. See [LICENSE](LICENSE).
