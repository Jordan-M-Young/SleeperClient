import requests


class SleeperClient():
    def __init__(self):
        self.base_url = "https://api.sleeper.app/v1"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }

    def get_user(self, user_id: str = None, username: str = None) -> requests.Response:
        endpoint = "user/"
        if not username and not user_id:
            raise ValueError("Either 'username' or 'user_id' must be provided.")

        if user_id:
            url = "/".join([self.base_url,endpoint,user_id])
        else:
            url = "/".join([self.base_url,endpoint,username])

        
        return requests.get(url=url,headers=self.headers)
    
    def get_user_leagues(self, user_id: str, season: str) -> requests.Response:
        url = f"{self.base_url}/user/{user_id}/leagues/nfl/{season}"
        return requests.get(url=url,headers=self.headers)


    def get_league(self, league_id: str) -> requests.Response:
        url = f"{self.base_url}/league/{league_id}"
        return requests.get(url=url,headers=self.headers)



def main():
    ID = ""
    client = SleeperClient()

    resp = client.get_user(user_id=ID)

    print("USER TEST")
    print(resp.status_code)
    print(resp.json())


    print("USER LEAGUES TEST")
    resp = client.get_user_leagues(ID, season="2026")
    print(resp.status_code)
    print(resp.json())






if __name__ == "__main__":
    main()


        
