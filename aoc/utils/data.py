import requests

from ..errors import InvalidConfiguration
from . import config

SESSION_COOKIE = "SESSION_COOKIE"


def download_input(year: int, day: int):
    """
    Downloads the given puzzle. It will raise an exception if the
    session_cookie is not found, or if there is any error downloading the data.
    """
    session_cookie = config.get(SESSION_COOKIE)

    if session_cookie is None:
        raise InvalidConfiguration("SESSION_COOKIE not found")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    result = requests.get(url, cookies={"session": session_cookie})

    result.raise_for_status()
    return result.text
