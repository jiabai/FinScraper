# Phase 5: Basic Data Fetchers Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the core data fetchers (IndexFetcher, NorthFlowFetcher, SectorFetcher) that use AkShareClient to fetch real financial data.

**Architecture:** Each Fetcher inherits from BaseFetcher, uses AkShareClient to fetch data, DataCleaner to clean it, and returns data in pandas DataFrame format.

**Tech Stack:** Python 3.10+, pandas, akshare, pydantic

---

## Task 1: Implement IndexFetcher

**Files:**
- Create: `finscraper/fetchers/index.py`
- Create: `tests/test_fetchers/test_index.py`

**Step 1: Write the failing test**

```python
# tests/test_fetchers/test_index.py
import pytest
from finscraper.fetchers.index import IndexFetcher


def test_index_fetcher_initialization():
    fetcher = IndexFetcher()
    assert fetcher.name == "index"


def test_index_fetcher_fetch_spot():
    fetcher = IndexFetcher()
    result = fetcher.fetch_spot()
    assert result is not None
    assert hasattr(result, "shape")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_fetchers/test_index.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write implementation**

```python
# finscraper/fetchers/index.py
import pandas as pd
from finscraper.fetchers.base import BaseFetcher
from finscraper.core.logger import get_logger


class IndexFetcher(BaseFetcher):
    """Fetcher for A-share index data."""
    
    def __init__(self):
        super().__init__("index")
    
    def fetch(self):
        """Fetch all index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch index spot data."""
        self.logger.info("Fetching index spot data")
        
        try:
            df = self.client.fetch_index_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_index_spot(df)
                self.logger.info(f"Fetched {len(df)} index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch index spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch index historical data."""
        self.logger.info(f"Fetching index history for {symbol}")
        
        try:
            df = self.client.fetch_index_hist_zh_a(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_index_history(df)
                self.logger.info(f"Fetched {len(df)} index history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch index history for {symbol}: {e}")
            raise
```

**Step 4: Update AkShareClient with index methods**

```python
# finscraper/core/akshare_client.py
def fetch_index_spot_em(self) -> pd.DataFrame:
    """Fetch A-share index spot data from East Money."""
    return self._call_akshare("index_spot_em")


def fetch_index_hist_zh_a(
    self,
    symbol: str,
    period: str = "daily",
    start_date: str = "",
    end_date: str = "",
) -> pd.DataFrame:
    """Fetch A-share index historical data."""
    return self._call_akshare(
        "index_hist_zh_a",
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
    )
```

**Step 5: Update DataCleaner with index cleaning methods**

```python
# finscraper/core/data_cleaner.py
def clean_index_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean index spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df


def clean_index_history(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean index history data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/test_fetchers/test_index.py -v`
Expected: PASS (basic tests)

**Step 7: Commit**

```bash
git add finscraper/fetchers/index.py finscraper/core/akshare_client.py finscraper/core/data_cleaner.py tests/test_fetchers/test_index.py
git commit -m "feat: add IndexFetcher with spot and history methods"
```

---

## Task 2: Implement NorthFlowFetcher

**Files:**
- Create: `finscraper/fetchers/north_flow.py`
- Create: `tests/test_fetchers/test_north_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_fetchers/test_north_flow.py
import pytest
from finscraper.fetchers.north_flow import NorthFlowFetcher


def test_north_flow_fetcher_initialization():
    fetcher = NorthFlowFetcher()
    assert fetcher.name == "north-flow"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_fetchers/test_north_flow.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write implementation**

```python
# finscraper/fetchers/north_flow.py
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class NorthFlowFetcher(BaseFetcher):
    """Fetcher for northbound capital flow data."""
    
    def __init__(self):
        super().__init__("north-flow")
    
    def fetch(self):
        """Fetch all north flow data."""
        return self.fetch_daily()
    
    def fetch_daily(self) -> pd.DataFrame:
        """Fetch north flow daily data."""
        self.logger.info("Fetching north flow daily data")
        
        try:
            df = self.client.fetch_em_north_flow_20()
            if df is not None and not df.empty:
                df = self.cleaner.clean_north_flow_daily(df)
                self.logger.info(f"Fetched {len(df)} north flow daily records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch north flow daily data: {e}")
            raise
    
    def fetch_intraday(self) -> pd.DataFrame:
        """Fetch north flow intraday data."""
        self.logger.info("Fetching north flow intraday data")
        
        try:
            df = self.client.fetch_em_north_flow_today()
            if df is not None and not df.empty:
                df = self.cleaner.clean_north_flow_intraday(df)
                self.logger.info(f"Fetched {len(df)} north flow intraday records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch north flow intraday data: {e}")
            raise
```

**Step 4: Update AkShareClient with north flow methods**

```python
# finscraper/core/akshare_client.py
def fetch_em_north_flow_20(self) -> pd.DataFrame:
    """Fetch northbound capital flow 2020 data."""
    return self._call_akshare("em_north_flow_20")


def fetch_em_north_flow_today(self) -> pd.DataFrame:
    """Fetch northbound capital flow today data."""
    return self._call_akshare("em_north_flow_today")
```

**Step 5: Update DataCleaner with north flow cleaning methods**

```python
# finscraper/core/data_cleaner.py
def clean_north_flow_daily(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean north flow daily data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df


def clean_north_flow_intraday(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean north flow intraday data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/test_fetchers/test_north_flow.py -v`
Expected: PASS

**Step 7: Commit**

```bash
git add finscraper/fetchers/north_flow.py finscraper/core/akshare_client.py finscraper/core/data_cleaner.py tests/test_fetchers/test_north_flow.py
git commit -m "feat: add NorthFlowFetcher with daily and intraday methods"
```

---

## Task 3: Implement SectorFetcher

**Files:**
- Create: `finscraper/fetchers/sector.py`
- Create: `tests/test_fetchers/test_sector.py`

**Step 1: Write the failing test**

```python
# tests/test_fetchers/test_sector.py
import pytest
from finscraper.fetchers.sector import SectorFetcher


def test_sector_fetcher_initialization():
    fetcher = SectorFetcher()
    assert fetcher.name == "sector"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_fetchers/test_sector.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write implementation**

```python
# finscraper/fetchers/sector.py
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class SectorFetcher(BaseFetcher):
    """Fetcher for sector data."""
    
    def __init__(self):
        super().__init__("sector")
    
    def fetch(self):
        """Fetch all sector data."""
        return self.fetch_spot()
    
    def fetch_list(self) -> pd.DataFrame:
        """Fetch sector list."""
        self.logger.info("Fetching sector list")
        
        try:
            df = self.client.fetch_sector_list_ths()
            if df is not None and not df.empty:
                df = self.cleaner.clean_sector_list(df)
                self.logger.info(f"Fetched {len(df)} sectors")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch sector list: {e}")
            raise
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch sector spot data."""
        self.logger.info("Fetching sector spot data")
        
        try:
            df = self.client.fetch_sector_spot_ths()
            if df is not None and not df.empty:
                df = self.cleaner.clean_sector_spot(df)
                self.logger.info(f"Fetched {len(df)} sector spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch sector spot data: {e}")
            raise
    
    def fetch_stocks(self, sector: str) -> pd.DataFrame:
        """Fetch sector constituent stocks."""
        self.logger.info(f"Fetching stocks for sector: {sector}")
        
        try:
            df = self.client.fetch_sector_detail_ths(symbol=sector)
            if df is not None and not df.empty:
                df = self.cleaner.clean_sector_stocks(df)
                self.logger.info(f"Fetched {len(df)} stocks for sector {sector}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch stocks for sector {sector}: {e}")
            raise
```

**Step 4: Update AkShareClient with sector methods**

```python
# finscraper/core/akshare_client.py
def fetch_sector_list_ths(self) -> pd.DataFrame:
    """Fetch sector list from TongHuaShun."""
    return self._call_akshare("sector_list_ths")


def fetch_sector_spot_ths(self) -> pd.DataFrame:
    """Fetch sector spot data from TongHuaShun."""
    return self._call_akshare("sector_spot_ths")


def fetch_sector_detail_ths(self, symbol: str) -> pd.DataFrame:
    """Fetch sector detail from TongHuaShun."""
    return self._call_akshare("sector_detail_ths", symbol=symbol)
```

**Step 5: Update DataCleaner with sector cleaning methods**

```python
# finscraper/core/data_cleaner.py
def clean_sector_list(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean sector list data."""
    df = df.copy()
    df = self.clean_column_names(df)
    return df


def clean_sector_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean sector spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df


def clean_sector_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean sector stocks data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/test_fetchers/test_sector.py -v`
Expected: PASS

**Step 7: Commit**

```bash
git add finscraper/fetchers/sector.py finscraper/core/akshare_client.py finscraper/core/data_cleaner.py tests/test_fetchers/test_sector.py
git commit -m "feat: add SectorFetcher with list, spot, and stocks methods"
```

---

## Task 4: Run All Fetcher Tests

**Step 1: Run full fetcher test suite**

Run: `pytest tests/test_fetchers/ -v`
Expected: All tests pass

**Step 2: Run integration test (optional)**

Run: `python -c "from finscraper.fetchers.index import IndexFetcher; f = IndexFetcher(); print('IndexFetcher initialized successfully')"`

**Step 3: Commit**

```bash
git add tests/test_fetchers/
git commit -m "test: ensure all fetcher tests pass"
```

---

## Task 5: Update Documentation

**Files:**
- Update: `README.md`

**Step 1: Update README with fetcher usage**

```markdown
## Python API 使用

### IndexFetcher

```python
from finscraper.fetchers.index import IndexFetcher
from finscraper.storage.csv_storage import CSVStorage

# 获取指数实时行情
fetcher = IndexFetcher()
data = fetcher.fetch_spot()
print(data)

# 保存到文件
storage = CSVStorage()
storage.save(data, "data/index/spot.csv")

# 获取历史数据
history = fetcher.fetch_history(
    symbol="000001",
    start_date="20240101",
    end_date="20241231",
    period="daily",
)
```

### NorthFlowFetcher

```python
from finscraper.fetchers.north_flow import NorthFlowFetcher

fetcher = NorthFlowFetcher()
daily = fetcher.fetch_daily()
intraday = fetcher.fetch_intraday()
```

### SectorFetcher

```python
from finscraper.fetchers.sector import SectorFetcher

fetcher = SectorFetcher()
sectors = fetcher.fetch_list()
spot = fetcher.fetch_spot()
stocks = fetcher.fetch_stocks("sector_code")
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with fetcher usage examples"
```

---

## Summary

This plan implements the core data fetchers:

1. ✅ IndexFetcher - A-share index (spot, history)
2. ✅ NorthFlowFetcher - Northbound capital flow (daily, intraday)
3. ✅ SectorFetcher - Sector data (list, spot, stocks)
4. ✅ Run all fetcher tests
5. ✅ Update documentation

**Next Steps:** Proceed to Phase 4 (CLI Command Implementation) after completing this plan.
