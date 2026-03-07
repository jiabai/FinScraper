# FinScraper

基于 akshare 的专业金融数据获取工具，支持 CLI 和 Python API，提供 A 股指数、北向资金、板块、大宗商品、资金流向和重要新闻等数据。

## 功能特点

- ✅ **指数数据**：A 股指数实时行情、历史数据
- ✅ **北向资金**：北向资金日数据和日内数据
- ✅ **板块数据**：板块列表、实时行情、成分股
- ✅ **大宗商品**：商品实时行情、历史数据
- ✅ **资金流向**：个股、板块和市场资金流向
- ✅ **重要新闻**：全球新闻、新闻提醒、个股新闻
- ✅ **CLI 工具**：强大的命令行工具，支持多种输出格式
- ✅ **Python API**：简洁的 Python API，易于集成
- ✅ **多种存储格式**：CSV、JSON、Parquet、SQLite
- ✅ **重试机制**：内置请求重试和错误处理
- ✅ **日志系统**：完善的日志记录

## 数据类型

| 数据类型 | 说明 | 数据源 |
|---------|------|--------|
| A 股指数 | 上证指数、深证成指、创业板指等 | 东方财富 |
| 北向资金 | 沪股通、深股通资金流向 | 东方财富 |
| 板块数据 | 行业板块、概念板块数据 | 东方财富 |
| 大宗商品 | 黄金、白银、原油等商品行情 | 东方财富 |
| 资金流向 | 个股、板块、市场资金流向 | 东方财富 |
| 重要新闻 | 全球财经新闻、市场提醒 | 东方财富 |

## 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用

```bash
# 查看版本
finscraper --version

# 查看帮助
finscraper --help

# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231

# 保存数据到文件
finscraper index spot --output-path data/index_spot.csv

# 获取北向资金日数据
finscraper north-flow daily

# 获取板块列表
finscraper sector list

# 获取板块实时行情
finscraper sector spot

# 获取大宗商品实时行情
finscraper commodity spot

# 获取资金流向数据
finscraper money-flow market

# 获取全球新闻
finscraper news global

# JSON 输出
finscraper index spot --format json

# 详细日志模式
finscraper -v index spot

# 一键获取所有数据
finscraper fetch-all
```

### 脚本使用

```bash
# 运行示例脚本
python scripts/example.py

# 一键获取所有数据（向后兼容）
python scripts/fetch_all.py
```

### Python API 使用

#### IndexFetcher

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

#### NorthFlowFetcher

```python
from finscraper.fetchers.north_flow import NorthFlowFetcher

fetcher = NorthFlowFetcher()
daily = fetcher.fetch_daily()
intraday = fetcher.fetch_intraday()
```

#### SectorFetcher

```python
from finscraper.fetchers.sector import SectorFetcher

fetcher = SectorFetcher()
sectors = fetcher.fetch_list()
spot = fetcher.fetch_spot()
stocks = fetcher.fetch_stocks("sector_code")
```

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

## 项目结构

```
FinScraper/
├── finscraper/          # 主代码包
│   ├── core/            # 核心模块
│   ├── fetchers/        # 数据获取模块
│   ├── models/          # 数据模型
│   ├── storage/         # 存储模块
│   └── config/          # 配置文件
├── tests/               # 测试代码
├── data/                # 数据文件（不提交到Git）
├── docs/                # 文档
├── scripts/             # 脚本文件
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明
```

## 开发

### 安装依赖

```bash
pip install -e .[dev]
```

### 代码格式化

```bash
# 格式化代码
black .
isort .
```

### 代码检查

```bash
# 运行所有检查
pylint finscraper/
flake8 finscraper/
mypy finscraper/
```

### 运行测试

```bash
pytest
```

## 开发流程

1. 创建新分支进行开发
2. 编写代码和测试
3. 运行格式化和检查工具
4. 提交代码
