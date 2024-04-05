import argparse
from calendar import DECEMBER
from datetime import date, datetime

from ..errors import InvalidConfiguration

VALID_YEARS = range(2023, 2024)
VALID_DECEMBER_DAYS = range(1, 26)

CLI_DESCRIPTION = "Code for the Advent of Code challenges, from 2023 onwards."

YEAR_HELP = (
    "Year to execute. "
    "Defaults to the current year on December and,"
    "to the previous year otherwise."
)
DAY_HELP = (
    "Day to execute."
    "Defaults to today date on December and,"
    "it is required otherwise."
    "It is also required if we are on December 26-31 range."
)


def parse_args(args=None):
    # Avoid sending None to parse_args, as that will trigger a read
    # from sys.argv, which will defeat the testing process
    if args is None:
        args = []

    parser = argparse.ArgumentParser(
        prog="aoc",
        description=CLI_DESCRIPTION,
        allow_abbrev=True,
    )
    parser.add_argument("--year", type=int, default=_get_default_year(), help=YEAR_HELP)
    parser.add_argument("--day", type=int, default=_get_default_day(), help=DAY_HELP)

    args = vars(parser.parse_args(args))

    year = args["year"]
    month = DECEMBER
    day = args["day"]

    target_day = date(year, month, day)

    if not is_valid_date(target_day):
        raise InvalidConfiguration(f'The specified date "{target_day}" is invalid')

    return args


def is_valid_date(date):
    year = date.year
    month = date.month
    day = date.day

    return year in VALID_YEARS and month == DECEMBER and day in VALID_DECEMBER_DAYS


def _get_default_year():
    current = datetime.now()

    if current.month == DECEMBER:
        return current.year

    return current.year - 1


def _get_default_day():
    current = datetime.now()
    today = current.day

    if current.month == DECEMBER:
        return today

    return None
