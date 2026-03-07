# Phase 2: Core Framework Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the core framework including logging system, data models, akshare client, data cleaner, base fetcher, storage layer, and exception handling.

**Architecture:** Layered architecture with clear separation of concerns. Core layer provides akshare API abstraction and data cleaning. Models layer uses Pydantic for type safety. Storage layer supports multiple formats. All layers use centralized logging and exception handling.

**Tech Stack:** Python 3.10+, Pydantic 2.0+, Loguru 0.7+, Pandas 2.0+, Akshare 1.12+

---

## Task 1: Implement Logging System

**Files:**
- Create: `finscraper/core/logger.py`
- Create: `tests/test_core/test_logger.py`

**Step 1: Write the failing test**

```python
# tests/test_core/test_logger.py
import pytest
from finscraper.core.logger import get_logger, set_log_level


def test_get_logger_returns_logger():
    logger = get_logger("test_module")
    assert logger is not None
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")


def test_set_log_level():
    import os
    os.environ["FINSCRAPER_LOG_LEVEL"] = "DEBUG"
    logger = get_logger("test_debug")
    assert logger is not None


def test_logger_writes_to_file(tmp_path):
    import os
    from pathlib import Path
    
    log_file = tmp_path / "test.log"
    os.environ["FINSCRAPER_LOG_FILE"] = str(log_file)
    
    logger = get_logger("test_file")
    logger.info("Test message")
    
    assert log_file.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_core/test_logger.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.core.logger'"

**Step 3: Create test directory structure**

Run: `mkdir -p tests/test_core`
Run: `touch tests/test_core/__init__.py`

**Step 4: Write minimal implementation**

```python
# finscraper/core/logger.py
import sys
from pathlib import Path
from loguru import logger
from finscraper.config.settings import Settings


def get_logger(name: str):
    """Get a logger instance for the given module name."""
    settings = Settings()
    
    logger.remove()
    
    log_level = settings.log_level
    logger.add(sys.stderr, level=log_level, format="{time} | {level} | {name} | {message}")
    
    log_file = Path(settings.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(log_file, level="DEBUG", rotation="1 day", retention="7 days")
    
    return logger.bind(name=name)


def set_log_level(level: str):
    """Set the global log level."""
    import os
    os.environ["FINSCRAPER_LOG_LEVEL"] = level.upper()
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_core/test_logger.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add tests/test_core/ finscraper/core/logger.py
git commit -m "feat: add logging system with loguru"
```

---

## Task 2: Implement Custom Exceptions

**Files:**
- Create: `finscraper/core/exceptions.py`
- Create: `tests/test_core/test_exceptions.py`

**Step 1: Write the failing test**

```python
# tests/test_core/test_exceptions.py
import pytest
from finscraper.core.exceptions import (
    FinScraperError,
    NetworkError,
    DataError,
    StorageError,
    ValidationError,
)


def test_base_exception():
    error = FinScraperError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_network_error():
    error = NetworkError("Connection failed", status_code=500)
    assert str(error) == "Connection failed"
    assert error.status_code == 500


def test_data_error():
    error = DataError("Invalid data format", field="price")
    assert str(error) == "Invalid data format"
    assert error.field == "price"


def test_storage_error():
    error = StorageError("File write failed", path="/tmp/test.csv")
    assert str(error) == "File write failed"
    assert error.path == "/tmp/test.csv"


def test_validation_error():
    error = ValidationError("Invalid parameter", param="symbol")
    assert str(error) == "Invalid parameter"
    assert error.param == "symbol"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_core/test_exceptions.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.core.exceptions'"

**Step 3: Write minimal implementation**

```python
# finscraper/core/exceptions.py
from typing import Optional


class FinScraperError(Exception):
    """Base exception for FinScraper."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NetworkError(FinScraperError):
    """Network-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class DataError(FinScraperError):
    """Data-related errors."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


class StorageError(FinScraperError):
    """Storage-related errors."""
    
    def __init__(self, message: str, path: Optional[str] = None):
        self.path = path
        super().__init__(message)


class ValidationError(FinScraperError):
    """Validation-related errors."""
    
    def __init__(self, message: str, param: Optional[str] = None):
        self.param = param
        super().__init__(message)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_core/test_exceptions.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/core/exceptions.py tests/test_core/test_exceptions.py
git commit -m "feat: add custom exception classes"
```

---

## Task 3: Implement Retry Mechanism

**Files:**
- Create: `finscraper/core/retry.py`
- Create: `tests/test_core/test_retry.py`

**Step 1: Write the failing test**

```python
# tests/test_core/test_retry.py
import pytest
from finscraper.core.retry import retry_with_backoff


def test_retry_success_on_first_attempt():
    call_count = 0
    
    @retry_with_backoff(max_retries=3, delay=0.1)
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = successful_function()
    assert result == "success"
    assert call_count == 1


def test_retry_success_after_failures():
    call_count = 0
    
    @retry_with_backoff(max_retries=3, delay=0.1)
    def eventually_successful_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary error")
        return "success"
    
    result = eventually_successful_function()
    assert result == "success"
    assert call_count == 3


def test_retry_max_retries_exceeded():
    call_count = 0
    
    @retry_with_backoff(max_retries=2, delay=0.1)
    def always_failing_function():
        nonlocal call_count
        call_count += 1
        raise ValueError("Permanent error")
    
    with pytest.raises(ValueError, match="Permanent error"):
        always_failing_function()
    
    assert call_count == 3  # Initial + 2 retries
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_core/test_retry.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.core.retry'"

**Step 3: Write minimal implementation**

```python
# finscraper/core/retry.py
import time
import functools
from typing import Callable, Type, Tuple
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    delay: float = 2.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Retry decorator with exponential backoff."""
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed. "
                            f"Last error: {e}"
                        )
            
            raise last_exception
        
        return wrapper
    
    return decorator
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_core/test_retry.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/core/retry.py tests/test_core/test_retry.py
git commit -m "feat: add retry mechanism with exponential backoff"
```

---

## Task 4: Implement Index Data Models

**Files:**
- Create: `finscraper/models/index.py`
- Create: `tests/test_models/test_index.py`

**Step 1: Write the failing test**

```python
# tests/test_models/test_index.py
import pytest
from datetime import datetime
from finscraper.models.index import IndexSpot, IndexHistory


def test_index_spot_creation():
    spot = IndexSpot(
        symbol="000001",
        name="上证指数",
        price=3000.50,
        change=10.50,
        change_percent=0.35,
        volume=1000000,
        amount=150000000.0,
        high=3010.0,
        low=2990.0,
        open=2995.0,
        close=3000.50,
        updated_at=datetime(2024, 1, 1, 15, 0, 0)
    )
    
    assert spot.symbol == "000001"
    assert spot.name == "上证指数"
    assert spot.price == 3000.50
    assert spot.change_percent == 0.35


def test_index_history_creation():
    history = IndexHistory(
        symbol="000001",
        date=datetime(2024, 1, 1),
        open=2995.0,
        high=3010.0,
        low=2990.0,
        close=3000.50,
        volume=1000000,
        amount=150000000.0
    )
    
    assert history.symbol == "000001"
    assert history.close == 3000.50


def test_index_spot_validation():
    with pytest.raises(ValueError):
        IndexSpot(
            symbol="000001",
            name="上证指数",
            price="invalid",  # Should be float
            change=10.50,
            change_percent=0.35,
            volume=1000000,
            amount=150000000.0,
            high=3010.0,
            low=2990.0,
            open=2995.0,
            close=3000.50,
            updated_at=datetime(2024, 1, 1, 15, 0, 0)
        )
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models/test_index.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.models.index'"

**Step 3: Create test directory structure**

Run: `mkdir -p tests/test_models`
Run: `touch tests/test_models/__init__.py`

**Step 4: Write minimal implementation**

```python
# finscraper/models/index.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IndexSpot(BaseModel):
    """A-share index spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    amount: float
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class IndexHistory(BaseModel):
    """A-share index history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_models/test_index.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/models/index.py tests/test_models/
git commit -m "feat: add index data models"
```

---

## Task 5: Implement North Flow Data Models

**Files:**
- Create: `finscraper/models/north_flow.py`
- Create: `tests/test_models/test_north_flow.py`

**Step 1: Write the failing test**

```python
# tests/test_models/test_north_flow.py
import pytest
from datetime import datetime
from finscraper.models.north_flow import NorthFlowDaily, NorthFlowIntraday


def test_north_flow_daily_creation():
    flow = NorthFlowDaily(
        date=datetime(2024, 1, 1),
        sh_net_inflow=100000000.0,
        sz_net_inflow=80000000.0,
        total_net_inflow=180000000.0,
        sh_net_buy=95000000.0,
        sz_net_buy=75000000.0,
        total_net_buy=170000000.0
    )
    
    assert flow.date == datetime(2024, 1, 1)
    assert flow.total_net_inflow == 180000000.0


def test_north_flow_intraday_creation():
    flow = NorthFlowIntraday(
        time=datetime(2024, 1, 1, 9, 30, 0),
        sh_net_inflow=50000000.0,
        sz_net_inflow=40000000.0,
        total_net_inflow=90000000.0
    )
    
    assert flow.time.hour == 9
    assert flow.total_net_inflow == 90000000.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models/test_north_flow.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.models.north_flow'"

**Step 3: Write minimal implementation**

```python
# finscraper/models/north_flow.py
from pydantic import BaseModel
from datetime import datetime


class NorthFlowDaily(BaseModel):
    """North-bound capital flow daily data model."""
    
    date: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
    sh_net_buy: float
    sz_net_buy: float
    total_net_buy: float


class NorthFlowIntraday(BaseModel):
    """North-bound capital flow intraday data model."""
    
    time: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models/test_north_flow.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/models/north_flow.py tests/test_models/test_north_flow.py
git commit -m "feat: add north flow data models"
```

---

## Task 6: Implement Remaining Data Models

**Files:**
- Create: `finscraper/models/sector.py`
- Create: `finscraper/models/commodity.py`
- Create: `finscraper/models/money_flow.py`
- Create: `finscraper/models/news.py`
- Create: `tests/test_models/test_sector.py`
- Create: `tests/test_models/test_commodity.py`
- Create: `tests/test_models/test_money_flow.py`
- Create: `tests/test_models/test_news.py`

**Step 1: Write all failing tests**

```python
# tests/test_models/test_sector.py
import pytest
from datetime import datetime
from finscraper.models.sector import SectorSpot, SectorStock


def test_sector_spot_creation():
    spot = SectorSpot(
        sector_code="BK0001",
        sector_name="半导体",
        change_percent=2.5,
        lead_stock="中芯国际",
        lead_stock_change_percent=5.0,
        total_stock_count=50,
        up_count=35,
        down_count=15,
        amount=1000000000.0,
        updated_at=datetime(2024, 1, 1, 15, 0, 0)
    )
    assert spot.sector_name == "半导体"


# tests/test_models/test_commodity.py
from finscraper.models.commodity import CommoditySpot, CommodityHistory


def test_commodity_spot_creation():
    spot = CommoditySpot(
        symbol="AU",
        name="黄金",
        price=2000.50,
        change=10.50,
        change_percent=0.53,
        unit="USD/oz",
        high=2010.0,
        low=1990.0,
        open=1995.0,
        close=2000.50,
        updated_at=datetime(2024, 1, 1, 15, 0, 0)
    )
    assert spot.name == "黄金"


# tests/test_models/test_money_flow.py
from finscraper.models.money_flow import StockMoneyFlow, SectorMoneyFlow


def test_stock_money_flow_creation():
    flow = StockMoneyFlow(
        stock_code="000001",
        stock_name="平安银行",
        date=datetime(2024, 1, 1),
        main_net_inflow=50000000.0,
        main_net_inflow_percent=1.5,
        super_large_net_inflow=30000000.0,
        super_large_net_inflow_percent=0.9,
        large_net_inflow=20000000.0,
        large_net_inflow_percent=0.6,
        medium_net_inflow=-10000000.0,
        medium_net_inflow_percent=-0.3,
        small_net_inflow=-5000000.0,
        small_net_inflow_percent=-0.15
    )
    assert flow.stock_name == "平安银行"


# tests/test_models/test_news.py
from finscraper.models.news import NewsItem


def test_news_item_creation():
    news = NewsItem(
        title="央行宣布降准",
        content="中国人民银行决定下调存款准备金率...",
        source="新华社",
        publish_time=datetime(2024, 1, 1, 10, 0, 0),
        url="https://example.com/news/1",
        importance=5
    )
    assert news.title == "央行宣布降准"
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_models/ -v`
Expected: FAIL with multiple "ModuleNotFoundError"

**Step 3: Write minimal implementations**

```python
# finscraper/models/sector.py
from pydantic import BaseModel
from datetime import datetime


class SectorSpot(BaseModel):
    """Sector spot data model."""
    
    sector_code: str
    sector_name: str
    change_percent: float
    lead_stock: str
    lead_stock_change_percent: float
    total_stock_count: int
    up_count: int
    down_count: int
    amount: float
    updated_at: datetime


class SectorStock(BaseModel):
    """Sector stock data model."""
    
    sector_code: str
    sector_name: str
    stock_code: str
    stock_name: str
    change_percent: float
    price: float
    volume: int
    amount: float


# finscraper/models/commodity.py
from pydantic import BaseModel
from datetime import datetime


class CommoditySpot(BaseModel):
    """Commodity spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    unit: str
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class CommodityHistory(BaseModel):
    """Commodity history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int


# finscraper/models/money_flow.py
from pydantic import BaseModel
from datetime import datetime


class StockMoneyFlow(BaseModel):
    """Stock money flow data model."""
    
    stock_code: str
    stock_name: str
    date: datetime
    main_net_inflow: float
    main_net_inflow_percent: float
    super_large_net_inflow: float
    super_large_net_inflow_percent: float
    large_net_inflow: float
    large_net_inflow_percent: float
    medium_net_inflow: float
    medium_net_inflow_percent: float
    small_net_inflow: float
    small_net_inflow_percent: float


class SectorMoneyFlow(BaseModel):
    """Sector money flow data model."""
    
    sector_code: str
    sector_name: str
    date: datetime
    net_inflow: float
    net_inflow_percent: float
    lead_stock: str


# finscraper/models/news.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsItem(BaseModel):
    """News item data model."""
    
    title: str
    content: Optional[str] = None
    source: str
    publish_time: datetime
    url: Optional[str] = None
    importance: Optional[int] = None
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_models/ -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/models/ tests/test_models/
git commit -m "feat: add all data models (sector, commodity, money_flow, news)"
```

---

## Task 7: Implement AkShareClient

**Files:**
- Create: `finscraper/core/akshare_client.py`
- Create: `tests/test_core/test_akshare_client.py`

**Step 1: Write the failing test**

```python
# tests/test_core/test_akshare_client.py
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from finscraper.core.akshare_client import AkShareClient


def test_get_index_spot():
    mock_data = pd.DataFrame({
        "代码": ["000001", "399001"],
        "名称": ["上证指数", "深证成指"],
        "最新价": [3000.0, 10000.0],
        "涨跌幅": [0.5, 0.3]
    })
    
    with patch("akshare.index_zh_a_spot_em", return_value=mock_data):
        client = AkShareClient()
        result = client.get_index_spot()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "代码" in result.columns


def test_get_index_history():
    mock_data = pd.DataFrame({
        "日期": ["2024-01-01", "2024-01-02"],
        "开盘": [2990.0, 3000.0],
        "收盘": [3000.0, 3010.0],
        "最高": [3010.0, 3020.0],
        "最低": [2980.0, 2990.0],
        "成交量": [1000000, 1100000]
    })
    
    with patch("akshare.index_zh_a_hist", return_value=mock_data):
        client = AkShareClient()
        result = client.get_index_history(
            symbol="000001",
            period="daily",
            start_date="20240101",
            end_date="20240102"
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2


def test_get_north_flow_daily():
    mock_data = pd.DataFrame({
        "日期": ["2024-01-01"],
        "沪股通净流入": [100000000.0],
        "深股通净流入": [80000000.0]
    })
    
    with patch("akshare.stock_em_hsgt_north_net_flow_in_em", return_value=mock_data):
        client = AkShareClient()
        result = client.get_north_flow_daily()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_core/test_akshare_client.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.core.akshare_client'"

**Step 3: Write minimal implementation**

```python
# finscraper/core/akshare_client.py
import pandas as pd
import akshare as ak
from finscraper.core.logger import get_logger
from finscraper.core.retry import retry_with_backoff
from finscraper.core.exceptions import NetworkError

logger = get_logger(__name__)


class AkShareClient:
    """AkShare API client with retry mechanism."""
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_index_spot(self) -> pd.DataFrame:
        """Get A-share index spot data."""
        try:
            logger.info("Fetching index spot data")
            return ak.index_zh_a_spot_em()
        except Exception as e:
            logger.error(f"Failed to fetch index spot data: {e}")
            raise NetworkError(f"Failed to fetch index spot data: {e}")
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_index_history(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = ""
    ) -> pd.DataFrame:
        """Get A-share index history data."""
        try:
            logger.info(f"Fetching index history for {symbol}")
            return ak.index_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            logger.error(f"Failed to fetch index history: {e}")
            raise NetworkError(f"Failed to fetch index history: {e}")
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_north_flow_daily(self) -> pd.DataFrame:
        """Get north-bound capital flow daily data."""
        try:
            logger.info("Fetching north flow daily data")
            return ak.stock_em_hsgt_north_net_flow_in_em(symbol="北向")
        except Exception as e:
            logger.error(f"Failed to fetch north flow data: {e}")
            raise NetworkError(f"Failed to fetch north flow data: {e}")
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_core/test_akshare_client.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/core/akshare_client.py tests/test_core/test_akshare_client.py
git commit -m "feat: add akshare client with retry mechanism"
```

---

## Task 8: Implement DataCleaner

**Files:**
- Create: `finscraper/core/data_cleaner.py`
- Create: `tests/test_core/test_data_cleaner.py`

**Step 1: Write the failing test**

```python
# tests/test_core/test_data_cleaner.py
import pytest
import pandas as pd
from finscraper.core.data_cleaner import DataCleaner


def test_clean_column_names():
    df = pd.DataFrame({
        "代码": ["000001"],
        "名称": ["上证指数"],
        "最新价": [3000.0]
    })
    
    cleaner = DataCleaner()
    result = cleaner.clean_column_names(df)
    
    assert "代码" in result.columns
    assert "名称" in result.columns


def test_clean_numeric_columns():
    df = pd.DataFrame({
        "价格": ["3000.50", "10000.00"],
        "涨跌幅": ["0.5%", "0.3%"]
    })
    
    cleaner = DataCleaner()
    result = cleaner.clean_numeric_columns(df, ["价格"])
    
    assert result["价格"].dtype == float
    assert result["价格"][0] == 3000.50


def test_clean_percentage_columns():
    df = pd.DataFrame({
        "涨跌幅": ["0.5%", "0.3%", "-0.2%"]
    })
    
    cleaner = DataCleaner()
    result = cleaner.clean_percentage_columns(df, ["涨跌幅"])
    
    assert result["涨跌幅"][0] == 0.5
    assert result["涨跌幅"][2] == -0.2


def test_fill_missing_values():
    df = pd.DataFrame({
        "价格": [3000.0, None, 3010.0],
        "成交量": [1000000, 1100000, None]
    })
    
    cleaner = DataCleaner()
    result = cleaner.fill_missing_values(df, method="ffill")
    
    assert result["价格"].isna().sum() == 0
    assert result["成交量"].isna().sum() == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_core/test_data_cleaner.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.core.data_cleaner'"

**Step 3: Write minimal implementation**

```python
# finscraper/core/data_cleaner.py
import pandas as pd
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """Data cleaning utilities."""
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        logger.debug(f"Cleaning column names: {df.columns.tolist()}")
        return df
    
    def clean_numeric_columns(
        self,
        df: pd.DataFrame,
        columns: list
    ) -> pd.DataFrame:
        """Convert columns to numeric type."""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                logger.debug(f"Converted column {col} to numeric")
        return df
    
    def clean_percentage_columns(
        self,
        df: pd.DataFrame,
        columns: list
    ) -> pd.DataFrame:
        """Convert percentage strings to float."""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace("%", "").astype(float)
                logger.debug(f"Converted column {col} from percentage to float")
        return df
    
    def fill_missing_values(
        self,
        df: pd.DataFrame,
        method: str = "ffill"
    ) -> pd.DataFrame:
        """Fill missing values using specified method."""
        df = df.copy()
        if method == "ffill":
            df = df.fillna(method="ffill")
        elif method == "bfill":
            df = df.fillna(method="bfill")
        elif method == "zero":
            df = df.fillna(0)
        
        logger.debug(f"Filled missing values using method: {method}")
        return df
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_core/test_data_cleaner.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/core/data_cleaner.py tests/test_core/test_data_cleaner.py
git commit -m "feat: add data cleaner utilities"
```

---

## Task 9: Implement Base Storage

**Files:**
- Create: `finscraper/storage/base.py`
- Create: `finscraper/storage/csv_storage.py`
- Create: `finscraper/storage/json_storage.py`
- Create: `finscraper/storage/parquet_storage.py`
- Create: `finscraper/storage/sqlite_storage.py`
- Create: `tests/test_storage/test_csv_storage.py`
- Create: `tests/test_storage/test_json_storage.py`
- Create: `tests/test_storage/test_parquet_storage.py`
- Create: `tests/test_storage/test_sqlite_storage.py`

**Step 1: Write the failing tests**

```python
# tests/test_storage/test_csv_storage.py
import pytest
import pandas as pd
from pathlib import Path
from finscraper.storage.csv_storage import CSVStorage


def test_csv_save_and_load(tmp_path):
    df = pd.DataFrame({
        "symbol": ["000001", "000002"],
        "price": [3000.0, 3010.0]
    })
    
    storage = CSVStorage()
    file_path = tmp_path / "test.csv"
    
    storage.save(df, str(file_path))
    assert file_path.exists()
    
    loaded = storage.load(str(file_path))
    assert len(loaded) == 2
    assert loaded["symbol"][0] == "000001"


# tests/test_storage/test_json_storage.py
from finscraper.storage.json_storage import JSONStorage


def test_json_save_and_load(tmp_path):
    df = pd.DataFrame({
        "symbol": ["000001", "000002"],
        "price": [3000.0, 3010.0]
    })
    
    storage = JSONStorage()
    file_path = tmp_path / "test.json"
    
    storage.save(df, str(file_path))
    assert file_path.exists()
    
    loaded = storage.load(str(file_path))
    assert len(loaded) == 2


# tests/test_storage/test_parquet_storage.py
from finscraper.storage.parquet_storage import ParquetStorage


def test_parquet_save_and_load(tmp_path):
    df = pd.DataFrame({
        "symbol": ["000001", "000002"],
        "price": [3000.0, 3010.0]
    })
    
    storage = ParquetStorage()
    file_path = tmp_path / "test.parquet"
    
    storage.save(df, str(file_path))
    assert file_path.exists()
    
    loaded = storage.load(str(file_path))
    assert len(loaded) == 2


# tests/test_storage/test_sqlite_storage.py
from finscraper.storage.sqlite_storage import SQLiteStorage


def test_sqlite_save_and_load(tmp_path):
    df = pd.DataFrame({
        "symbol": ["000001", "000002"],
        "price": [3000.0, 3010.0]
    })
    
    storage = SQLiteStorage()
    db_path = tmp_path / "test.db"
    
    storage.save(df, str(db_path), table_name="test_data")
    assert db_path.exists()
    
    loaded = storage.load(str(db_path), table_name="test_data")
    assert len(loaded) == 2
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_storage/ -v`
Expected: FAIL with multiple "ModuleNotFoundError"

**Step 3: Create test directory structure**

Run: `mkdir -p tests/test_storage`
Run: `touch tests/test_storage/__init__.py`

**Step 4: Write minimal implementations**

```python
# finscraper/storage/base.py
from abc import ABC, abstractmethod
import pandas as pd


class BaseStorage(ABC):
    """Base storage interface."""
    
    @abstractmethod
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save data to storage."""
        pass
    
    @abstractmethod
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load data from storage."""
        pass


# finscraper/storage/csv_storage.py
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class CSVStorage(BaseStorage):
    """CSV file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to CSV file."""
        data.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info(f"Saved data to CSV: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from CSV file."""
        df = pd.read_csv(path)
        logger.info(f"Loaded data from CSV: {path}")
        return df


# finscraper/storage/json_storage.py
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class JSONStorage(BaseStorage):
    """JSON file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to JSON file."""
        data.to_json(path, orient="records", force_ascii=False, indent=2)
        logger.info(f"Saved data to JSON: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from JSON file."""
        df = pd.read_json(path, orient="records")
        logger.info(f"Loaded data from JSON: {path}")
        return df


# finscraper/storage/parquet_storage.py
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class ParquetStorage(BaseStorage):
    """Parquet file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to Parquet file."""
        data.to_parquet(path, index=False)
        logger.info(f"Saved data to Parquet: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from Parquet file."""
        df = pd.read_parquet(path)
        logger.info(f"Loaded data from Parquet: {path}")
        return df


# finscraper/storage/sqlite_storage.py
import pandas as pd
import sqlite3
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class SQLiteStorage(BaseStorage):
    """SQLite database storage."""
    
    def save(
        self,
        data: pd.DataFrame,
        path: str,
        table_name: str = "data",
        **kwargs
    ) -> None:
        """Save DataFrame to SQLite database."""
        conn = sqlite3.connect(path)
        data.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        logger.info(f"Saved data to SQLite: {path}, table: {table_name}")
    
    def load(self, path: str, table_name: str = "data", **kwargs) -> pd.DataFrame:
        """Load DataFrame from SQLite database."""
        conn = sqlite3.connect(path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        logger.info(f"Loaded data from SQLite: {path}, table: {table_name}")
        return df
```

**Step 5: Run tests to verify they pass**

Run: `pytest tests/test_storage/ -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/storage/ tests/test_storage/
git commit -m "feat: add storage layer (CSV, JSON, Parquet, SQLite)"
```

---

## Task 10: Implement BaseFetcher

**Files:**
- Create: `finscraper/fetchers/base.py`
- Create: `tests/test_fetchers/test_base.py`

**Step 1: Write the failing test**

```python
# tests/test_fetchers/test_base.py
import pytest
from finscraper.fetchers.base import BaseFetcher


class MockFetcher(BaseFetcher):
    """Mock fetcher for testing."""
    
    def fetch(self):
        return {"data": "test"}
    
    def fetch_with_retry(self):
        return self._fetch_with_retry(self.fetch)


def test_base_fetcher_initialization():
    fetcher = MockFetcher(name="test_fetcher")
    assert fetcher.name == "test_fetcher"


def test_base_fetcher_has_logger():
    fetcher = MockFetcher(name="test_fetcher")
    assert fetcher.logger is not None


def test_base_fetcher_has_client():
    fetcher = MockFetcher(name="test_fetcher")
    assert fetcher.client is not None


def test_base_fetcher_has_cleaner():
    fetcher = MockFetcher(name="test_fetcher")
    assert fetcher.cleaner is not None


def test_fetch_with_retry():
    fetcher = MockFetcher(name="test_fetcher")
    result = fetcher.fetch_with_retry()
    assert result == {"data": "test"}
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_fetchers/test_base.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'finscraper.fetchers.base'"

**Step 3: Create test directory structure**

Run: `mkdir -p tests/test_fetchers`
Run: `touch tests/test_fetchers/__init__.py`

**Step 4: Write minimal implementation**

```python
# finscraper/fetchers/base.py
from abc import ABC, abstractmethod
from finscraper.core.logger import get_logger
from finscraper.core.akshare_client import AkShareClient
from finscraper.core.data_cleaner import DataCleaner


class BaseFetcher(ABC):
    """Base fetcher for all data types."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"finscraper.fetchers.{name}")
        self.client = AkShareClient()
        self.cleaner = DataCleaner()
    
    @abstractmethod
    def fetch(self):
        """Fetch data from source."""
        pass
    
    def _fetch_with_retry(self, fetch_func, *args, **kwargs):
        """Execute fetch function with retry mechanism."""
        try:
            self.logger.info(f"Fetching {self.name} data")
            result = fetch_func(*args, **kwargs)
            self.logger.info(f"Successfully fetched {self.name} data")
            return result
        except Exception as e:
            self.logger.error(f"Failed to fetch {self.name} data: {e}")
            raise
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_fetchers/test_base.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/fetchers/base.py tests/test_fetchers/
git commit -m "feat: add base fetcher class"
```

---

## Task 11: Run All Tests

**Step 1: Run full test suite**

Run: `pytest tests/ -v --cov=finscraper --cov-report=term-missing`
Expected: All tests pass with coverage report

**Step 2: Verify coverage**

Expected: Coverage > 80% for all modules

**Step 3: Commit if needed**

```bash
git add tests/
git commit -m "test: ensure all tests pass with >80% coverage"
```

---

## Task 12: Update Documentation

**Files:**
- Update: `README.md`

**Step 1: Add usage examples to README**

```markdown
# FinScraper

基于 akshare 的金融数据获取工具，支持 CLI 和 Python API。

## 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用

```bash
# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231
```

### Python API 使用

```python
from finscraper.fetchers.index import IndexFetcher
from finscraper.storage.csv_storage import CSVStorage

# 获取数据
fetcher = IndexFetcher()
data = fetcher.fetch_spot()

# 保存数据
storage = CSVStorage()
storage.save(data, "data/index/spot.csv")
```

## 开发

```bash
# 安装开发依赖
pip install -e .[dev]

# 运行测试
pytest

# 代码格式化
black .
isort .
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with usage examples"
```

---

## Summary

This plan implements the core framework for FinScraper:

1. ✅ Logging system with loguru
2. ✅ Custom exception classes
3. ✅ Retry mechanism with exponential backoff
4. ✅ All data models (index, north_flow, sector, commodity, money_flow, news)
5. ✅ AkShare client with retry
6. ✅ Data cleaner utilities
7. ✅ Storage layer (CSV, JSON, Parquet, SQLite)
8. ✅ Base fetcher class
9. ✅ Comprehensive tests with >80% coverage
10. ✅ Updated documentation

**Next Steps:** Proceed to Phase 3 (CLI Framework) after completing this plan.
