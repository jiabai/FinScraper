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

# 保存数据到文件
finscraper index spot --output-path data/index_spot.csv

# 获取北向资金日数据
finscraper north-flow daily

# 获取板块列表
finscraper sector list

# 获取板块实时行情
finscraper sector spot

# JSON 输出
finscraper index spot --format json
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
