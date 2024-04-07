from unittest.mock import patch

import pytest
import requests
from fs.memoryfs import MemoryFS

from aoc.errors import InvalidConfiguration
from aoc.utils.data import (
    SESSION_COOKIE,
    download_input,
    get_puzzle_data,
    purge_cache,
    puzzle_filename,
)


@pytest.fixture
def config_mock():
    with patch.dict("aoc.utils.config") as mock:
        yield mock


@pytest.fixture
def dowload_input_mock():
    with patch("aoc.utils.data.download_input") as mock:
        yield mock


@pytest.fixture
def cache_fs_mock():
    with patch("aoc.utils.data.cache_fs", MemoryFS()) as mock:
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


class TestPuzzleFilename:
    def test_happy_path(self):
        year = 2023
        day = 12
        expected_filename = f"AOC_{year}_{day}.txt"
        result = puzzle_filename(year, day)

        assert result == expected_filename


class TestGetPuzzleData:
    @pytest.mark.usefixtures("cache_fs_mock")
    def test_input_is_fetched_when_cache_is_empty(self, dowload_input_mock):
        year = 2023
        day = 12
        dowload_input_mock.return_value = "PUZZLE_DATA"

        result = get_puzzle_data(year, day)
        result_data = result.read()

        assert result_data == "PUZZLE_DATA"
        dowload_input_mock.assert_called_once_with(year, day)

    def test_cache_is_populated(self, cache_fs_mock, dowload_input_mock):
        year = 2023
        day = 12
        filename = puzzle_filename(year, day)
        dowload_input_mock.return_value = "PUZZLE_DATA"

        assert cache_fs_mock.exists(filename) is False

        get_puzzle_data(year, day)

        assert cache_fs_mock.exists(filename) is True
        assert cache_fs_mock.readtext(filename) == "PUZZLE_DATA"

    def test_input_is_retrieved_from_cache(self, dowload_input_mock, cache_fs_mock):
        year = 2023
        day = 12
        filename = puzzle_filename(year, day)

        cache_fs_mock.writetext(filename, "PUZZLE_DATA")

        result = get_puzzle_data(year, day)
        result_data = result.read()

        assert result_data == "PUZZLE_DATA"
        dowload_input_mock.assert_not_called()


class TestPurgeCache:
    def test_cache_is_deleted(self, cache_fs_mock):
        cache_fs_mock.touch("data.txt")
        assert cache_fs_mock.exists("/") is True
        assert cache_fs_mock.isempty("/") is False

        purge_cache()
        assert cache_fs_mock.exists("/") is True
        assert cache_fs_mock.isempty("/") is True
