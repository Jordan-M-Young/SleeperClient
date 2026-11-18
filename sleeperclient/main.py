import requests


class SleeperClient():
    """Client for the public Sleeper fantasy football API (v1).

    Wraps the read-only Sleeper endpoints. Each method sends a GET request and
    returns the raw ``requests.Response``, so callers handle status codes and
    JSON decoding themselves.

    Attributes:
        base_url: Root URL of the Sleeper API.
        headers: HTTP headers sent with every request.
    """

    def __init__(self):
        """Set up the client with the API base URL and default request headers."""
        self.base_url = "https://api.sleeper.app/v1"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }

    def get_user(self, user_id: str = None, username: str = None) -> requests.Response:
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
        endpoint = "user/"
        if not username and not user_id:
            raise ValueError("Either 'username' or 'user_id' must be provided.")

        if user_id:
            url = "/".join([self.base_url,endpoint,user_id])
        else:
            url = "/".join([self.base_url,endpoint,username])

        
        return requests.get(url=url,headers=self.headers)
    
    def get_user_leagues(self, user_id: str, season: str) -> requests.Response:
        """Fetch all NFL leagues a user belongs to in a given season.

        Args:
            user_id: The user's numeric Sleeper ID, as a string.
            season: The season year, e.g. ``"2026"``.

        Returns:
            The response from ``GET /user/<user_id>/leagues/nfl/<season>``.
        """
        url = f"{self.base_url}/user/{user_id}/leagues/nfl/{season}"
        return requests.get(url=url,headers=self.headers)


    def get_league(self, league_id: str) -> requests.Response:
        """Fetch details for a single league.

        Args:
            league_id: The league's numeric Sleeper ID, as a string.

        Returns:
            The response from ``GET /league/<league_id>``.
        """
        url = f"{self.base_url}/league/{league_id}"
        return requests.get(url=url,headers=self.headers)


    def get_avatar(self, avatar_id: str, thumbnail=False):
        if thumbnail:
            url = f"https://sleepercdn.com/avatars/thumbs/{avatar_id}"
        else:
            url = f"https://sleepercdn.com/avatars/{avatar_id}"


        return requests.get(url=url,headers=self.headers)
    

    def get_league_rosters(self, league_id: str) -> requests.Response:
        url = f"{self.base_url}/league/{league_id}/rosters"
        return requests.get(url=url,headers=self.headers)
    
    def get_league_users(self, league_id: str) -> requests.Response:
        url = f"{self.base_url}/league/{league_id}/users"
        return requests.get(url=url,headers=self.headers)
    
    def get_league_matchups(self, league_id: str, week: str) -> requests.Response:
        url = f"{self.base_url}/league/{league_id}/matchups/{week}"
        return requests.get(url=url,headers=self.headers)


def main():
    ID = ""
    LEAGUE_ID = ""
    client = SleeperClient()


    # print("USER TEST")
    # resp = client.get_user(user_id=ID)
    # print(resp.status_code)
    # print(resp.json())


    # print("USER LEAGUES TEST")
    # resp = client.get_user_leagues(ID, season="2026")
    # print(resp.status_code)
    # print(resp.json())


    resp = client.get_league(LEAGUE_ID)
    print(resp.status_code)
    print(resp.json())



if __name__ == "__main__":
    main()


        
