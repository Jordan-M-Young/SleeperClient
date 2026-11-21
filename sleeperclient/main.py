from importlib.metadata import PackageNotFoundError, version

import requests

try:
    __version__ = version("sleeperclient")
except PackageNotFoundError:
    __version__ = "0.0.0"


class SleeperClient:
    """Client for the public Sleeper fantasy football API (v1).

    Wraps the read-only Sleeper endpoints. Each method sends a GET request and
    returns the raw ``requests.Response``, so callers handle status codes and
    JSON decoding themselves.

    Attributes:
        base_url: Root URL of the Sleeper API.
        headers: HTTP headers sent with every request.
        timeout: Seconds to wait for the server before giving up on a request.
    """

    def __init__(self, timeout: float = 10):
        """Set up the client with the API base URL and default request headers.

        Args:
            timeout: Seconds to wait for the server before a request raises
                ``requests.Timeout``. Defaults to 10.
        """
        self.base_url = "https://api.sleeper.app/v1"

        self.headers = {
            "User-Agent": f"sleeperclient/{__version__}",
            "Accept": "application/json",
        }

        self.timeout = timeout

    def get_user(
        self, user_id: str | None = None, username: str | None = None
    ) -> requests.Response:
        """Fetch a Sleeper user by user ID or username.

        If both are given, ``user_id`` is used.

        Args:
            user_id: The user's numeric Sleeper ID, as a string.
            username: The user's Sleeper username.

        Returns:
            The response from ``GET /user/<user_id or username>``.

        Raises:
            ValueError: If neither ``user_id`` nor ``username`` is provided.
        """
        endpoint = "user"
        if not username and not user_id:
            raise ValueError("Either 'username' or 'user_id' must be provided.")

        if user_id:
            url = f"{self.base_url}/{endpoint}/{user_id}"
        else:
            url = f"{self.base_url}/{endpoint}/{username}"

        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_user_leagues(self, user_id: str, season: str) -> requests.Response:
        """Fetch all NFL leagues a user belongs to in a given season.

        Args:
            user_id: The user's numeric Sleeper ID, as a string.
            season: The season year, e.g. ``"2026"``.

        Returns:
            The response from ``GET /user/<user_id>/leagues/nfl/<season>``.
        """
        url = f"{self.base_url}/user/{user_id}/leagues/nfl/{season}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_avatar(self, avatar_id: str, thumbnail=False):
        """Fetch a user or league avatar image from the Sleeper CDN.

        Args:
            avatar_id: The avatar ID, as found on a user or league object.
            thumbnail: If True, fetch the small thumbnail instead of the
                full-size image.

        Returns:
            The response from ``GET https://sleepercdn.com/avatars/<avatar_id>``
            (or ``/avatars/thumbs/<avatar_id>``). The body is image data, not JSON.
        """
        if thumbnail:
            url = f"https://sleepercdn.com/avatars/thumbs/{avatar_id}"
        else:
            url = f"https://sleepercdn.com/avatars/{avatar_id}"

        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league(self, league_id: str) -> requests.Response:
        """Fetch details for a single league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>``.
        """
        url = f"{self.base_url}/league/{league_id}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league_rosters(self, league_id: str) -> requests.Response:
        """Fetch all rosters in a league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>/rosters``.
        """
        url = f"{self.base_url}/league/{league_id}/rosters"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league_users(self, league_id: str) -> requests.Response:
        """Fetch all users in a league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>/users``.
        """
        url = f"{self.base_url}/league/{league_id}/users"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league_matchups(self, league_id: str, week: str) -> requests.Response:
        """Fetch all matchups in a league for a given week.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.
            week: The week number, e.g. ``"1"``.

        Returns:
            The response from ``GET /league/<league_id>/matchups/<week>``.
        """
        url = f"{self.base_url}/league/{league_id}/matchups/{week}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league_playoff_bracket(
        self, league_id: str, winner=True
    ) -> requests.Response:
        """Fetch a league's winners or losers playoff bracket.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.
            winner: If True, fetch the winners bracket; if False, the losers
                bracket.

        Returns:
            The response from ``GET /league/<league_id>/winners_bracket``
            (or ``/losers_bracket``).
        """
        if winner:
            url = f"{self.base_url}/league/{league_id}/winners_bracket"
        else:
            url = f"{self.base_url}/league/{league_id}/losers_bracket"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_league_transactions(self, league_id: str, week: str) -> requests.Response:
        """Fetch all transactions in a league for a given week.

        Transactions include trades, waiver claims and free agent moves.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.
            week: The week number, e.g. ``"1"``.

        Returns:
            The response from ``GET /league/<league_id>/transactions/<week>``.
        """
        url = f"{self.base_url}/league/{league_id}/transactions/{week}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_traded_picks(self, league_id: str) -> requests.Response:
        """Fetch all draft picks that have been traded in a league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>/traded_picks``.
        """
        url = f"{self.base_url}/league/{league_id}/traded_picks"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_state(self, sport: str) -> requests.Response:
        """Fetch the current state of a sport, such as the current week and season.

        Args:
            sport: The sport to query, e.g. ``"nfl"``.

        Returns:
            The response from ``GET /state/<sport>``.
        """
        url = f"{self.base_url}/state/{sport}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_drafts_for_user(
        self, user_id: str, season: str, sport: str = "nfl"
    ) -> requests.Response:
        """Fetch all drafts a user took part in for a given sport and season.

        Args:
            user_id: The user's numeric Sleeper ID, as a string.
            season: The season year, e.g. ``"2026"``.
            sport: The sport to query. Defaults to ``"nfl"``.

        Returns:
            The response from ``GET /user/<user_id>/drafts/<sport>/<season>``.
        """
        url = f"{self.base_url}/user/{user_id}/drafts/{sport}/{season}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_drafts_for_league(self, league_id: str) -> requests.Response:
        """Fetch all drafts for a league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>/drafts``.
        """
        url = f"{self.base_url}/league/{league_id}/drafts"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_specific_draft(self, draft_id: str) -> requests.Response:
        """Fetch details for a single draft.

        Args:
            draft_id: The draft's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /draft/<draft_id>``.
        """
        url = f"{self.base_url}/draft/{draft_id}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_draft_picks(self, draft_id: str) -> requests.Response:
        """Fetch every pick made in a draft.

        Args:
            draft_id: The draft's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /draft/<draft_id>/picks``.
        """
        url = f"{self.base_url}/draft/{draft_id}/picks"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_draft_traded_picks(self, draft_id: str) -> requests.Response:
        """Fetch the picks that were traded before or during a draft.

        Args:
            draft_id: The draft's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /draft/<draft_id>/traded_picks``.
        """
        url = f"{self.base_url}/draft/{draft_id}/traded_picks"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_all_players(
        self, position: str | None = None, active: bool = True
    ) -> requests.Response:
        """Fetch NFL players, optionally filtered by position and active status.

        The unfiltered response is large (about 15 MB), so Sleeper asks that you
        call this endpoint at most once a day and cache the result.

        Args:
            position: Only return players at this position, e.g. ``"QB"``.
                If None, players at every position are returned.
            active: If True, only return active players.

        Returns:
            The response from ``GET /players/nfl``, with ``position`` and
            ``active`` sent as query parameters.
        """
        url = f"{self.base_url}/players/nfl"

        params = {}
        if position:
            params["position"] = position
        if active:
            params["active"] = "true"

        return requests.get(
            url=url, params=params, headers=self.headers, timeout=self.timeout
        )

    def get_trending_players(
        self, action_type: str, hours: int | None = None, limit: int | None = None
    ) -> requests.Response:
        """Fetch the NFL players most added or dropped across Sleeper leagues.

        Args:
            action_type: ``"add"`` for the most-added players, or ``"drop"``
                for the most-dropped.
            hours: How many hours back to count adds or drops. If None, Sleeper
                uses its default of 24.
            limit: The maximum number of players to return. If None, Sleeper
                uses its default of 25.

        Returns:
            The response from ``GET /players/nfl/trending/<action_type>``, with
            ``hours`` sent as ``lookback_hours`` and ``limit`` as ``limit``.
            The body is a list of ``{"player_id": ..., "count": ...}`` objects,
            sorted by count.
        """
        url = f"{self.base_url}/players/nfl/trending/{action_type}"

        params = {}
        if hours is not None:
            params["lookback_hours"] = hours
        if limit is not None:
            params["limit"] = limit
        return requests.get(
            url=url, params=params, headers=self.headers, timeout=self.timeout
        )
