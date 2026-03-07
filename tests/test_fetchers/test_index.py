import pytest
from finscraper.fetchers.index import IndexFetcher


def test_index_fetcher_initialization():
    fetcher = IndexFetcher()
    assert fetcher.name == "index"
