from unittest.mock import patch

import pytest
import requests

from aoc.errors import InvalidConfiguration
from aoc.utils.data import SESSION_COOKIE, download_input


@pytest.fixture
def config_mock():
    with patch.dict("aoc.utils.config") as mock:
        yield mock


class TestDownloadInput:
    def test_fails_with_no_cookie_session(self, config_mock):
        config_mock.pop(SESSION_COOKIE, None)

        with pytest.raises(InvalidConfiguration):
            download_input(2023, 2)

    def test_request_data_from_aoc(self, config_mock, requests_mock):
        config_mock[SESSION_COOKIE] = "TEST_AOC_SESSION_COOKIE"

        year = 2023
        day = 12
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        requests_mock.get(url, text="PUZZLE_DATA")

        result = download_input(year, day)

        assert result == "PUZZLE_DATA"
        assert requests_mock.called
        assert requests_mock.request_history[0].url == url
        assert "session" in requests_mock.request_history[0]._cookies
        assert (
            requests_mock.request_history[0]._cookies["session"]
            == "TEST_AOC_SESSION_COOKIE"
        )

    def test_failure(self, config_mock, requests_mock):
        config_mock[SESSION_COOKIE] = "TEST_AOC_SESSION_COOKIE"

        year = 2023
        day = 12
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        requests_mock.get(url, status_code=400, text=f"Bad Request for url: {url}")

        with pytest.raises(requests.exceptions.HTTPError):
            download_input(2023, 12)
