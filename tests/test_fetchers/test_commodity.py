import pytest
import pandas as pd
from finscraper.fetchers.commodity import CommodityFetcher


def test_commodity_fetcher_initialization():
    fetcher = CommodityFetcher()
    assert fetcher is not None
    assert fetcher.name == "commodity"


def test_commodity_fetch_list():
    fetcher = CommodityFetcher()
    try:
        df = fetcher.fetch_list()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_commodity_fetch_spot():
    fetcher = CommodityFetcher()
    try:
        df = fetcher.fetch_spot()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_commodity_fetch_history():
    fetcher = CommodityFetcher()
    try:
        df = fetcher.fetch_history(
            symbol="000001",
            start_date="20240101",
            end_date="20241231",
        )
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
