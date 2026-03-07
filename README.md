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
| A 股指数 | 上证指数、深证成指、创业板指等 | 新浪财经 |
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

#### 全局选项

```bash
# 查看版本
finscraper --version
finscraper -V

# 查看帮助
finscraper --help

# 详细日志模式 (-v=INFO, -vv=DEBUG)
finscraper -v index spot
finscraper -vv index spot

# 安静模式（只显示错误）
finscraper -q index spot

# 指定配置文件
finscraper -c config.yaml index spot
```

#### 指数命令 (index)

```bash
# 列出所有可用指数（支持 --format 参数）
finscraper index list
finscraper index list --format json
finscraper index list -f json

# 获取指数实时行情（所有指数）
finscraper index spot

# 获取指定指数的实时行情
finscraper index spot --symbols sh000001,sz399001
finscraper index spot -s sh000001

# 获取指数历史数据
finscraper index history 000001
finscraper index history 000001 --start-date 20240101 --end-date 20241231
finscraper index history 000001 --period daily      # daily|weekly|monthly

# 保存数据到文件
finscraper index spot --output-path data/index_spot.csv
finscraper index spot -p data/index_spot.csv
finscraper index spot -p data/index_spot.json --output json
```

#### 北向资金命令 (north-flow)

```bash
# 获取北向资金日数据
finscraper north-flow daily

# 获取北向资金日内数据
finscraper north-flow intraday
```

#### 板块命令 (sector)

```bash
# 获取板块列表和实时行情
finscraper sector spot

# （板块列表已集成在实时行情命令中）
```

#### 大宗商品命令 (commodity)

```bash
# 列出所有商品（支持 --format 参数）
finscraper commodity list
finscraper commodity list --format json
finscraper commodity list -f json

# 获取商品实时行情
finscraper commodity spot

# 获取商品历史数据
finscraper commodity history AU0
finscraper commodity history AU0 --start-date 20240101 --end-date 20241231
finscraper commodity history AU0 --period daily      # daily|weekly|monthly

# 保存数据到文件
finscraper commodity spot --output-path data/commodity_spot.csv
finscraper commodity spot -p data/commodity_spot.csv
```

#### 资金流向命令 (money-flow)

```bash
# 获取个股资金流向
finscraper money-flow stock

# 获取板块资金流向
finscraper money-flow sector

# 获取两市资金流向
finscraper money-flow market

# 保存数据到文件
finscraper money-flow stock --output-path data/stock_money_flow.csv
finscraper money-flow stock -p data/stock_money_flow.csv
```

#### 新闻命令 (news)

```bash
# 获取全球财经资讯
finscraper news global

# 获取A股公告
finscraper news alert

# 获取个股资讯
finscraper news stock 000001

# 保存数据到文件
finscraper news global --output-path data/global_news.csv
finscraper news global -p data/global_news.csv
```

#### 一键获取所有数据

> ⚠️ 功能开发中，暂不可用

```bash
finscraper fetch-all
```

#### 输出格式选项

```bash
# index list 命令支持 --format 参数
finscraper index list --format table    # 默认，表格格式
finscraper index list --format json     # JSON格式
finscraper index list -f json

# 文件保存格式（--output 参数）
finscraper index spot --output csv      # CSV格式（默认）
finscraper index spot --output json     # JSON格式
finscraper index spot --output parquet  # Parquet格式
finscraper index spot --output sqlite   # SQLite格式
finscraper index spot -o json

# 组合使用示例
finscraper index spot -o csv -p data/spot.csv
finscraper index list -f json -o json -p data/index.json
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
