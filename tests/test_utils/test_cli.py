from calendar import (APRIL, AUGUST, DECEMBER, FEBRUARY, JANUARY, JULY, JUNE,
                      MARCH, MAY, NOVEMBER, OCTOBER, SEPTEMBER)
from datetime import date, datetime

import pytest
from immobilus import immobilus

from aoc.errors import InvalidConfiguration
from aoc.utils.cli import VALID_YEARS, is_valid_date, parse_args


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


class TestIsValidDate:
    @pytest.mark.parametrize("year", VALID_YEARS)
    def test_valid_years(self, year):
        test_date = date(year, DECEMBER, 1)

        result = is_valid_date(test_date)

        assert result is True

    @pytest.mark.parametrize("year", [2022, 2024])
    def test_invalid_years(self, year):
        test_date = date(year, DECEMBER, 1)

        result = is_valid_date(test_date)

        assert result is False

    def test_december_is_valid(self):
        test_date = date(2023, DECEMBER, 1)

        result = is_valid_date(test_date)

        assert result is True

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
    def test_invalid_months(self, month):
        test_date = date(2023, month, 1)

        result = is_valid_date(test_date)

        assert result is False

    @pytest.mark.parametrize("day", range(1, 26))
    def test_valid_days(self, day):
        test_date = date(2023, DECEMBER, day)

        result = is_valid_date(test_date)

        assert result is True

    @pytest.mark.parametrize("day", range(26, 32))
    def test_invalid_days(self, day):
        test_date = date(2023, DECEMBER, day)

        result = is_valid_date(test_date)

        assert result is False
