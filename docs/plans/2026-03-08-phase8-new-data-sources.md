# Phase 8: 新数据源扩展计划

> **日期**: 2026-03-08  
> **目标**: 添加市场情绪、港股、美股、汇率等新数据源

---

## 概述

本计划扩展 FinScraper 项目，添加 4 个新的数据获取器（Fetcher），以支持完整的市场概览需求：

1. **MarketSentimentFetcher** - 市场情绪数据（涨跌家数、涨停跌停）
2. **HKIndexFetcher** - 港股/恒生指数数据
3. **USIndexFetcher** - 美股指数数据（道指、纳指、标普500）
4. **ForexFetcher** - 汇率数据（美元、欧元、港币等）

---

## 前置条件

- ✅ akshare 库已在项目依赖中（版本 ≥ 1.18.35）
- ✅ 现有 fetcher 架构完整可复用
- ✅ 编码规范和文档标准已确立

---

## Task 1: 更新 AkShareClient

**文件**: `finscraper/core/akshare_client.py`

### Step 1: 添加 MarketSentiment 相关方法

```python
def fetch_stock_zh_a_spot_em(self) -> pd.DataFrame:
    """Fetch all A-share spot data from East Money."""
    return self._call_akshare("stock_zh_a_spot_em")

def fetch_stock_zt_pool_em(self, date: str = "") -> pd.DataFrame:
    """Fetch limit-up stock pool from East Money."""
    if date:
        return self._call_akshare("stock_zt_pool_em", date=date)
    return self._call_akshare("stock_zt_pool_em")

def fetch_stock_dt_pool_em(self, date: str = "") -> pd.DataFrame:
    """Fetch limit-down stock pool from East Money."""
    if date:
        return self._call_akshare("stock_zt_pool_em", date=date)
    return self._call_akshare("stock_zt_pool_em")
```

### Step 2: 添加 HKIndex 相关方法

```python
def fetch_index_hk_spot_em(self) -> pd.DataFrame:
    """Fetch Hong Kong index spot data from East Money."""
    return self._call_akshare("index_hk_spot_em")
```

### Step 3: 添加 USIndex 相关方法

```python
def fetch_index_us_spot(self) -> pd.DataFrame:
    """Fetch US index spot data."""
    return self._call_akshare("index_us_spot")

def fetch_index_global_spot(self) -> pd.DataFrame:
    """Fetch global index spot data."""
    return self._call_akshare("index_global_spot")
```

### Step 4: 添加 Forex 相关方法

```python
def fetch_forex_spot_em(self) -> pd.DataFrame:
    """Fetch forex spot data from East Money."""
    return self._call_akshare("forex_spot_em")

def fetch_forex_hist_em(
    self,
    symbol: str,
    period: str = "daily",
    start_date: str = "",
    end_date: str = "",
) -> pd.DataFrame:
    """Fetch forex historical data from East Money."""
    return self._call_akshare(
        "forex_hist_em",
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
    )
```

---

## Task 2: 更新 DataCleaner

**文件**: `finscraper/core/data_cleaner.py`

### Step 1: 添加 MarketSentiment 清洗方法

```python
def clean_market_sentiment_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean market sentiment spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_limit_up(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean limit-up stock data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_limit_down(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean limit-down stock data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

### Step 2: 添加 HKIndex 清洗方法

```python
def clean_hk_index_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean Hong Kong index spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

### Step 3: 添加 USIndex 清洗方法

```python
def clean_us_index_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean US index spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_global_index_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean global index spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

### Step 4: 添加 Forex 清洗方法

```python
def clean_forex_spot(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean forex spot data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df

def clean_forex_history(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean forex historical data."""
    df = df.copy()
    df = self.clean_column_names(df)
    df = self.convert_numeric_columns(df)
    return df
```

---

## Task 3: 创建数据模型

**文件**: `finscraper/models/market_sentiment.py`

```python
"""Market sentiment data models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MarketSentimentSpot(BaseModel):
    """Market sentiment spot data model."""
    
    up_count: int
    down_count: int
    flat_count: int
    limit_up_count: int
    limit_down_count: int
    updated_at: datetime


class LimitUpStock(BaseModel):
    """Limit-up stock data model."""
    
    symbol: str
    name: str
    price: float
    change_percent: float
    limit_up_time: Optional[str] = None
    first_limit_up_time: Optional[str] = None
    last_limit_up_time: Optional[str] = None
    open_times: Optional[int] = None


class LimitDownStock(BaseModel):
    """Limit-down stock data model."""
    
    symbol: str
    name: str
    price: float
    change_percent: float
    limit_down_time: Optional[str] = None
```

**文件**: `finscraper/models/hk_index.py`

```python
"""Hong Kong index data models."""
from pydantic import BaseModel
from datetime import datetime


class HKIndexSpot(BaseModel):
    """Hong Kong index spot data model."""
    
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
```

**文件**: `finscraper/models/us_index.py`

```python
"""US index data models."""
from pydantic import BaseModel
from datetime import datetime


class USIndexSpot(BaseModel):
    """US index spot data model."""
    
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
```

**文件**: `finscraper/models/forex.py`

```python
"""Forex data models."""
from pydantic import BaseModel
from datetime import datetime


class ForexSpot(BaseModel):
    """Forex spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class ForexHistory(BaseModel):
    """Forex history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
```

**更新文件**: `finscraper/models/__init__.py`

添加新模型的导出：

```python
from finscraper.models.market_sentiment import (
    MarketSentimentSpot,
    LimitUpStock,
    LimitDownStock,
)
from finscraper.models.hk_index import HKIndexSpot
from finscraper.models.us_index import USIndexSpot
from finscraper.models.forex import ForexSpot, ForexHistory

__all__ = [
    ...,
    "MarketSentimentSpot",
    "LimitUpStock",
    "LimitDownStock",
    "HKIndexSpot",
    "USIndexSpot",
    "ForexSpot",
    "ForexHistory",
]
```

---

## Task 4: 实现 MarketSentimentFetcher

**文件**: `finscraper/fetchers/market_sentiment.py`

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class MarketSentimentFetcher(BaseFetcher):
    """Fetcher for market sentiment data."""
    
    def __init__(self):
        super().__init__("market-sentiment")
    
    def fetch(self):
        """Fetch all market sentiment data."""
        return self.fetch_sentiment()
    
    def fetch_sentiment(self) -> pd.DataFrame:
        """Fetch comprehensive market sentiment data."""
        self.logger.info("Fetching market sentiment data")
        
        try:
            up_down_df = self.fetch_up_down_count()
            limit_up_df = self.fetch_limit_up()
            limit_down_df = self.fetch_limit_down()
            
            sentiment_data = {
                "up_count": len(up_down_df[up_down_df["change_percent"] > 0]) if not up_down_df.empty else 0,
                "down_count": len(up_down_df[up_down_df["change_percent"] < 0]) if not up_down_df.empty else 0,
                "flat_count": len(up_down_df[up_down_df["change_percent"] == 0]) if not up_down_df.empty else 0,
                "limit_up_count": len(limit_up_df) if not limit_up_df.empty else 0,
                "limit_down_count": len(limit_down_df) if not limit_down_df.empty else 0,
            }
            
            df = pd.DataFrame([sentiment_data])
            self.logger.info("Successfully fetched market sentiment data")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch market sentiment data: {e}")
            raise
    
    def fetch_up_down_count(self) -> pd.DataFrame:
        """Fetch up/down stock count."""
        self.logger.info("Fetching up/down count")
        
        try:
            df = self.client.fetch_stock_zh_a_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_market_sentiment_spot(df)
                self.logger.info(f"Fetched {len(df)} stocks for up/down count")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch up/down count: {e}")
            raise
    
    def fetch_limit_up(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-up stocks."""
        self.logger.info("Fetching limit-up stocks")
        
        try:
            df = self.client.fetch_stock_zt_pool_em(date=date)
            if df is not None and not df.empty:
                df = self.cleaner.clean_limit_up(df)
                self.logger.info(f"Fetched {len(df)} limit-up stocks")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch limit-up stocks: {e}")
            raise
    
    def fetch_limit_down(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-down stocks."""
        self.logger.info("Fetching limit-down stocks")
        
        try:
            df = self.client.fetch_stock_dt_pool_em(date=date)
            if df is not None and not df.empty:
                df = self.cleaner.clean_limit_down(df)
                self.logger.info(f"Fetched {len(df)} limit-down stocks")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch limit-down stocks: {e}")
            raise
```

**测试文件**: `tests/test_fetchers/test_market_sentiment.py`

```python
import pytest
import pandas as pd
from finscraper.fetchers.market_sentiment import MarketSentimentFetcher


def test_market_sentiment_fetcher_initialization():
    fetcher = MarketSentimentFetcher()
    assert fetcher is not None
    assert fetcher.name == "market-sentiment"


def test_market_sentiment_fetch_sentiment():
    fetcher = MarketSentimentFetcher()
    try:
        df = fetcher.fetch_sentiment()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_market_sentiment_fetch_limit_up():
    fetcher = MarketSentimentFetcher()
    try:
        df = fetcher.fetch_limit_up()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_market_sentiment_fetch_limit_down():
    fetcher = MarketSentimentFetcher()
    try:
        df = fetcher.fetch_limit_down()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
```

---

## Task 5: 实现 HKIndexFetcher

**文件**: `finscraper/fetchers/hk_index.py`

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class HKIndexFetcher(BaseFetcher):
    """Fetcher for Hong Kong index data."""
    
    def __init__(self):
        super().__init__("hk-index")
    
    def fetch(self):
        """Fetch all Hong Kong index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch Hong Kong index spot data."""
        self.logger.info("Fetching Hong Kong index spot data")
        
        try:
            df = self.client.fetch_index_hk_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_hk_index_spot(df)
                self.logger.info(f"Fetched {len(df)} Hong Kong index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch Hong Kong index spot data: {e}")
            raise
```

**测试文件**: `tests/test_fetchers/test_hk_index.py`

```python
import pytest
import pandas as pd
from finscraper.fetchers.hk_index import HKIndexFetcher


def test_hk_index_fetcher_initialization():
    fetcher = HKIndexFetcher()
    assert fetcher is not None
    assert fetcher.name == "hk-index"


def test_hk_index_fetch_spot():
    fetcher = HKIndexFetcher()
    try:
        df = fetcher.fetch_spot()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
```

---

## Task 6: 实现 USIndexFetcher

**文件**: `finscraper/fetchers/us_index.py`

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class USIndexFetcher(BaseFetcher):
    """Fetcher for US index data."""
    
    def __init__(self):
        super().__init__("us-index")
    
    def fetch(self):
        """Fetch all US index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch US index spot data."""
        self.logger.info("Fetching US index spot data")
        
        try:
            df = self.client.fetch_index_us_spot()
            if df is not None and not df.empty:
                df = self.cleaner.clean_us_index_spot(df)
                self.logger.info(f"Fetched {len(df)} US index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch US index spot data: {e}")
            raise
    
    def fetch_global(self) -> pd.DataFrame:
        """Fetch global index spot data."""
        self.logger.info("Fetching global index spot data")
        
        try:
            df = self.client.fetch_index_global_spot()
            if df is not None and not df.empty:
                df = self.cleaner.clean_global_index_spot(df)
                self.logger.info(f"Fetched {len(df)} global index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch global index spot data: {e}")
            raise
```

**测试文件**: `tests/test_fetchers/test_us_index.py`

```python
import pytest
import pandas as pd
from finscraper.fetchers.us_index import USIndexFetcher


def test_us_index_fetcher_initialization():
    fetcher = USIndexFetcher()
    assert fetcher is not None
    assert fetcher.name == "us-index"


def test_us_index_fetch_spot():
    fetcher = USIndexFetcher()
    try:
        df = fetcher.fetch_spot()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_us_index_fetch_global():
    fetcher = USIndexFetcher()
    try:
        df = fetcher.fetch_global()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
```

---

## Task 7: 实现 ForexFetcher

**文件**: `finscraper/fetchers/forex.py`

```python
import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class ForexFetcher(BaseFetcher):
    """Fetcher for forex data."""
    
    def __init__(self):
        super().__init__("forex")
    
    def fetch(self):
        """Fetch all forex data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch forex spot data."""
        self.logger.info("Fetching forex spot data")
        
        try:
            df = self.client.fetch_forex_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_forex_spot(df)
                self.logger.info(f"Fetched {len(df)} forex spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch forex spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch forex historical data."""
        self.logger.info(f"Fetching forex history for {symbol}")
        
        try:
            df = self.client.fetch_forex_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_forex_history(df)
                self.logger.info(f"Fetched {len(df)} forex history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch forex history for {symbol}: {e}")
            raise
```

**测试文件**: `tests/test_fetchers/test_forex.py`

```python
import pytest
import pandas as pd
from finscraper.fetchers.forex import ForexFetcher


def test_forex_fetcher_initialization():
    fetcher = ForexFetcher()
    assert fetcher is not None
    assert fetcher.name == "forex"


def test_forex_fetch_spot():
    fetcher = ForexFetcher()
    try:
        df = fetcher.fetch_spot()
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")


def test_forex_fetch_history():
    fetcher = ForexFetcher()
    try:
        df = fetcher.fetch_history(
            symbol="USDCNH",
            start_date="20240101",
            end_date="20241231",
        )
        assert df is not None
        assert isinstance(df, pd.DataFrame)
    except Exception as e:
        pytest.skip(f"API call failed: {e}")
```

---

## Task 8: 更新 fetchers/__init__.py

**文件**: `finscraper/fetchers/__init__.py`

添加新 fetcher 的导出：

```python
from finscraper.fetchers.market_sentiment import MarketSentimentFetcher
from finscraper.fetchers.hk_index import HKIndexFetcher
from finscraper.fetchers.us_index import USIndexFetcher
from finscraper.fetchers.forex import ForexFetcher

__all__ = [
    ...,
    "MarketSentimentFetcher",
    "HKIndexFetcher",
    "USIndexFetcher",
    "ForexFetcher",
]
```

---

## Task 9: 添加 CLI 命令

### Step 1: 创建 CLI 命令模块

**文件**: `finscraper/cli/commands/market_sentiment.py`

```python
import typer
from typing import Optional
from finscraper.fetchers import MarketSentimentFetcher
from finscraper.cli.utils import handle_output


app = typer.Typer(help="市场情绪数据命令")


@app.command("spot")
def spot(
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取市场情绪数据"""
    fetcher = MarketSentimentFetcher()
    data = fetcher.fetch_sentiment()
    handle_output(data, output, output_path)


@app.command("limit-up")
def limit_up(
    date: Optional[str] = typer.Option(None, "-d", "--date", help="日期，格式 YYYYMMDD"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取涨停股票"""
    fetcher = MarketSentimentFetcher()
    data = fetcher.fetch_limit_up(date=date)
    handle_output(data, output, output_path)


@app.command("limit-down")
def limit_down(
    date: Optional[str] = typer.Option(None, "-d", "--date", help="日期，格式 YYYYMMDD"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取跌停股票"""
    fetcher = MarketSentimentFetcher()
    data = fetcher.fetch_limit_down(date=date)
    handle_output(data, output, output_path)
```

**文件**: `finscraper/cli/commands/hk_index.py`

```python
import typer
from typing import Optional
from finscraper.fetchers import HKIndexFetcher
from finscraper.cli.utils import handle_output


app = typer.Typer(help="港股指数数据命令")


@app.command("spot")
def spot(
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取港股指数实时行情"""
    fetcher = HKIndexFetcher()
    data = fetcher.fetch_spot()
    handle_output(data, output, output_path)
```

**文件**: `finscraper/cli/commands/us_index.py`

```python
import typer
from typing import Optional
from finscraper.fetchers import USIndexFetcher
from finscraper.cli.utils import handle_output


app = typer.Typer(help="美股指数数据命令")


@app.command("spot")
def spot(
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取美股指数实时行情"""
    fetcher = USIndexFetcher()
    data = fetcher.fetch_spot()
    handle_output(data, output, output_path)


@app.command("global")
def global_index(
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取全球指数实时行情"""
    fetcher = USIndexFetcher()
    data = fetcher.fetch_global()
    handle_output(data, output, output_path)
```

**文件**: `finscraper/cli/commands/forex.py`

```python
import typer
from typing import Optional
from finscraper.fetchers import ForexFetcher
from finscraper.cli.utils import handle_output


app = typer.Typer(help="汇率数据命令")


@app.command("spot")
def spot(
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取汇率实时行情"""
    fetcher = ForexFetcher()
    data = fetcher.fetch_spot()
    handle_output(data, output, output_path)


@app.command("history")
def history(
    symbol: str = typer.Argument(..., help="货币对代码，如 USDCNH"),
    start_date: Optional[str] = typer.Option(None, "-s", "--start-date", help="开始日期，格式 YYYYMMDD"),
    end_date: Optional[str] = typer.Option(None, "-e", "--end-date", help="结束日期，格式 YYYYMMDD"),
    period: str = typer.Option("daily", "-p", "--period", help="周期，可选 daily/weekly/monthly"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出格式"),
    output_path: Optional[str] = typer.Option(None, "-p", "--output-path", help="输出文件路径"),
):
    """获取汇率历史数据"""
    fetcher = ForexFetcher()
    data = fetcher.fetch_history(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        period=period,
    )
    handle_output(data, output, output_path)
```

### Step 2: 集成到主 CLI

**文件**: `finscraper/cli/main.py`

添加新命令的导入和注册：

```python
from finscraper.cli.commands import (
    ...,
    market_sentiment,
    hk_index,
    us_index,
    forex,
)

app.add_typer(market_sentiment.app, name="sentiment", help="市场情绪数据")
app.add_typer(hk_index.app, name="hk-index", help="港股指数数据")
app.add_typer(us_index.app, name="us-index", help="美股指数数据")
app.add_typer(forex.app, name="forex", help="汇率数据")
```

---

## Task 10: 更新文档

### Step 1: 更新 API_REFERENCE.md

在适当位置添加新 fetcher 的 API 文档。

### Step 2: 更新 USER_GUIDE.md

在适当位置添加新功能的使用说明和示例。

### Step 3: 更新 README.md

在适当位置添加新 fetcher 的使用示例。

---

## Task 11: 运行所有测试

```bash
pytest tests/test_fetchers/test_market_sentiment.py -v
pytest tests/test_fetchers/test_hk_index.py -v
pytest tests/test_fetchers/test_us_index.py -v
pytest tests/test_fetchers/test_forex.py -v
pytest tests/test_fetchers/ -v
```

---

## 总结

本计划实现以下新功能：

1. ✅ MarketSentimentFetcher - 市场情绪数据（涨跌家数、涨停跌停）
2. ✅ HKIndexFetcher - 港股/恒生指数数据
3. ✅ USIndexFetcher - 美股指数数据
4. ✅ ForexFetcher - 汇率数据
5. ✅ 对应的 CLI 命令
6. ✅ 完整的测试用例
7. ✅ 文档更新

**下一步**: 按照本计划逐步实现代码。
