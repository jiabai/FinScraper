import pytest
from finscraper.cli.utils import get_log_level


def test_get_log_level():
    assert get_log_level(0) == "WARNING"
    assert get_log_level(1) == "INFO"
    assert get_log_level(2) == "DEBUG"
    assert get_log_level(3) == "DEBUG"
