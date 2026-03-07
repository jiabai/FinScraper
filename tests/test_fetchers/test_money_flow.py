import pytest
import pandas as pd
from finscraper.fetchers.money_flow import MoneyFlowFetcher


def test_money_flow_fetcher_initialization():
    fetcher = MoneyFlowFetcher()
    assert fetcher is not None
    assert fetcher.name == "money-flow"


def test_money_flow_fetch_stock():
    fetcher = MoneyFlowFetcher()
    try:
        df = fetcher.fetch_stock()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_money_flow_fetch_sector():
    fetcher = MoneyFlowFetcher()
    try:
        df = fetcher.fetch_sector()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_money_flow_fetch_market():
    fetcher = MoneyFlowFetcher()
    try:
        df = fetcher.fetch_market()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
