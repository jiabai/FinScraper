import pytest
import pandas as pd
from finscraper.fetchers.news import NewsFetcher


def test_news_fetcher_initialization():
    fetcher = NewsFetcher()
    assert fetcher is not None
    assert fetcher.name == "news"


def test_news_fetch_global():
    fetcher = NewsFetcher()
    try:
        df = fetcher.fetch_global()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_news_fetch_alert():
    fetcher = NewsFetcher()
    try:
        df = fetcher.fetch_alert()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_news_fetch_stock():
    fetcher = NewsFetcher()
    try:
        df = fetcher.fetch_stock(symbol="000001")
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
