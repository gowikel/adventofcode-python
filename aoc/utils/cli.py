import argparse
import calendar
from datetime import datetime

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


def _get_default_year():
    current = datetime.now()

    if current.month == calendar.DECEMBER:
        return current.year

    return current.year - 1


def _get_default_day():
    current = datetime.now()
    today = current.day

    if current.month == calendar.DECEMBER and today <= 25:
        return today

    return None


def parse_conf():
    parser = argparse.ArgumentParser(
        prog="aoc",
        description=CLI_DESCRIPTION,
        allow_abbrev=True,
    )
    parser.add_argument("--year", type=int, default=_get_default_year(), help=YEAR_HELP)
    parser.add_argument("--day", type=int, default=_get_default_day(), help=DAY_HELP)

    args = parser.parse_args()
    return vars(args)
