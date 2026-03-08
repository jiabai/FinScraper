# FinScraper - 金融数据获取项目

## 项目信息
- **项目名称**: FinScraper
- **创建日期**: 2026-03-07
- **负责人**: FinScraper Team
- **版本**: v1.4

---

## 1. PRD (产品需求文档)

### 1.1 项目背景
需要一个基于 akshare 库的金融数据获取工具，能够方便地获取 A 股指数、北向资金、板块数据、大宗商品、资金流向、重要新闻等多维度金融数据，并进行统一的数据清洗、转换和存储。

### 1.2 目标用户
- 量化分析师
- 金融数据研究员
- 个人投资者
- 金融软件开发人员

### 1.3 核心需求

| 需求编号 | 需求名称 | 需求描述 | 优先级 |
|---------|---------|---------|--------|
| REQ-001 | A 股指数数据 | 获取主要 A 股指数（上证指数、深证成指、创业板指等）的实时和历史行情数据 | P0 |
| REQ-002 | 北向资金数据 | 获取沪股通、深股通、北向资金净流入、净买入等数据 | P0 |
| REQ-003 | 板块数据 | 获取行业板块、概念板块的涨跌幅、领涨股等数据 | P0 |
| REQ-004 | 大宗商品数据 | 获取原油、黄金、白银、铜等大宗商品的价格数据 | P0 |
| REQ-005 | 资金流向数据 | 获取个股、板块的主力资金、超大单、大单、中单、小单资金流向数据 | P0 |
| REQ-006 | 重要新闻数据 | 获取财经新闻、市场资讯、公告等信息 | P1 |
| REQ-007 | 数据存储 | 支持将数据存储为 CSV、JSON、Parquet、SQLite 等格式 | P0 |
| REQ-008 | 数据模型 | 使用 Pydantic 定义统一的数据模型，确保数据类型安全 | P1 |
| REQ-009 | 增量更新 | 支持数据的增量更新，避免重复获取 | P2 |
| REQ-010 | 命令行工具 | 提供功能完善的 CLI，支持丰富的参数配置 | P0 |

### 1.4 功能范围
- **包含**: A 股指数、北向资金、板块数据、大宗商品、资金流向、重要新闻的数据获取、清洗、存储
- **不包含**: 实时数据推送、机器学习预测、Web 界面、交易功能

### 1.5 成功指标
- 支持 6+ 类数据获取
- 提供完整的命令行工具
- 代码测试覆盖率 > 80%
- 数据获取成功率 > 99%（基于 akshare 可靠性）
- 统一的数据模型覆盖所有数据类型

---

## 2. 技术栈

### 2.1 核心技术选型

| 类别 | 技术选型 | 版本 | 选型理由 |
|-----|---------|------|---------|
| 编程语言 | Python | 3.10+ | 生态丰富，数据分析工具成熟 |
| 金融数据源 | akshare | latest | 开源、免费、数据源丰富的金融数据接口库 |
| 数据处理 | pandas | 2.0+ | 数据分析标准库 |
| 数据验证 | pydantic | 2.0+ | 类型安全，性能优秀 |
| 配置管理 | pydantic-settings | 2.0+ | 类型安全的配置管理 |
| 数据存储 | pandas (CSV/JSON/Parquet) + SQLite | - | 灵活多样的存储选项 |
| CLI 框架 | Typer | 0.12+ | 类型安全、自动生成帮助文档、现代美观 |
| 测试框架 | pytest | 7.4+ | 功能强大，插件丰富 |
| 代码格式化 | black | 23.0+ | 统一代码风格 |
| 导入排序 | isort | 5.12+ | 配合 black 使用 |
| 代码检查 | pylint + flake8 | 2.17+/6.0+ | 代码质量保证 |
| 类型检查 | mypy | 1.0+ | 静态类型检查 |

### 2.2 开发工具
- IDE: VS Code / PyCharm
- 版本控制: Git
- 虚拟环境: venv
- 任务运行: 直接使用 Python 命令或 CLI

### 2.3 依赖列表

#### 生产依赖
```toml
dependencies = [
    "akshare>=1.12.0",
    "pandas>=2.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "openpyxl>=3.1.0",
    "pyarrow>=14.0.0",
    "loguru>=0.7.0",
    "typer>=0.12.0",
]
```

#### 开发依赖
```toml
dev = [
    "black>=23.0.0",
    "isort>=5.12.0",
    "pylint>=2.17.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]
```

---

## 3. 架构设计

### 3.1 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                 用户接口层 (CLI / Python)                  │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │  CLI 应用 (Typer)│         │   Python 库 API   │      │
│  └────────┬─────────┘         └────────┬─────────┘      │
└───────────┼─────────────────────────────┼────────────────┘
            │                             │
            └────────────┬────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Data Fetchers (数据获取层)                │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │  IndexFetcher   │  │  NorthFlowFetcher│                 │
│  │  (A股指数)      │  │  (北向资金)      │                 │
│  └─────────────────┘  └─────────────────┘                 │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │  SectorFetcher  │  │  CommodityFetcher│                 │
│  │  (板块数据)      │  │  (大宗商品)      │                 │
│  └─────────────────┘  └─────────────────┘                 │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │  MoneyFlowFetcher│ │  NewsFetcher    │                 │
│  │  (资金流向)      │  │  (重要新闻)      │                 │
│  └─────────────────┘  └─────────────────┘                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Core (核心层)                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  akshare API 封装层                                │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  数据清洗与转换层                                   │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Models (模型)   │    │   Storage (存储)  │
│  - schemas.py    │    │  - storage.py    │
│  - 数据模型定义   │    │  - 多格式存储     │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Config (配置)                          │
│  - settings.py                                            │
└─────────────────────────────────────────────────────────┘
```

### 3.2 目录结构

```
FinScraper/
├── finscraper/
│   ├── cli/                  # CLI 命令行工具
│   │   ├── __init__.py
│   │   ├── main.py          # CLI 入口
│   │   ├── index.py         # 指数命令
│   │   ├── north_flow.py    # 北向资金命令
│   │   ├── sector.py        # 板块命令
│   │   ├── commodity.py     # 大宗商品命令
│   │   ├── money_flow.py    # 资金流向命令
│   │   ├── news.py          # 新闻命令
│   │   └── fetch_all.py     # 一键获取命令
│   ├── fetchers/             # 数据获取器
│   │   ├── __init__.py
│   │   ├── base.py          # 基础获取器
│   │   ├── index.py         # A 股指数
│   │   ├── north_flow.py    # 北向资金
│   │   ├── sector.py        # 板块数据
│   │   ├── commodity.py     # 大宗商品
│   │   ├── money_flow.py    # 资金流向
│   │   └── news.py          # 重要新闻
│   ├── core/                 # 核心功能
│   │   ├── __init__.py
│   │   ├── akshare_client.py # akshare 客户端封装
│   │   └── data_cleaner.py  # 数据清洗
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── index.py         # 指数模型
│   │   ├── north_flow.py    # 北向资金模型
│   │   ├── sector.py        # 板块模型
│   │   ├── commodity.py     # 大宗商品模型
│   │   ├── money_flow.py    # 资金流向模型
│   │   └── news.py          # 新闻模型
│   ├── filters/              # 数据筛选模块
│   │   ├── __init__.py
│   │   ├── topic_filter.py  # 主题新闻筛选器
│   │   └── topic_config.py  # 主题关键词配置
│   ├── storage/              # 存储模块
│   │   ├── __init__.py
│   │   ├── base.py          # 基础存储
│   │   ├── csv_storage.py   # CSV 存储
│   │   ├── json_storage.py  # JSON 存储
│   │   ├── parquet_storage.py # Parquet 存储
│   │   └── sqlite_storage.py # SQLite 存储
│   └── config/               # 配置
│       ├── __init__.py
│       └── settings.py       # 配置管理
├── tests/                    # 测试
│   ├── __init__.py
│   ├── test_cli/            # CLI 测试
│   ├── test_fetchers/
│   ├── test_core/
│   ├── test_filters/         # 筛选模块测试
│   ├── test_models/
│   └── test_storage/
├── data/                     # 数据文件（不提交）
│   ├── index/
│   ├── north_flow/
│   ├── sector/
│   ├── commodity/
│   ├── money_flow/
│   └── news/
├── logs/                     # 日志文件（不提交）
├── docs/                     # 文档
│   ├── CODING_STANDARDS.md
│   ├── VIBE_CODING_TEMPLATE.md
│   └── PROJECT_SPEC.md
├── scripts/                  # 脚本（保留用于向后兼容）
│   ├── fetch_all.py         # 一键获取所有数据
│   └── example.py           # 使用示例
├── pyproject.toml            # 项目配置
├── .gitignore
└── README.md
```

### 3.3 分层架构

#### 3.3.1 CLI 层（命令行接口）
- 职责: 提供用户友好的命令行接口
- 基于 Typer 框架
- 支持丰富的参数配置和自动帮助文档
- 示例:
  ```python
  # finscraper/cli/index.py
  import typer
  from finscraper.fetchers.index import IndexFetcher
  from finscraper.storage import get_storage

  app = typer.Typer(name="index", help="A 股指数数据命令")

  @app.command()
  def spot(
      output: str = typer.Option("csv", help="输出格式: csv/json/parquet/sqlite"),
      output_path: str = typer.Option(None, help="输出文件路径"),
  ):
      fetcher = IndexFetcher()
      data = fetcher.fetch_spot()
      if output_path:
          storage = get_storage(output)
          storage.save(data, output_path)
      else:
          typer.echo(data.to_string())

  @app.command()
  def history(
      symbol: str = typer.Argument(..., help="指数代码"),
      start_date: str = typer.Option(None, help="开始日期 (YYYYMMDD)"),
      end_date: str = typer.Option(None, help="结束日期 (YYYYMMDD)"),
      period: str = typer.Option("daily", help="周期: daily/weekly/monthly"),
      output: str = typer.Option("csv", help="输出格式"),
      output_path: str = typer.Option(None, help="输出文件路径"),
  ):
      fetcher = IndexFetcher()
      data = fetcher.fetch_history(symbol, start_date, end_date, period)
      if output_path:
          storage = get_storage(output)
          storage.save(data, output_path)
      else:
          typer.echo(data.to_string())
  ```

#### 3.3.2 Fetchers 层（数据获取层）
- 职责: 具体数据类型的获取实现
- 继承 BaseFetcher，实现 fetch 方法
- 示例:
  ```python
  # finscraper/fetchers/index.py
  from finscraper.fetchers.base import BaseFetcher
  from finscraper.models.index import IndexData

  class IndexFetcher(BaseFetcher):
      def __init__(self):
          super().__init__("index")

      def fetch_index_list(self) -> list[IndexData]:
          pass

      def fetch_index_history(self, symbol: str, start_date: str, end_date: str) -> list[IndexData]:
          pass
  ```

#### 3.3.3 Core 层（核心层）
- 职责: akshare API 封装、数据清洗与转换
- AkShareClient: 统一的 akshare 调用入口
- DataCleaner: 数据清洗、格式转换、空值处理
- 示例:
  ```python
  # finscraper/core/akshare_client.py
  import akshare as ak

  class AkShareClient:
      @staticmethod
      def get_index_zh_a_spot_sina() -> pd.DataFrame:
          return ak.stock_zh_index_spot_sina()

      @staticmethod
      def get_stock_hsgt_fund_flow_summary_em() -> pd.DataFrame:
          return ak.stock_hsgt_fund_flow_summary_em()
      
      @staticmethod
      def get_stock_hsgt_fund_min_em() -> pd.DataFrame:
          return ak.stock_hsgt_fund_min_em()
      
      @staticmethod
      def get_stock_sector_spot() -> pd.DataFrame:
          return ak.stock_sector_spot()
  ```

#### 3.3.4 Models 层（数据模型层）
- 职责: 定义所有数据类型的 Pydantic 模型
- 确保数据类型安全
- 示例:
  ```python
  # finscraper/models/index.py
  from pydantic import BaseModel
  from datetime import datetime

  class IndexInfo(BaseModel):
      symbol: str
      name: str
      price: float
      change: float
      change_percent: float
      volume: int
      amount: float
      updated_at: datetime

  class IndexHistory(BaseModel):
      symbol: str
      date: datetime
      open: float
      high: float
      low: float
      close: float
      volume: int
      amount: float
  ```

#### 3.3.5 Storage 层（存储层）
- 职责: 多格式数据存储
- 支持: CSV、JSON、Parquet、SQLite
- 示例:
  ```python
  # finscraper/storage/csv_storage.py
  from finscraper.storage.base import BaseStorage
  import pandas as pd

  class CSVStorage(BaseStorage):
      def save(self, data: pd.DataFrame, path: str) -> None:
          data.to_csv(path, index=False, encoding='utf-8-sig')

      def load(self, path: str) -> pd.DataFrame:
          return pd.read_csv(path)
  ```

### 3.4 CLI 设计

#### 3.4.1 CLI 命令结构

```
finscraper
├── --version / -V          # 显示版本信息
├── --help / -h             # 显示帮助
├── --config / -c           # 指定配置文件
├── --verbose / -v          # 详细日志 (可多次: -v, -vv, -vvv)
├── --quiet / -q            # 安静模式，只显示错误
│
├── index                   # A 股指数命令组
│   ├── list                # 列出可用指数
│   ├── spot                # 获取实时行情
│   └── history             # 获取历史数据
│
├── north-flow              # 北向资金命令组
│   ├── daily               # 获取单日数据
│   └── intraday            # 获取分时数据
│
├── sector                  # 板块数据命令组
│   └── spot                # 板块实时行情（包含板块列表）
│
├── commodity               # 大宗商品命令组
│   ├── list                # 列出商品
│   ├── spot                # 实时行情
│   └── history             # 历史数据
│
├── money-flow              # 资金流向命令组
│   ├── stock               # 个股资金流
│   ├── sector              # 板块资金流
│   └── market              # 两市资金流
│
├── news                    # 新闻命令组
│   ├── global              # 全球财经资讯
│   ├── alert               # A 股公告
│   └── stock               # 个股资讯
│
└── fetch-all               # 一键获取所有数据
```

#### 3.4.2 全局选项

| 选项 | 简写 | 说明 | 默认值 |
|-----|------|------|--------|
| `--config` | `-c` | 指定配置文件路径 | None |
| `--verbose` | `-v` | 详细日志级别（-v=INFO, -vv=DEBUG） | WARNING |
| `--quiet` | `-q` | 安静模式，只显示错误 | False |
| `--version` | `-V` | 显示版本信息 | - |
| `--help` | `-h` | 显示帮助信息 | - |

#### 3.4.3 Index 命令详解

**list - 列出可用指数**
```bash
finscraper index list [--format table|json]
```

**spot - 获取实时行情**
```bash
finscraper index spot \
    [--symbols 000001,399001] \
    [--output csv|json|parquet|sqlite] \
    [--output-path data/index/spot.csv]
```

**history - 获取历史数据**
```bash
finscraper index history 000001 \
    --start-date 20240101 \
    --end-date 20241231 \
    --period daily|weekly|monthly \
    --output csv \
    --output-path data/index/000001.csv
```

#### 3.4.4 North-Flow 命令详解

**daily - 获取单日数据**
```bash
finscraper north-flow daily \
    [--start-date 20240101] \
    [--end-date 20241231] \
    --output csv \
    --output-path data/north_flow/daily.csv
```

**intraday - 获取分时数据**
```bash
finscraper north-flow intraday \
    --date 20240101 \
    --output csv \
    --output-path data/north_flow/intraday_20240101.csv
```

#### 3.4.5 Sector 命令详解

**spot - 板块实时行情（包含板块列表）**
```bash
finscraper sector spot \
    --format table|json \
    --output csv|json|parquet|sqlite \
    --output-path data/sector/spot.csv
```

#### 3.4.6 Commodity 命令详解

**list - 列出商品**
```bash
finscraper commodity list \
    --category precious|base|energy|agriculture \
    --format table|json
```

**spot - 实时行情**
```bash
finscraper commodity spot \
    --symbols gold,silver,crude_oil \
    --output csv \
    --output-path data/commodity/spot.csv
```

**history - 历史数据**
```bash
finscraper commodity history gold \
    --start-date 20240101 \
    --end-date 20241231 \
    --output csv \
    --output-path data/commodity/gold_history.csv
```

#### 3.4.7 Money-Flow 命令详解

**stock - 个股资金流**
```bash
finscraper money-flow stock 000001 \
    --indicator today|week|month \
    --output csv \
    --output-path data/money_flow/stock_000001.csv
```

**sector - 板块资金流**
```bash
finscraper money-flow sector \
    --indicator today \
    --output csv \
    --output-path data/money_flow/sector_today.csv
```

**market - 两市资金流**
```bash
finscraper money-flow market \
    --output csv \
    --output-path data/money_flow/market.csv
```

#### 3.4.8 News 命令详解

**global - 全球财经资讯**
```bash
finscraper news global \
    --limit 50 \
    --output json \
    --output-path data/news/global.json
```

**alert - A 股公告**
```bash
finscraper news alert 000001 \
    --start-date 20240101 \
    --output json \
    --output-path data/news/alert_000001.json
```

**stock - 个股资讯**
```bash
finscraper news stock 000001 \
    --limit 20 \
    --output json \
    --output-path data/news/stock_000001.json
```

**topics - 列出所有可用专题**
```bash
finscraper news topics
```

**topic - 获取指定专题的新闻**
```bash
# 获取中东地缘相关新闻（表格格式）
finscraper news topic --name "中东地缘"

# 仅输出纯 URL 列表
finscraper news topic --name "中东地缘" --urls-only

# 简要输出（标题、时间、摘要、链接）
finscraper news topic --name "中东地缘" --brief

# 保存到文件
finscraper news topic --name "中东地缘" --output csv --output-path middle_east_news.csv

# 同时匹配新闻内容
finscraper news topic --name "中东地缘" --match-content
```

#### 3.4.9 Fetch-All 命令详解

**一键获取所有数据**
```bash
finscraper fetch-all \
    --data-dir ./data \
    --format parquet \
    --include index,north-flow,sector \
    --exclude news
```

#### 3.4.10 使用示例

```bash
# 显示帮助
finscraper --help
finscraper index --help
finscraper index spot --help

# 获取指数实时行情并显示
finscraper index spot

# 获取指数实时行情并保存为 CSV
finscraper index spot --output csv --output-path data/index/spot.csv

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231 --output parquet

# 获取北向资金
finscraper north-flow daily --output csv

# 获取板块数据
finscraper sector spot --output csv

# 一键获取所有数据（详细日志）
finscraper -v fetch-all

# 使用配置文件
finscraper --config myconfig.toml index spot
```

### 3.5 数据模型设计

#### 3.5.1 A 股指数模型
```python
# finscraper/models/index.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class IndexSpot(BaseModel):
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

#### 3.5.2 北向资金模型
```python
# finscraper/models/north_flow.py
from pydantic import BaseModel
from datetime import datetime

class NorthFlowDaily(BaseModel):
    date: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
    sh_net_buy: float
    sz_net_buy: float
    total_net_buy: float

class NorthFlowIntraday(BaseModel):
    time: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
```

#### 3.5.3 板块数据模型
```python
# finscraper/models/sector.py
from pydantic import BaseModel
from datetime import datetime

class SectorSpot(BaseModel):
    sector_code: str
    sector_name: str
    change_percent: float
    lead_stock: str
    lead_stock_change_percent: float
    total_stock_count: int
    up_count: int
    down_count: float
    amount: float
    updated_at: datetime

class SectorStock(BaseModel):
    sector_code: str
    sector_name: str
    stock_code: str
    stock_name: str
    change_percent: float
    price: float
    volume: int
    amount: float
```

#### 3.5.4 大宗商品模型
```python
# finscraper/models/commodity.py
from pydantic import BaseModel
from datetime import datetime

class CommoditySpot(BaseModel):
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
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int
```

#### 3.5.5 资金流向模型
```python
# finscraper/models/money_flow.py
from pydantic import BaseModel
from datetime import datetime

class StockMoneyFlow(BaseModel):
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
    sector_code: str
    sector_name: str
    date: datetime
    net_inflow: float
    net_inflow_percent: float
    lead_stock: str
```

#### 3.5.6 新闻模型
```python
# finscraper/models/news.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsItem(BaseModel):
    title: str
    content: Optional[str] = None
    source: str
    publish_time: datetime
    url: Optional[str] = None
    importance: Optional[int] = None
```

### 3.6 详细需求说明

#### 3.6.1 A 股指数数据需求

**功能描述**: 获取主要 A 股指数的实时行情和历史数据

**包含指数**:
- 上证指数 (000001.SH)
- 深证成指 (399001.SZ)
- 创业板指 (399006.SZ)
- 沪深300 (000300.SH)
- 中证500 (000905.SH)
- 上证50 (000016.SH)
- 科创50 (000688.SH)

**数据字段**:
- 实时行情: 最新价、涨跌幅、涨跌额、成交量、成交额、最高、最低、今开、昨收
- 历史数据: 日期、开盘价、最高价、最低价、收盘价、成交量、成交额、涨跌幅

**akshare 接口**:
- `ak.stock_zh_index_spot_sina()` - 实时行情（新浪财经数据源）
- `ak.index_zh_a_hist(symbol, period, start_date, end_date)` - 历史数据

#### 3.6.2 北向资金数据需求

**功能描述**: 获取沪股通、深股通、北向资金的净流入、净买入数据

**数据类型**:
- 单日数据: 日期、沪股通净流入、深股通净流入、合计净流入、沪股通净买入、深股通净买入、合计净买入
- 分时数据: 时间点、沪股通净流入、深股通净流入、合计净流入

**akshare 接口**:
- `ak.stock_hsgt_fund_flow_summary_em()` - 单日净流入数据
- `ak.stock_hsgt_fund_min_em()` - 分时数据

#### 3.6.3 板块数据需求

**功能描述**: 获取行业板块、概念板块的涨跌幅、领涨股等数据

**板块类型**:
- 行业板块
- 概念板块
- 地域板块

**数据字段**:
- 板块代码、板块名称
- 涨跌幅
- 领涨股及涨跌幅
- 上涨家数、下跌家数
- 板块成交额
- 板块成分股列表

**akshare 接口**:
- `ak.stock_sector_spot()` - 板块实时行情

#### 3.6.4 大宗商品数据需求

**功能描述**: 获取原油、黄金、白银、铜等大宗商品的价格数据

**商品种类**:
- 贵金属: 黄金、白银
- 基本金属: 铜、铝、锌、铅、镍、锡
- 能源: 原油、天然气
- 农产品: 大豆、玉米、小麦

**数据字段**:
- 商品代码、商品名称
- 最新价、涨跌幅、涨跌额
- 计价单位
- 最高、最低、今开、昨收
- 持仓量（期货）

**akshare 接口**:
- `ak.futures_zh_spot()` - 国内期货实时行情
- `ak.futures_global_commodity()` - 全球大宗商品
- `ak.get_international_gold()` - 国际黄金

#### 3.6.5 资金流向数据需求

**功能描述**: 获取个股、板块的主力资金、超大单、大单、中单、小单资金流向数据

**数据类型**:
- 个股资金流向
- 板块资金流向
- 两市资金流向

**资金分类**:
- 主力资金
- 超大单
- 大单
- 中单
- 小单

**数据字段**:
- 净流入金额
- 净流入占比
- 净流出金额
- 净流出占比

**akshare 接口**:
- `ak.stock_individual_fund_flow_rank(indicator="今日")` - 个股资金流排名
- `ak.stock_sector_fund_flow_rank(indicator="今日")` - 板块资金流排名
- `ak.stock_market_fund_flow()` - 两市资金流向

#### 3.6.6 重要新闻数据需求

**功能描述**: 获取财经新闻、市场资讯、公告等信息

**新闻类型**:
- 财经要闻
- 市场资讯
- 公司公告
- 研报摘要

**数据字段**:
- 新闻标题
- 新闻内容（摘要）
- 新闻来源
- 发布时间
- 新闻链接
- 重要程度

**akshare 接口**:
- `ak.stock_info_global_em()` - 全球财经资讯
- `ak.stock_zh_a_alert_em()` - A 股公告
- `ak.stock_zh_a_eminfo(symbol)` - 个股资讯

#### 3.6.7 主题新闻筛选需求

**功能描述**: 支持按特定主题关键词筛选新闻，帮助用户快速获取关注领域的资讯

**内置主题**:
- 中东地缘: 中东地区相关新闻（以色列、巴勒斯坦、伊朗、沙特等）
- 全国两会: 全国人大、政协相关新闻
- 美联储: 美联储货币政策相关新闻
- 人工智能: AI、大模型相关新闻
- 新能源: 光伏、风电、电动车等相关新闻
- 房地产: 房地产行业相关新闻

**筛选功能**:
- 列出所有可用专题
- 按专题名称筛选新闻（基于标题关键词匹配）
- 支持同时匹配新闻内容
- 支持仅输出新闻 URL 列表
- 支持简要输出（标题、时间、摘要、链接）
- 支持多专题同时筛选

**akshare 接口**:
- `ak.stock_info_global_em()` - 全球财经资讯（用于筛选）

### 3.7 API 设计

#### 3.7.1 Python 库使用示例

```python
from finscraper.fetchers.index import IndexFetcher
from finscraper.fetchers.north_flow import NorthFlowFetcher
from finscraper.filters import TopicFilter
from finscraper.storage.csv_storage import CSVStorage
import akshare as ak

index_fetcher = IndexFetcher()
spot_data = index_fetcher.fetch_spot()
print(spot_data)

history_data = index_fetcher.fetch_history("000001", "20240101", "20241231")

storage = CSVStorage()
storage.save(history_data, "data/index/000001_history.csv")

north_flow_fetcher = NorthFlowFetcher()
north_flow_data = north_flow_fetcher.fetch_daily()

# 主题新闻筛选示例
df = ak.stock_info_global_em()
filter = TopicFilter()
topics = filter.list_topics()
print("可用专题:", topics)
filtered_df = filter.filter_by_topic(df, topic="中东地缘")
print(filtered_df)
urls = filter.get_topic_urls(df, topic="中东地缘")
print("相关新闻URL:", urls)
```

#### 3.7.2 CLI 使用示例

```bash
# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231 --output csv --output-path data/index/000001.csv

# 获取北向资金
finscraper north-flow daily --output csv

# 一键获取所有数据
finscraper -v fetch-all
```

#### 3.7.3 一键获取脚本（保留用于向后兼容）

```python
# scripts/fetch_all.py
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
    CommodityFetcher,
    MoneyFlowFetcher,
    NewsFetcher,
)
from finscraper.storage.csv_storage import CSVStorage
import datetime

def main():
    today = datetime.datetime.now().strftime("%Y%m%d")
    storage = CSVStorage()

    index_fetcher = IndexFetcher()
    index_data = index_fetcher.fetch_spot()
    storage.save(index_data, f"data/index/spot_{today}.csv")

    north_flow_fetcher = NorthFlowFetcher()
    north_flow_data = north_flow_fetcher.fetch_daily()
    storage.save(north_flow_data, f"data/north_flow/daily_{today}.csv")

    sector_fetcher = SectorFetcher()
    sector_data = sector_fetcher.fetch_industry()
    storage.save(sector_data, f"data/sector/industry_{today}.csv")

if __name__ == "__main__":
    main()
```

### 3.8 关键技术决策

| 决策项 | 决策 | 备选方案 | 决策理由 |
|-------|------|---------|---------|
| 数据源 | akshare | Tushare/BAOSTOCK/自建爬虫 | 开源免费、数据源丰富、维护活跃 |
| 配置管理 | pydantic-settings | python-dotenv | 类型安全，支持验证 |
| 数据验证 | pydantic | dataclasses/attrs | 生态好，性能优秀 |
| 代码格式化 | black | autopep8/yapf | 零配置，统一风格 |
| 数据存储 | 多格式支持 (CSV/Parquet/SQLite) | 单一格式 | 灵活满足不同需求 |
| 日志系统 | loguru | logging | 更现代的 API，更好的格式化和性能 |
| CLI 框架 | Typer | Click/argparse | 类型安全、自动生成帮助文档、现代美观 |

### 3.9 错误处理策略

#### 3.9.1 错误类型
- **网络错误**: akshare 请求失败、超时
- **数据错误**: 数据格式异常、字段缺失
- **存储错误**: 文件写入失败、数据库连接失败
- **参数错误**: 输入参数验证失败
- **CLI 错误**: 命令参数无效、配置错误

#### 3.9.2 错误处理原则
1. 捕获并记录所有异常，不静默失败
2. 提供清晰的错误信息，便于调试
3. 对于可恢复的错误，实现重试机制
4. 使用自定义异常类，便于错误分类处理
5. CLI 输出友好的错误信息，使用颜色区分

#### 3.9.3 重试机制
- 网络请求失败：最多重试 3 次，指数退避（2s, 4s, 8s）
- 可通过配置调整重试次数和间隔

### 3.10 日志系统设计

#### 3.10.1 日志级别
- **DEBUG**: 详细的调试信息（如原始数据、请求参数）
- **INFO**: 常规操作信息（如数据获取成功、存储完成）
- **WARNING**: 警告信息（如数据格式异常但可继续）
- **ERROR**: 错误信息（如请求失败、存储失败）
- **CRITICAL**: 严重错误（如系统无法运行）

#### 3.10.2 日志输出
- 控制台输出：INFO 及以上级别（可通过 -v/-vv 调整）
- 文件输出：DEBUG 及以上级别，按日期轮转
- 日志格式：`时间 | 级别 | 模块 | 消息`

### 3.11 配置项说明

#### 3.11.1 核心配置
```python
# finscraper/config/settings.py
class Settings(BaseSettings):
    # 数据目录
    data_dir: str = "data"
    
    # 请求配置
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 2
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/finscraper.log"
    
    # 存储配置
    default_storage_format: str = "csv"
    
    # CLI 配置
    default_output_format: str = "csv"
    
    model_config = {
        "env_prefix": "FINSCRAPER_",
    }
```

### 3.12 性能考虑

#### 3.12.1 数据量预估
- 指数实时数据：约 10KB/次
- 北向资金单日数据：约 5KB/次
- 板块数据：约 50KB/次
- 大宗商品数据：约 20KB/次
- 资金流向数据：约 100KB/次
- 新闻数据：约 100KB/次
- 总计：约 300KB/完整获取

#### 3.12.2 优化策略
1. 使用 Parquet 格式存储历史数据，节省空间和提高读写速度
2. 实现增量更新，避免重复获取
3. 对于大数据集，支持分批处理
4. 使用缓存减少重复请求（可选）
5. CLI 支持流式输出，避免内存溢出

### 3.13 安全考虑

- 不存储任何敏感信息（如账号密码）
- 所有数据文件不提交到 Git（通过 .gitignore 控制）
- 使用环境变量管理配置，避免硬编码
- 对于公开数据源，不涉及数据隐私问题
- CLI 参数验证，防止路径遍历攻击

---

## 4. 实施计划

### 4.1 里程碑

| 里程碑 | 日期 | 交付物 |
|-------|------|--------|
| M1: 项目初始化 | 2026-03-07 | 项目骨架、配置、编码规范 |
| M2: 核心框架 | 2026-03-08 | 数据模型、Core 层、Storage 层 |
| M3: CLI 框架 | 2026-03-09 | CLI 基础框架、通用命令 |
| M4: 基础数据获取 | 2026-03-10 | A 股指数、北向资金、板块数据 |
| M5: 完整数据获取 | 2026-03-12 | 大宗商品、资金流向、新闻数据 |
| M6: 测试与文档 | 2026-03-14 | 测试代码 > 80%、使用示例、文档完善 |
| M7: 发布 v1.0 | 2026-03-15 | 正式版本 |

### 4.2 任务分解

#### Phase 1: 项目初始化 ✅
- [x] 创建项目结构
- [x] 配置开发环境（更新 pyproject.toml）
- [x] 编写编码规范
- [x] 编写项目文档

#### Phase 2: 核心框架
- [x] 更新 pyproject.toml 添加 akshare 依赖
- [ ] 实现日志系统（添加 loguru 依赖）
- [ ] 实现所有数据模型 (index, north_flow, sector, commodity, money_flow, news)
- [ ] 实现 AkShareClient (akshare_client.py)
- [ ] 实现 DataCleaner (data_cleaner.py)
- [ ] 实现 BaseFetcher (fetchers/base.py)
- [ ] 实现 Storage 层 (CSV/JSON/Parquet/SQLite)
- [ ] 实现异常处理和重试机制
- [ ] 编写核心层单元测试

#### Phase 3: CLI 框架
- [ ] 更新 pyproject.toml 添加 typer 依赖
- [ ] 配置 pyproject.toml 中的 entry points
- [ ] 实现 CLI 主入口 (cli/main.py)
- [ ] 实现全局选项处理（--version, --help, --verbose, --config）
- [ ] 实现 CLI 工具函数（输出格式化、进度条、颜色输出）
- [ ] 编写 CLI 基础测试

#### Phase 4: CLI 命令实现
- [ ] 实现 index 命令组 (list, spot, history)
- [ ] 实现 north-flow 命令组 (daily, intraday)
- [ ] 实现 sector 命令组 (list, spot, stocks)
- [ ] 实现 commodity 命令组 (list, spot, history)
- [ ] 实现 money-flow 命令组 (stock, sector, market)
- [ ] 实现 news 命令组 (global, alert, stock)
- [ ] 实现 fetch-all 命令
- [ ] 编写 CLI 集成测试

#### Phase 5: 基础数据获取
- [ ] 实现 IndexFetcher（A 股指数）
- [ ] 实现 NorthFlowFetcher（北向资金）
- [ ] 实现 SectorFetcher（板块数据）
- [ ] 编写 Fetchers 层单元测试
- [ ] 编写集成测试

#### Phase 6: 完整数据获取
- [ ] 实现 CommodityFetcher（大宗商品）
- [ ] 实现 MoneyFlowFetcher（资金流向）
- [ ] 实现 NewsFetcher（重要新闻）
- [ ] 编写完整测试
- [ ] 编写使用示例

#### Phase 7: 完善与优化
- [ ] 实现一键获取脚本 (scripts/fetch_all.py)（保留用于向后兼容）
- [ ] 实现示例脚本 (scripts/example.py)
- [ ] 完善 README.md
- [ ] 代码审查与优化
- [ ] 测试覆盖率 > 80%

---

## 5. 风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| akshare 接口变更 | 高 | 中 | 封装统一的客户端层，便于快速适配 |
| akshare 数据源失效 | 高 | 低 | 预留备用数据源接口设计 |
| 数据量大导致内存问题 | 中 | 中 | 支持分批获取和增量更新 |
| 请求频率限制 | 中 | 中 | 添加请求间隔和重试机制 |
| CLI 参数复杂导致用户困惑 | 中 | 低 | 提供详细的帮助文档和示例 |

---

## 6. 附录

### 6.1 参考资料
- [akshare 官方文档](https://akshare.akfamily.xyz/)
- [Typer 官方文档](https://typer.tiangolo.com/)
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Black 文档](https://black.readthedocs.io/)
- [Pydantic 文档](https://docs.pydantic.dev/)

### 6.2 术语表
- **akshare**: 开源的金融数据接口库
- **北向资金**: 沪股通和深股通的合称，指境外投资者投资 A 股的资金
- **Pydantic**: Python 数据验证库，使用类型注解
- **Typer**: 现代的 Python CLI 框架，基于类型注解
- **增量更新**: 只获取新增或变更的数据

### 6.3 变更记录

| 版本 | 日期 | 修改人 | 修改内容 |
|-----|------|-------|---------|
| v1.0 | 2026-03-07 | FinScraper Team | 初始版本 |
| v1.1 | 2026-03-07 | FinScraper Team | 细化需求，加入 akshare 和 6 类数据详细需求 |
| v1.2 | 2026-03-07 | FinScraper Team | 补充错误处理、日志系统、配置说明、性能考虑、安全考虑、快速开始、FAQ |
| v1.3 | 2026-03-07 | FinScraper Team | 添加完整的 CLI 设计，包括命令结构、参数说明、使用示例 |
| v1.4 | 2026-03-08 | FinScraper Team | 更新 API 引用：将 A 股指数数据源切换为新浪财经（stock_zh_index_spot_sina），更新北向资金 API（stock_hsgt_fund_flow_summary_em、stock_hsgt_fund_min_em），更新板块 API（stock_sector_spot）；简化 sector 命令，只保留 spot 命令 |

---

## 7. 快速开始指南

### 7.1 环境准备

```bash
# 克隆或进入项目目录
cd FinScraper

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -e .[dev]
```

### 7.2 CLI 快速使用

```bash
# 查看版本
finscraper --version

# 查看帮助
finscraper --help

# 获取指数实时行情
finscraper index spot

# 获取指数历史数据并保存
finscraper index history 000001 \
    --start-date 20240101 \
    --end-date 20241231 \
    --output csv \
    --output-path data/index/000001.csv

# 获取北向资金
finscraper north-flow daily --output csv

# 一键获取所有数据（详细日志）
finscraper -v fetch-all
```

### 7.3 Python 库使用

```python
# 导入需要的模块
from finscraper.fetchers.index import IndexFetcher
from finscraper.fetchers.north_flow import NorthFlowFetcher
from finscraper.storage.csv_storage import CSVStorage

# 获取指数实时行情
index_fetcher = IndexFetcher()
spot_data = index_fetcher.fetch_spot()
print(spot_data)

# 获取指数历史数据
history_data = index_fetcher.fetch_history(
    symbol="000001",
    start_date="20240101",
    end_date="20241231"
)

# 保存数据
storage = CSVStorage()
storage.save(history_data, "data/index/000001_history.csv")

# 获取北向资金
north_flow_fetcher = NorthFlowFetcher()
north_flow_data = north_flow_fetcher.fetch_daily()
```

### 7.4 使用一键获取脚本（保留用于向后兼容）

```bash
# 运行一键获取脚本
python scripts/fetch_all.py
```

### 7.5 开发工具命令

```bash
# 代码格式化
black .
isort .

# 代码检查
pylint finscraper/
flake8 finscraper/
mypy finscraper/

# 运行测试
pytest

# 运行测试并查看覆盖率
pytest --cov=finscraper
```

---

## 8. 常见问题（FAQ）

### 8.1 安装与配置

**Q: 安装 akshare 时遇到网络问题怎么办？**
A: 可以使用国内镜像源：
```bash
pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 如何修改默认配置？**
A: 有两种方式：
1. 使用环境变量：`export FINSCRAPER_DATA_DIR=/path/to/data`
2. 修改代码中的 `finscraper/config/settings.py`

**Q: CLI 命令无法识别怎么办？**
A: 请确保：
1. 使用了 editable 安装：`pip install -e .`
2. 虚拟环境已激活
3. 检查 `pyproject.toml` 中的 entry points 配置

### 8.2 数据获取

**Q: akshare 接口调用失败怎么办？**
A: 请检查：
1. 网络连接是否正常
2. akshare 版本是否为最新
3. 参考 akshare 官方文档确认接口是否有变更

**Q: 数据量太大导致内存不足怎么办？**
A: 可以：
1. 使用 Parquet 格式存储，更节省空间
2. 分批获取和处理数据
3. 只获取需要的字段

**Q: 如何实现增量更新？**
A: 记录上次获取的时间，下次只获取该时间之后的数据。具体实现可参考各 Fetcher 的实现。

### 8.3 存储相关

**Q: 应该选择哪种存储格式？**
A:
- **CSV**: 适合小数据量，需要人工查看的场景
- **Parquet**: 适合大数据量，需要高效读写的场景
- **SQLite**: 适合需要查询和关系型数据的场景
- **JSON**: 适合需要交换数据或与 Web 系统集成的场景

**Q: 如何将数据导出到 Excel？**
A: 使用 pandas 的 to_excel 方法：
```python
import pandas as pd
data.to_excel("output.xlsx", index=False)
```

### 8.4 CLI 使用

**Q: 如何查看命令的帮助信息？**
A: 使用 `--help` 选项：
```bash
finscraper --help
finscraper index --help
finscraper index spot --help
```

**Q: 如何开启调试日志？**
A: 使用 `-v` 或 `-vv` 选项：
```bash
finscraper -v index spot    # INFO 级别
finscraper -vv index spot   # DEBUG 级别
```

**Q: 如何指定输出格式？**
A: 使用 `--output` 选项：
```bash
finscraper index spot --output csv
finscraper index spot --output json
finscraper index spot --output parquet
```

### 8.5 开发与调试

**Q: 如何添加新的 CLI 命令？**
A:
1. 在 `finscraper/cli/` 中创建对应的命令文件
2. 定义 Typer app 和命令
3. 在 `cli/main.py` 中注册命令
4. 编写测试用例

**Q: 测试时如何避免真实的网络请求？**
A: 使用 pytest 的 mock 功能，模拟 akshare 的返回数据。

**Q: 如何测试 CLI 命令？**
A: 使用 `typer.testing.CliRunner` 进行测试，或者使用 subprocess 调用命令。

### 8.6 其他问题

**Q: 这个项目可以用于商业用途吗？**
A: 可以，本项目采用 MIT 许可证。但请注意：
1. akshare 的数据源可能有各自的使用条款
2. 请遵守相关网站的 robots.txt 和使用规范
3. 合理控制请求频率，避免对数据源造成压力

**Q: 如何贡献代码？**
A:
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

**Q: 遇到问题如何寻求帮助？**
A:
1. 查看本文档和 akshare 官方文档
2. 检查 GitHub Issues 是否有类似问题
3. 提交新的 Issue，详细描述问题和复现步骤
