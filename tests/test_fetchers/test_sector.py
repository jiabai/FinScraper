import pytest
from finscraper.fetchers.sector import SectorFetcher


def test_sector_fetcher_initialization():
    fetcher = SectorFetcher()
    assert fetcher.name == "sector"
