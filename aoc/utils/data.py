from typing import IO

import requests
from fs.appfs import UserCacheFS

from ..errors import InvalidConfiguration
from . import config

SESSION_COOKIE = "SESSION_COOKIE"

cache_fs = UserCacheFS(appname="aoc", author="gowikel")


def download_input(year: int, day: int) -> str:
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


def puzzle_filename(year: int, day: int) -> str:
    """A utility function to name puzzle files"""
    return f"AOC_{year}_{day}.txt"


def get_puzzle_data(year: int, day: int) -> IO:
    """
    Fetches the puzzle data and stores it in a cache.

    Subsequent calls will not download the data again, but load it from
    the cached folder
    """
    filename = puzzle_filename(year, day)
    if cache_fs.exists(filename):
        return cache_fs.open(filename)

    data = download_input(year, day)
    cache_fs.writetext(filename, data)
    return cache_fs.open(filename)
