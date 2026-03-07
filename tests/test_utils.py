import pytest
from finscraper.utils.requests import is_valid_url, build_url


class TestIsValidUrl:
    def test_valid_url(self):
        assert is_valid_url("https://example.com") is True

    def test_invalid_url(self):
        assert is_valid_url("not-a-url") is False

    def test_url_with_path(self):
        assert is_valid_url("https://example.com/path") is True


class TestBuildUrl:
    def test_build_simple_url(self):
        result = build_url("https://example.com", "/path")
        assert result == "https://example.com/path"

    def test_build_url_with_params(self):
        result = build_url("https://example.com", "/path", {"q": "test", "page": 1})
        assert "https://example.com/path?" in result
        assert "q=test" in result
        assert "page=1" in result
