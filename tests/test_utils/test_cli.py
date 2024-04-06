from calendar import (
    APRIL,
    AUGUST,
    DECEMBER,
    FEBRUARY,
    JANUARY,
    JULY,
    JUNE,
    MARCH,
    MAY,
    NOVEMBER,
    OCTOBER,
    SEPTEMBER,
)
from datetime import date, datetime

import pytest
from immobilus import immobilus

from aoc.errors import InvalidConfiguration
from aoc.utils.cli import VALID_YEARS, parse_args


class TestParseArgs:
    class TestDefaults:
        @immobilus("2023-12-01")
        def test_gets_current_year_on_december(self):
            result = parse_args()
            assert result["year"] == 2023

        @pytest.mark.parametrize("day", range(1, 26))
        def test_gets_current_day_on_december(self, day):
            test_date = datetime(2023, DECEMBER, day)

            with immobilus(test_date):
                result = parse_args()
                assert result["day"] == day

        @pytest.mark.parametrize(
            "month",
            [
                JANUARY,
                FEBRUARY,
                MARCH,
                APRIL,
                MAY,
                JUNE,
                JULY,
                AUGUST,
                SEPTEMBER,
                OCTOBER,
                NOVEMBER,
            ],
        )
        def test_gets_previous_year_on_other_months(self, month):
            test_date = datetime(2024, month, 1)

            with immobilus(test_date):
                result = parse_args(["--day", "1"])
                assert result["year"] == 2023

        @pytest.mark.parametrize("day", range(26, 32))
        def test_invalid_december_days(self, day):
            test_date = datetime(2023, DECEMBER, day)

            with immobilus(test_date):
                with pytest.raises(InvalidConfiguration):
                    parse_args()

    class TestParse:
        @pytest.mark.parametrize("year", VALID_YEARS)
        @immobilus("2023-12-04")
        def test_year_is_correctly_parsed(self, year):
            result = parse_args(["--year", str(year)])

            assert result["year"] == year

        @pytest.mark.parametrize("day", range(1, 26))
        @immobilus("2023-12-04")
        def test_day_is_correctly_parsed(self, day):
            result = parse_args(["--day", str(day)])

            assert result["day"] == day

    class TestInvalidDates:
        @pytest.mark.parametrize("year", [2022, 2024])
        @immobilus("2023-12-04")
        def test_invalid_year(self, year):
            with pytest.raises(InvalidConfiguration):
                parse_args(["--year", str(year)])

        @pytest.mark.parametrize("day", range(26, 32))
        @immobilus("2023-12-04")
        def test_invalid_days_on_december(self, day):
            with pytest.raises(InvalidConfiguration):
                parse_args(["--day", str(day)])
