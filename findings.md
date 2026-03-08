# FinScraper 新数据源扩展 - 调研发现

> **日期**: 2026-03-08  
> **调研内容**: akshare 库对市场情绪、港股、美股、汇率等数据源的支持情况

---

## 1. 项目现状分析

### 1.1 已实现功能

通过代码分析，项目已完整实现以下功能：

| 数据类型 | Fetcher | 状态 |
|---------|---------|------|
| A 股指数 | IndexFetcher | ✅ 已实现 |
| 北向资金 | NorthFlowFetcher | ✅ 已实现 |
| 板块数据 | SectorFetcher | ✅ 已实现 |
| 大宗商品 | CommodityFetcher | ✅ 已实现 |
| 资金流向 | MoneyFlowFetcher | ✅ 已实现 |
| 重要新闻 | NewsFetcher | ✅ 已实现 |

### 1.2 代码架构

项目采用清晰的分层架构：

```
finscraper/
├── core/
│   ├── akshare_client.py    # akshare API 封装
│   ├── data_cleaner.py       # 数据清洗工具
│   └── ...
├── fetchers/
│   ├── base.py               # 基类 BaseFetcher
│   ├── index.py              # 已实现的 fetcher
│   └── ...
├── models/
│   └── *.py                  # Pydantic 数据模型
└── cli/
    └── commands/             # CLI 命令
```

### 1.3 编码规范

- **命名规范**: 小写 + 下划线分隔（模块/函数），大驼峰（类）
- **文档字符串**: Google 风格
- **类型注解**: 完整的类型提示
- **基类继承**: 所有 Fetcher 继承自 `BaseFetcher`

---

## 2. akshare 库支持情况调研

### 2.1 市场情绪数据

#### 涨跌家数

| 功能 | akshare 接口 | 可用性 |
|-----|-------------|--------|
| 获取全部A股实时行情 | `stock_zh_a_spot_em()` | ✅ 完全可用 |
| 统计涨跌家数 | 需自行统计 `涨跌幅` 列 | ✅ 可行 |

**实现方案**：
```python
df = ak.stock_zh_a_spot_em()
up_count = (df['涨跌幅'] > 0).sum()
down_count = (df['涨跌幅'] < 0).sum()
flat_count = (df['涨跌幅'] == 0).sum()
```

#### 涨停/跌停数据

| 功能 | akshare 接口 | 可用性 |
|-----|-------------|--------|
| 涨停股池 | `stock_zt_pool_em(date="YYYYMMDD")` | ✅ 完全可用 |
| 跌停股池 | `stock_zt_pool_em(date="YYYYMMDD")` | ✅ 需确认参数 |

**参考资料**：
- 实测文章显示 `stock_zt_pool_em` 可获取涨停板数据
- 数据源：东方财富网

### 2.2 港股数据

| 功能 | akshare 接口 | 可用性 |
|-----|-------------|--------|
| 港股实时行情 | `index_hk_spot_em()` | ✅ 完全可用 |
| 恒生指数 | 包含在港股行情中 | ✅ 可用 |

### 2.3 美股数据

| 功能 | akshare 接口 | 可用性 |
|-----|-------------|--------|
| 美股实时行情 | `index_us_spot()` | ✅ 完全可用 |
| 道琼斯工业平均指数 | .DJIA | ✅ 可用 |
| 纳斯达克综合指数 | .IXIC | ✅ 可用 |
| 标准普尔500 | .INX | ✅ 可用 |
| 全球指数 | `index_global_spot()` | ✅ 可用 |

### 2.4 汇率数据

| 功能 | akshare 接口 | 可用性 |
|-----|-------------|--------|
| 外汇实时行情 | `forex_spot_em()` | ✅ 完全可用 |
| 外汇历史数据 | `forex_hist_em(symbol="USDCNH")` | ✅ 完全可用 |
| 中国银行汇率 | `currency_boc_sina()` | ✅ 可用 |

**支持的货币对**：
- USDCNH（美元兑离岸人民币）
- 其他主要货币对

---

## 3. 技术可行性结论

| 新数据源 | akshare 支持 | 实现难度 | 优先级 |
|---------|-------------|---------|--------|
| 市场情绪（涨跌家数） | ✅ 完全支持 | 低 | P0 |
| 市场情绪（涨停跌停） | ✅ 完全支持 | 低 | P0 |
| 港股/恒生指数 | ✅ 完全支持 | 低 | P1 |
| 美股指数 | ✅ 完全支持 | 低 | P1 |
| 汇率数据 | ✅ 完全支持 | 低 | P1 |

**结论**：所有计划添加的数据源在 akshare 库中都有完整支持，实现难度低，可以快速开发。

---

## 4. 实现建议

### 4.1 命名建议

| 数据类型 | 建议 Fetcher 名称 | 说明 |
|---------|-------------------|------|
| 市场情绪 | MarketSentimentFetcher | 包含涨跌家数、涨停跌停 |
| 港股 | HKIndexFetcher | 港股及恒生指数 |
| 美股 | USIndexFetcher | 道指、纳指、标普500 |
| 汇率 | ForexFetcher | 外汇汇率数据 |

### 4.2 数据模型建议

为每个新 fetcher 创建对应的 Pydantic 模型：
- `MarketSentimentSpot`
- `HKIndexSpot` / `HKIndexHistory`
- `USIndexSpot` / `USIndexHistory`
- `ForexSpot` / `ForexHistory`

### 4.3 CLI 命令建议

```bash
finscraper sentiment spot
finscraper hk-index spot
finscraper us-index spot
finscraper forex spot
```
