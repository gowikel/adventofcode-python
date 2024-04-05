import os
from unittest.mock import patch

import pytest

from aoc.utils import load_config


@pytest.fixture
def envfile_mock():
    with patch("aoc.utils.dotenv_values") as mock:
        mock.return_value = {}
        yield mock


@pytest.fixture
def environ_mock():
    with patch.dict(os.environ, clear=True) as mock:
        yield mock


def test_reads_from_envfile(envfile_mock, environ_mock):
    # Force a clean environ. Pytest is trying to add PYTEST_CURRENT_TEST
    environ_mock.clear()

    envfile_mock.return_value["TEST_DOTENV_KEY"] = "TEST_DOTENV_VALUE"

    result = load_config()

    assert result == {
        "TEST_DOTENV_KEY": "TEST_DOTENV_VALUE",
    }


@pytest.mark.usefixtures("envfile_mock")
def test_reads_from_environ(environ_mock):
    # Force a clean environ. Pytest is trying to add PYTEST_CURRENT_TEST
    environ_mock.clear()

    environ_mock["TEST_ENVIRON_KEY"] = "TEST_ENVIRON_VALUE"

    result = load_config()

    assert result == {"TEST_ENVIRON_KEY": "TEST_ENVIRON_VALUE"}


def test_environ_has_preference_over_dotenv(envfile_mock, environ_mock):
    # Force a clean environ. Pytest is trying to add PYTEST_CURRENT_TEST
    environ_mock.clear()

    environ_mock["TEST_SHARED_KEY"] = "TEST_SHARED_ENVIRON"
    envfile_mock.return_value["TEST_SHARED_KEY"] = "TEST_SHARED_DOTENV"

    result = load_config()

    assert result == {"TEST_SHARED_KEY": "TEST_SHARED_ENVIRON"}
