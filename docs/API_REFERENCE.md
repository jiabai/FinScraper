# API 参考文档

本文档详细介绍 FinScraper 的 Python API。

---

## 目录

1. [概述](#概述)
2. [数据获取器 (Fetchers)](#数据获取器-fetchers)
3. [存储模块 (Storage)](#存储模块-storage)
4. [数据筛选器 (Filters)](#数据筛选器-filters)
5. [配置模块 (Config)](#配置模块-config)
6. [核心模块 (Core)](#核心模块-core)
7. [数据模型 (Models)](#数据模型-models)

---

## 概述

FinScraper 提供简洁的 Python API，支持：

- **类型安全**: 完整的类型注解
- **统一接口**: 所有 Fetcher 遵循相同的接口规范
- **灵活存储**: 支持多种存储格式
- **错误处理**: 完善的异常体系

### 快速开始

```python
from finscraper.fetchers import IndexFetcher

# 创建获取器
fetcher = IndexFetcher()

# 获取数据
data = fetcher.fetch_spot()
print(data.head())
```

---

## 数据获取器 (Fetchers)

所有数据获取器都继承自 `BaseFetcher`，提供统一的基础功能。

### BaseFetcher

基类，定义了所有 Fetcher 的通用接口。

```python
from finscraper.fetchers.base import BaseFetcher
```

#### 属性

| 属性 | 类型 | 说明 |
|-----|------|------|
| `name` | `str` | Fetcher 名称 |
| `logger` | `Logger` | 日志记录器 |

#### 方法

| 方法 | 返回类型 | 说明 |
|-----|---------|------|
| `__init__(name: str)` | - | 初始化 Fetcher |

---

### IndexFetcher

A 股指数数据获取器。

```python
from finscraper.fetchers import IndexFetcher

fetcher = IndexFetcher()
```

#### 方法

##### fetch_spot

获取指数实时行情数据。

```python
def fetch_spot(
    symbols: Optional[list[str]] = None,
) -> pd.DataFrame:
    """获取指数实时行情。

    Args:
        symbols: 指数代码列表，如 ['sh000001', 'sz399001']。
            如果为 None，则获取所有指数。

    Returns:
        DataFrame 包含以下列：
            - symbol: 指数代码
            - name: 指数名称
            - price: 最新价
            - change: 涨跌额
            - change_percent: 涨跌幅
            - volume: 成交量
            - amount: 成交额
            - updated_at: 更新时间
    """
```

**示例**:

```python
# 获取所有指数
data = fetcher.fetch_spot()

# 获取指定指数
data = fetcher.fetch_spot(['sh000001', 'sz399001'])
```

##### fetch_history

获取指数历史数据。

```python
def fetch_history(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = "daily",
) -> pd.DataFrame:
    """获取指数历史数据。

    Args:
        symbol: 指数代码（不含前缀），如 '000001'。
        start_date: 开始日期，格式 YYYYMMDD。
        end_date: 结束日期，格式 YYYYMMDD。
        period: 周期，可选 'daily', 'weekly', 'monthly'。

    Returns:
        DataFrame 包含以下列：
            - date: 日期
            - open: 开盘价
            - high: 最高价
            - low: 最低价
            - close: 收盘价
            - volume: 成交量
            - amount: 成交额
    """
```

**示例**:

```python
# 获取上证指数历史数据
data = fetcher.fetch_history('000001')

# 指定日期范围
data = fetcher.fetch_history(
    symbol='000001',
    start_date='20240101',
    end_date='20241231',
)

# 获取周线数据
data = fetcher.fetch_history('000001', period='weekly')
```

##### fetch_list

获取可用指数列表。

```python
def fetch_list() -> pd.DataFrame:
    """获取所有可用指数列表。

    Returns:
        DataFrame 包含指数代码和名称。
    """
```

---

### NorthFlowFetcher

北向资金数据获取器。

```python
from finscraper.fetchers import NorthFlowFetcher

fetcher = NorthFlowFetcher()
```

#### 方法

##### fetch_daily

获取北向资金日数据。

```python
def fetch_daily() -> pd.DataFrame:
    """获取北向资金日数据。

    Returns:
        DataFrame 包含以下列：
            - date: 日期
            - sh_inflow: 沪股通流入（亿元）
            - sh_outflow: 沪股通流出（亿元）
            - sz_inflow: 深股通流入（亿元）
            - sz_outflow: 深股通流出（亿元）
            - north_net_inflow: 北向净流入（亿元）
            - balance: 当日余额（亿元）
    """
```

**示例**:

```python
data = fetcher.fetch_daily()
print(data[['date', 'north_net_inflow']].head())
```

##### fetch_intraday

获取北向资金日内数据。

```python
def fetch_intraday() -> pd.DataFrame:
    """获取北向资金日内分时数据。

    Returns:
        DataFrame 包含以下列：
            - time: 时间
            - sh_inflow: 沪股通流入
            - sz_inflow: 深股通流入
            - north_inflow: 北向资金流入
    """
```

---

### SectorFetcher

板块数据获取器。

```python
from finscraper.fetchers import SectorFetcher

fetcher = SectorFetcher()
```

#### 方法

##### fetch_list

获取板块列表。

```python
def fetch_list() -> pd.DataFrame:
    """获取所有板块列表。

    Returns:
        DataFrame 包含板块代码和名称。
    """
```

##### fetch_spot

获取板块实时行情。

```python
def fetch_spot() -> pd.DataFrame:
    """获取板块实时行情。

    Returns:
        DataFrame 包含以下列：
            - symbol: 板块代码
            - name: 板块名称
            - change_percent: 涨跌幅
            - change: 涨跌额
            - leading_stock: 领涨股
            - leading_percent: 领涨股涨幅
            - volume: 成交量
            - amount: 成交额
            - turnover_rate: 换手率
    """
```

##### fetch_stocks

获取板块成分股。

```python
def fetch_stocks(sector_code: str) -> pd.DataFrame:
    """获取板块成分股。

    Args:
        sector_code: 板块代码。

    Returns:
        DataFrame 包含成分股信息。
    """
```

**示例**:

```python
# 获取板块列表
sectors = fetcher.fetch_list()

# 获取板块行情
spot = fetcher.fetch_spot()

# 获取成分股
stocks = fetcher.fetch_stocks('BK0428')
```

---

### CommodityFetcher

大宗商品数据获取器。

```python
from finscraper.fetchers import CommodityFetcher

fetcher = CommodityFetcher()
```

#### 方法

##### fetch_list

获取商品列表。

```python
def fetch_list() -> pd.DataFrame:
    """获取所有可用商品列表。

    Returns:
        DataFrame 包含商品代码和名称。
    """
```

##### fetch_spot

获取商品实时行情。

```python
def fetch_spot() -> pd.DataFrame:
    """获取商品实时行情。

    Returns:
        DataFrame 包含以下列：
            - symbol: 商品代码
            - name: 商品名称
            - price: 最新价
            - change: 涨跌额
            - change_percent: 涨跌幅
            - volume: 成交量
            - open: 开盘价
            - high: 最高价
            - low: 最低价
            - previous_close: 昨收价
    """
```

##### fetch_history

获取商品历史数据。

```python
def fetch_history(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = "daily",
) -> pd.DataFrame:
    """获取商品历史数据。

    Args:
        symbol: 商品代码，如 'AU0'（黄金）。
        start_date: 开始日期，格式 YYYYMMDD。
        end_date: 结束日期，格式 YYYYMMDD。
        period: 周期，可选 'daily', 'weekly', 'monthly'。

    Returns:
        DataFrame 包含历史价格数据。
    """
```

**常用商品代码**:

| 代码 | 商品 |
|-----|------|
| AU0 | 黄金 |
| AG0 | 白银 |
| CU0 | 铜 |
| AL0 | 铝 |
| ZN0 | 锌 |
| RB0 | 螺纹钢 |
| SC0 | 原油 |

---

### MoneyFlowFetcher

资金流向数据获取器。

```python
from finscraper.fetchers import MoneyFlowFetcher

fetcher = MoneyFlowFetcher()
```

#### 方法

##### fetch_stock

获取个股资金流向。

```python
def fetch_stock() -> pd.DataFrame:
    """获取个股资金流向排名。

    Returns:
        DataFrame 包含以下列：
            - symbol: 股票代码
            - name: 股票名称
            - main_net_inflow: 主力净流入
            - super_large_inflow: 超大单流入
            - large_inflow: 大单流入
            - medium_inflow: 中单流入
            - small_inflow: 小单流入
            - net_percent: 净占比
    """
```

##### fetch_sector

获取板块资金流向。

```python
def fetch_sector() -> pd.DataFrame:
    """获取板块资金流向。

    Returns:
        DataFrame 包含板块资金流向数据。
    """
```

##### fetch_market

获取市场资金流向。

```python
def fetch_market() -> pd.DataFrame:
    """获取两市资金流向。

    Returns:
        DataFrame 包含市场整体资金流向数据。
    """
```

---

### NewsFetcher

新闻数据获取器。

```python
from finscraper.fetchers import NewsFetcher

fetcher = NewsFetcher()
```

#### 方法

##### fetch_global

获取全球财经新闻。

```python
def fetch_global() -> pd.DataFrame:
    """获取全球财经新闻。

    Returns:
        DataFrame 包含以下列：
            - title: 新闻标题
            - content: 新闻内容
            - time: 发布时间
            - source: 来源
            - url: 链接
    """
```

##### fetch_alert

获取 A 股公告快讯。

```python
def fetch_alert() -> pd.DataFrame:
    """获取 A 股公告快讯。

    Returns:
        DataFrame 包含公告信息。
    """
```

##### fetch_stock

获取个股相关新闻。

```python
def fetch_stock(symbol: str) -> pd.DataFrame:
    """获取个股相关新闻。

    Args:
        symbol: 股票代码。

    Returns:
        DataFrame 包含个股相关新闻。
    """
```

---

## 存储模块 (Storage)

存储模块提供多种格式的数据存储支持。

### BaseStorage

存储模块基类。

```python
from finscraper.storage.base import BaseStorage
```

#### 方法

```python
def save(self, data: pd.DataFrame, path: str) -> None:
    """保存数据到文件。

    Args:
        data: 要保存的数据。
        path: 文件路径。
    """

def load(self, path: str) -> pd.DataFrame:
    """从文件加载数据。

    Args:
        path: 文件路径。

    Returns:
        加载的数据。
    """
```

---

### CSVStorage

CSV 格式存储。

```python
from finscraper.storage import CSVStorage

storage = CSVStorage()

# 保存数据
storage.save(data, "data/index.csv")

# 加载数据
data = storage.load("data/index.csv")
```

---

### JSONStorage

JSON 格式存储。

```python
from finscraper.storage import JSONStorage

storage = JSONStorage()

# 保存数据
storage.save(data, "data/index.json")

# 加载数据
data = storage.load("data/index.json")
```

---

### ParquetStorage

Parquet 格式存储（适合大数据）。

```python
from finscraper.storage import ParquetStorage

storage = ParquetStorage()

# 保存数据
storage.save(data, "data/index.parquet")

# 加载数据
data = storage.load("data/index.parquet")
```

---

### SQLiteStorage

SQLite 数据库存储。

```python
from finscraper.storage import SQLiteStorage

storage = SQLiteStorage()

# 保存数据到表
storage.save(data, "data/finance.db", table_name="index_spot")

# 加载数据
data = storage.load("data/finance.db", table_name="index_spot")
```

---

### get_storage 工厂函数

根据格式自动选择存储实现。

```python
from finscraper.storage import get_storage

# 获取 CSV 存储
storage = get_storage("csv")

# 获取 JSON 存储
storage = get_storage("json")

# 获取 Parquet 存储
storage = get_storage("parquet")

# 获取 SQLite 存储
storage = get_storage("sqlite")
```

---

## 数据筛选器 (Filters)

### TopicFilter

专题新闻筛选器。

```python
from finscraper.filters import TopicFilter

filter = TopicFilter()
```

#### 方法

##### list_topics

列出所有可用专题。

```python
def list_topics() -> list[str]:
    """列出所有可用专题。

    Returns:
        专题名称列表。
    """
```

##### filter_by_topic

按专题筛选新闻。

```python
def filter_by_topic(
    df: pd.DataFrame,
    topic: str,
    match_content: bool = False,
) -> pd.DataFrame:
    """按专题筛选新闻。

    Args:
        df: 新闻数据 DataFrame。
        topic: 专题名称。
        match_content: 是否同时匹配新闻内容。

    Returns:
        筛选后的 DataFrame。
    """
```

##### get_topic_urls

获取专题新闻 URL 列表。

```python
def get_topic_urls(
    df: pd.DataFrame,
    topic: str,
) -> list[str]:
    """获取专题新闻 URL 列表。

    Args:
        df: 新闻数据 DataFrame。
        topic: 专题名称。

    Returns:
        URL 列表。
    """
```

**示例**:

```python
import akshare as ak
from finscraper.filters import TopicFilter

# 获取新闻数据
df = ak.stock_info_global_em()

# 创建筛选器
filter = TopicFilter()

# 列出专题
topics = filter.list_topics()
print(topics)

# 筛选专题新闻
filtered = filter.filter_by_topic(df, "中东地缘")

# 获取 URL 列表
urls = filter.get_topic_urls(df, "中东地缘")
```

---

## 配置模块 (Config)

### Settings

配置管理类。

```python
from finscraper.config import Settings

# 使用默认配置
settings = Settings()

# 自定义配置
settings = Settings(
    request_timeout=60,
    max_retries=5,
    log_level="DEBUG",
)
```

#### 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|-------|------|-------|------|
| `request_timeout` | `int` | `30` | 请求超时时间（秒） |
| `max_retries` | `int` | `3` | 最大重试次数 |
| `user_agent` | `str` | `Mozilla/5.0...` | 请求 User-Agent |
| `data_dir` | `str` | `data` | 数据存储目录 |
| `log_level` | `str` | `INFO` | 日志级别 |
| `log_file` | `str` | `logs/finscraper.log` | 日志文件路径 |

#### 环境变量配置

所有配置项都可以通过环境变量设置，前缀为 `FINSCRAPER_`：

```bash
export FINSCRAPER_REQUEST_TIMEOUT=60
export FINSCRAPER_MAX_RETRIES=5
export FINSCRAPER_LOG_LEVEL=DEBUG
```

---

## 核心模块 (Core)

### AkShareClient

AkShare API 封装客户端。

```python
from finscraper.core import AkShareClient

client = AkShareClient()
```

#### 方法

| 方法 | 说明 |
|-----|------|
| `get_index_zh_a_spot_sina()` | 获取 A 股指数实时行情 |
| `get_stock_zh_index_daily()` | 获取指数历史数据 |
| `stock_hsgt_fund_flow_summary_em()` | 获取北向资金数据 |
| `stock_board_concept_name_em()` | 获取板块列表 |
| `futures_sina_main_sina()` | 获取商品数据 |

---

### DataCleaner

数据清洗工具。

```python
from finscraper.core import DataCleaner

cleaner = DataCleaner()

# 清洗数据
clean_data = cleaner.clean(raw_data)
```

#### 方法

| 方法 | 说明 |
|-----|------|
| `clean(df)` | 清洗数据 |
| `rename_columns(df, mapping)` | 重命名列 |
| `convert_types(df, type_map)` | 转换数据类型 |
| `handle_missing(df)` | 处理缺失值 |

---

### 异常类

```python
from finscraper.core.exceptions import (
    FinScraperError,
    NetworkError,
    DataParseError,
    ValidationError,
    StorageError,
)
```

| 异常 | 说明 |
|-----|------|
| `FinScraperError` | 基础异常类 |
| `NetworkError` | 网络请求错误 |
| `DataParseError` | 数据解析错误 |
| `ValidationError` | 数据验证错误 |
| `StorageError` | 存储操作错误 |

---

## 数据模型 (Models)

所有数据模型使用 Pydantic 定义，确保类型安全。

### IndexInfo

指数信息模型。

```python
from finscraper.models import IndexInfo

info = IndexInfo(
    symbol="sh000001",
    name="上证指数",
    price=3050.23,
    change=12.45,
    change_percent=0.41,
    volume=123456789,
    amount=1234567890.0,
)
```

### NorthFlowData

北向资金数据模型。

```python
from finscraper.models import NorthFlowData

data = NorthFlowData(
    date="2024-01-01",
    sh_inflow=50.5,
    sz_inflow=30.2,
    north_net_inflow=80.7,
)
```

---

## 完整示例

### 批量获取并存储数据

```python
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
)
from finscraper.storage import CSVStorage, ParquetStorage

# 创建获取器
index_fetcher = IndexFetcher()
north_fetcher = NorthFlowFetcher()
sector_fetcher = SectorFetcher()

# 创建存储器
csv_storage = CSVStorage()
parquet_storage = ParquetStorage()

# 获取数据
index_data = index_fetcher.fetch_spot()
north_data = north_fetcher.fetch_daily()
sector_data = sector_fetcher.fetch_spot()

# 存储为 CSV
csv_storage.save(index_data, "data/index.csv")
csv_storage.save(north_data, "data/north_flow.csv")

# 存储为 Parquet
parquet_storage.save(sector_data, "data/sector.parquet")
```

### 定时任务示例

```python
import schedule
import time
from finscraper.fetchers import IndexFetcher
from finscraper.storage import CSVStorage

def fetch_and_save():
    fetcher = IndexFetcher()
    storage = CSVStorage()
    
    data = fetcher.fetch_spot()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    storage.save(data, f"data/index_{timestamp}.csv")
    print(f"数据已保存: index_{timestamp}.csv")

# 每 5 分钟执行一次
schedule.every(5).minutes.do(fetch_and_save)

while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 更多信息

- [用户指南](./USER_GUIDE.md) - 详细使用教程
- [项目规格](./PROJECT_SPEC.md) - 项目设计文档
- [贡献指南](./CONTRIBUTING.md) - 如何贡献代码
