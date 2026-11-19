"""Quick manual check against the live Sleeper API.

Not part of the published package. Run with:

    poetry run python examples/basic_usage.py <league_id>
"""

import sys

from sleeperclient import SleeperClient


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python examples/basic_usage.py <league_id>")

    client = SleeperClient()
    resp = client.get_league(sys.argv[1])
    print(resp.status_code)
    print(resp.json())


if __name__ == "__main__":
    main()
