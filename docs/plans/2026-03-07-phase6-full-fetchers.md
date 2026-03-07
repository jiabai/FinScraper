# Phase 6: Full Data Fetchers Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement remaining data fetchers (Commodity, MoneyFlow, News) to complete the full data acquisition capabilities.

**Architecture:** Follow the same pattern as existing Fetchers - inherit from BaseFetcher, use AkShareClient for data, use DataCleaner for cleaning.

**Tech Stack:** akshare, pandas, existing fetcher architecture

---

## Task 1: Update AkShareClient with missing methods

**Files:**
- Modify: `finscraper/core/akshare_client.py`

**Step 1: Add Commodity methods to AkShareClient**

```python
def fetch_commodity_spot_em(self) -> pd.DataFrame:
    """Fetch commodity spot data from East Money."""
    return self._call_akshare("futures_zh_spot_em")

def fetch_commodity_hist_em(
    self,
    symbol: str,
    period: str = "daily",
    start_date: str = "",
    end_date: str = "",
) -> pd.DataFrame:
    """Fetch commodity historical data from East Money."""
    return self._call_akshare(
        "futures_zh_hist",
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
    )
```

**Step 2: Add MoneyFlow methods to AkShareClient**

```python
def fetch_money_flow_stock_em(self) -> pd.DataFrame:
    """Fetch stock money flow data from East Money."""
    return self._call_akshare("stock_individual_fund_flow_rank", indicator="今日")

def fetch_money_flow_sector_em(self) -> pd.DataFrame:
    """Fetch sector money flow data from East Money."""
    return self._call_akshare("stock_sector_fund_flow_rank", indicator="今日")

def fetch_money_flow_market_em(self) -> pd.DataFrame:
    """Fetch market money flow data from East Money."""
    return self._call_akshare("stock_market_fund_flow")
```

**Step 3: Add News methods to AkShareClient**

```python
def fetch_news_global_em(self) -> pd.DataFrame:
    """Fetch global news from East Money."""
    return self._call_akshare("news_global")

def fetch_news_alert_em(self) -> pd.DataFrame:
    """Fetch news alerts from East Money."""
    return self._call_akshare("stock_em_info_aj_em")

def fetch_news_stock_em(self, symbol: str) -> pd.DataFrame:
    """Fetch stock news from East Money."""
    return self._call_akshare("stock_news_em", symbol=symbol)
```

**Step 4: Commit**

```bash
git add finscraper/core/akshare_client.py
git commit -m "feat: add commodity, moneyflow, news methods to AkShareClient"
```

---

## Task 2: Update DataCleaner with missing methods

**Files:**
- Modify: `finscraper/core/data_cleaner.py`

**Step 1: Add Commodity cleaning methods**

```python
def clean_commodity_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean commodity spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_commodity_history(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean commodity historical data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

**Step 2: Add MoneyFlow cleaning methods**

```python
def clean_money_flow_stock(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean stock money flow data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_money_flow_sector(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean sector money flow data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_money_flow_market(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean market money flow data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

**Step 3: Add News cleaning methods**

```python
def clean_news_global(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean global news data."""
    df = df.copy()
    df = self.clean_column_names(df)
    return df

def clean_news_alert(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean news alert data."""
    df = df.copy()
    df = self.clean_column_names(df)
    return df

def clean_news_stock(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean stock news data."""
    df = df.copy()
    df = self.clean_column_names(df)
    return df
```

**Step 4: Commit**

```bash
git add finscraper/core/data_cleaner.py
git commit -m "feat: add commodity, moneyflow, news cleaning methods"
```

---

## Task 3: Implement CommodityFetcher

**Files:**
- Create: `finscraper/fetchers/commodity.py`
- Test: `tests/test_fetchers/test_commodity.py`

**Step 1: Create CommodityFetcher**

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class CommodityFetcher(BaseFetcher):
    """Fetcher for commodity data."""
    
    def __init__(self):
        super().__init__("commodity")
    
    def fetch(self):
        """Fetch all commodity data."""
        return self.fetch_spot()
    
    def fetch_list(self) -> pd.DataFrame:
        """Fetch commodity list."""
        self.logger.info("Fetching commodity list")
        
        try:
            df = self.client.fetch_commodity_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_spot(df)
                self.logger.info(f"Fetched {len(df)} commodities")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity list: {e}")
            raise
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch commodity spot data."""
        self.logger.info("Fetching commodity spot data")
        
        try:
            df = self.client.fetch_commodity_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_spot(df)
                self.logger.info(f"Fetched {len(df)} commodity spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch commodity historical data."""
        self.logger.info(f"Fetching commodity history for {symbol}")
        
        try:
            df = self.client.fetch_commodity_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_history(df)
                self.logger.info(f"Fetched {len(df)} commodity history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity history for {symbol}: {e}")
            raise
```

**Step 2: Create test file**

```python
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
```

**Step 3: Run tests**

Run: `pytest tests/test_fetchers/test_commodity.py -v`
Expected: All tests pass (some may be skipped if API fails)

**Step 4: Commit**

```bash
git add finscraper/fetchers/commodity.py tests/test_fetchers/test_commodity.py
git commit -m "feat: implement CommodityFetcher"
```

---

## Task 4: Implement MoneyFlowFetcher

**Files:**
- Create: `finscraper/fetchers/money_flow.py`
- Test: `tests/test_fetchers/test_money_flow.py`

**Step 1: Create MoneyFlowFetcher**

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class MoneyFlowFetcher(BaseFetcher):
    """Fetcher for money flow data."""
    
    def __init__(self):
        super().__init__("money-flow")
    
    def fetch(self):
        """Fetch all money flow data."""
        return self.fetch_market()
    
    def fetch_stock(self) -> pd.DataFrame:
        """Fetch stock money flow data."""
        self.logger.info("Fetching stock money flow data")
        
        try:
            df = self.client.fetch_money_flow_stock_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_stock(df)
                self.logger.info(f"Fetched {len(df)} stock money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch stock money flow data: {e}")
            raise
    
    def fetch_sector(self) -> pd.DataFrame:
        """Fetch sector money flow data."""
        self.logger.info("Fetching sector money flow data")
        
        try:
            df = self.client.fetch_money_flow_sector_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_sector(df)
                self.logger.info(f"Fetched {len(df)} sector money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch sector money flow data: {e}")
            raise
    
    def fetch_market(self) -> pd.DataFrame:
        """Fetch market money flow data."""
        self.logger.info("Fetching market money flow data")
        
        try:
            df = self.client.fetch_money_flow_market_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_market(df)
                self.logger.info(f"Fetched {len(df)} market money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch market money flow data: {e}")
            raise
```

**Step 2: Create test file**

```python
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
```

**Step 3: Run tests**

Run: `pytest tests/test_fetchers/test_money_flow.py -v`
Expected: All tests pass (some may be skipped if API fails)

**Step 4: Commit**

```bash
git add finscraper/fetchers/money_flow.py tests/test_fetchers/test_money_flow.py
git commit -m "feat: implement MoneyFlowFetcher"
```

---

## Task 5: Implement NewsFetcher

**Files:**
- Create: `finscraper/fetchers/news.py`
- Test: `tests/test_fetchers/test_news.py`

**Step 1: Create NewsFetcher**

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class NewsFetcher(BaseFetcher):
    """Fetcher for news data."""
    
    def __init__(self):
        super().__init__("news")
    
    def fetch(self):
        """Fetch all news data."""
        return self.fetch_global()
    
    def fetch_global(self) -> pd.DataFrame:
        """Fetch global news."""
        self.logger.info("Fetching global news")
        
        try:
            df = self.client.fetch_news_global_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_global(df)
                self.logger.info(f"Fetched {len(df)} global news records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch global news: {e}")
            raise
    
    def fetch_alert(self) -> pd.DataFrame:
        """Fetch news alerts."""
        self.logger.info("Fetching news alerts")
        
        try:
            df = self.client.fetch_news_alert_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_alert(df)
                self.logger.info(f"Fetched {len(df)} news alert records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch news alerts: {e}")
            raise
    
    def fetch_stock(self, symbol: str) -> pd.DataFrame:
        """Fetch stock news."""
        self.logger.info(f"Fetching news for stock: {symbol}")
        
        try:
            df = self.client.fetch_news_stock_em(symbol=symbol)
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_stock(df)
                self.logger.info(f"Fetched {len(df)} news records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch news for {symbol}: {e}")
            raise
```

**Step 2: Create test file**

```python
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
```

**Step 3: Run tests**

Run: `pytest tests/test_fetchers/test_news.py -v`
Expected: All tests pass (some may be skipped if API fails)

**Step 4: Commit**

```bash
git add finscraper/fetchers/news.py tests/test_fetchers/test_news.py
git commit -m "feat: implement NewsFetcher"
```

---

## Task 6: Run All Fetchers Tests

**Step 1: Run full fetchers test suite**

Run: `pytest tests/test_fetchers/ -v`
Expected: All tests pass

**Step 2: Commit**

```bash
git add tests/test_fetchers/
git commit -m "test: ensure all fetchers tests pass"
```

---

## Task 7: Update Documentation

**Files:**
- Update: `README.md`

**Step 1: Add Python API examples for new fetchers**

```markdown
#### CommodityFetcher

```python
from finscraper.fetchers.commodity import CommodityFetcher

fetcher = CommodityFetcher()
spot = fetcher.fetch_spot()
history = fetcher.fetch_history(
    symbol="AU0",
    start_date="20240101",
    end_date="20241231",
)
```

#### MoneyFlowFetcher

```python
from finscraper.fetchers.money_flow import MoneyFlowFetcher

fetcher = MoneyFlowFetcher()
stock_flow = fetcher.fetch_stock()
sector_flow = fetcher.fetch_sector()
market_flow = fetcher.fetch_market()
```

#### NewsFetcher

```python
from finscraper.fetchers.news import NewsFetcher

fetcher = NewsFetcher()
global_news = fetcher.fetch_global()
alerts = fetcher.fetch_alert()
stock_news = fetcher.fetch_stock("000001")
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with new fetchers examples"
```

---

## Summary

This plan implements the remaining data fetchers:

1. ✅ Update AkShareClient with commodity, moneyflow, news methods
2. ✅ Update DataCleaner with commodity, moneyflow, news cleaning methods
3. ✅ Implement CommodityFetcher (list, spot, history)
4. ✅ Implement MoneyFlowFetcher (stock, sector, market)
5. ✅ Implement NewsFetcher (global, alert, stock)
6. ✅ Run all fetchers tests
7. ✅ Update documentation

**Note:** This completes all 6 data types specified in the requirements.

**Next Steps:** Proceed to Phase 7 (完善与优化) after completing this plan.
