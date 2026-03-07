import pytest
from finscraper.fetchers.north_flow import NorthFlowFetcher


def test_north_flow_fetcher_initialization():
    fetcher = NorthFlowFetcher()
    assert fetcher.name == "north-flow"
