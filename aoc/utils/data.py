import requests
from errors import InvalidConfiguration

from . import config


def download_input(year: int, day: int):
    """
    Downloads the given puzzle. It will raise an exception if the
    session_cookie is not found, or if there is any error downloading the data.
    """
    session_cookie = config.get("SESSION_COOKIE")

    if session_cookie is None:
        raise InvalidConfiguration("SESSION_COOKIE not found")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    requests.get(url, cookies={"session": session_cookie})
