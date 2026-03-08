# FinScraper 用户教程

> 本教程将帮助您快速上手 FinScraper，掌握从安装到高级使用的所有功能。

---

## 目录

1. [简介](#1-简介)
2. [功能概览](#2-功能概览)
3. [安装](#3-安装)
4. [快速入门](#4-快速入门)
5. [CLI 命令详解](#5-cli-命令详解)
6. [Python API 使用](#6-python-api-使用)
7. [数据存储](#7-数据存储)
8. [配置选项](#8-配置选项)
9. [常见问题](#9-常见问题)

---

## 1. 简介

FinScraper 是一个基于 akshare 的专业金融数据获取工具，提供以下核心功能：

- **6 大数据类型**：A 股指数、北向资金、板块数据、大宗商品、资金流向、重要新闻
- **2 种使用方式**：命令行工具 (CLI) 和 Python API
- **4 种存储格式**：CSV、JSON、Parquet、SQLite
- **完善的错误处理**：自动重试、详细日志

### 适用场景

- 📊 量化分析：获取历史数据进行策略回测
- 📈 市场监控：实时监控指数、资金流向
- 📰 资讯收集：自动获取财经新闻和公告
- 💾 数据归档：定期备份金融数据

---

## 2. 功能概览

> 本章详细介绍 FinScraper 的核心功能、数据类型及其为用户提供的价值。

### 2.1 产品定位

FinScraper 是一款专业的金融数据获取工具，专注于为量化分析师、金融研究员、个人投资者提供高质量、多维度、易获取的 A 股市场数据。

#### 核心价值主张

| 维度 | 价值 |
|-----|------|
| **数据广度** | 覆盖 A 股市场 6 大核心数据类型 |
| **获取便捷** | 一行命令即可获取所需数据 |
| **格式灵活** | 支持多种数据格式，适配不同分析工具 |
| **使用灵活** | CLI 工具 + Python API，满足各类使用场景 |

### 2.2 核心能力

#### 数据获取能力

FinScraper 提供 10 大类金融数据的获取能力：

```
┌─────────────────────────────────────────────────────────┐
│                    FinScraper 数据矩阵                    │
├─────────────┬─────────────┬─────────────┬───────────────┤
│  A 股指数   │  北向资金   │  板块数据   │  大宗商品    │
├─────────────┼─────────────┼─────────────┼───────────────┤
│  资金流向   │  重要新闻   │  市场情绪   │  港股指数    │
├─────────────┼─────────────┼─────────────┼───────────────┤
│  美股指数   │  汇率数据   │             │              │
└─────────────┴─────────────┴─────────────┴───────────────┘
```

#### 数据时效性

| 数据类型 | 实时性 | 更新频率 | 数据价值 |
|---------|-------|---------|---------|
| A 股指数 | 实时 | 分钟级 | 市场走势监控 |
| 北向资金 | 实时 | 分钟级 | 外资动向追踪 |
| 板块数据 | 实时 | 分钟级 | 热点板块发现 |
| 大宗商品 | 实时 | 分钟级 | 商品期货分析 |
| 资金流向 | 日频 | 日更新 | 主力资金追踪 |
| 重要新闻 | 实时 | 即时 | 资讯驱动决策 |
| 市场情绪 | 实时 | 分钟级 | 市场温度感知 |
| 港股指数 | 实时 | 分钟级 | 港股走势监控 |
| 美股指数 | 实时 | 分钟级 | 全球市场参考 |
| 汇率数据 | 实时 | 分钟级 | 汇率走势分析 |

### 2.3 数据类型详解

#### A 股指数数据

**功能描述**

提供主要 A 股指数的实时行情和历史数据，包括：
- 上证指数、深证成指、创业板指
- 沪深300、上证50、中证500
- 科创板指数、北证50等

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 指数代码 | 唯一标识 | 数据关联 |
| 指数名称 | 中文名称 | 展示识别 |
| 最新价 | 当前点位 | 实时监控 |
| 涨跌额 | 绝对变化 | 波动分析 |
| 涨跌幅 | 百分比变化 | 趋势判断 |
| 成交量 | 成交股数 | 流动性分析 |
| 成交额 | 成交金额 | 活跃度评估 |

**用户价值**

- 📊 **市场监控**：实时掌握大盘走势
- 📈 **技术分析**：获取历史数据进行趋势分析
- 📉 **风险评估**：通过波动率评估市场风险
- 📊 **策略回测**：获取历史数据验证交易策略

#### 北向资金数据

**功能描述**

追踪沪深港通资金流向，反映外资对 A 股的投资态度：
- 沪股通、深股通资金流向
- 日级别和日内级别数据
- 净流入、净买入、余额等指标

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 日期 | 交易日期 | 时间序列分析 |
| 沪股通流入 | 上海市场流入额 | 分市场分析 |
| 深股通流入 | 深圳市场流入额 | 分市场分析 |
| 北向净流入 | 合计净流入 | 整体外资态度 |
| 当日余额 | 剩余额度 | 热度指标 |

**用户价值**

- 🌍 **外资动向**：追踪国际资本对 A 股的配置
- 📊 **市场情绪**：北向资金常被视为"聪明钱"
- 📈 **择时参考**：大额流入往往预示市场机会
- 📉 **风险预警**：持续流出可能预示调整

#### 板块数据

**功能描述**

提供行业板块和概念板块的全面数据：
- 板块列表和分类
- 板块实时行情（涨跌幅、领涨股等）
- 板块成分股明细

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 板块代码 | 唯一标识 | 数据关联 |
| 板块名称 | 中文名称 | 展示识别 |
| 涨跌幅 | 整体表现 | 热点发现 |
| 领涨股 | 涨幅最大个股 | 龙头识别 |
| 领跌股 | 跌幅最大个股 | 风险识别 |
| 成交额 | 板块成交 | 活跃度评估 |
| 换手率 | 换手比例 | 热度指标 |

**用户价值**

- 🔥 **热点发现**：识别市场热点板块
- 📊 **行业配置**：行业轮动策略分析
- 🎯 **个股筛选**：在强势板块中选龙头
- 📈 **趋势跟踪**：板块趋势持续性分析

#### 大宗商品数据

**功能描述**

提供黄金、白银、原油、铜等主要商品的价格数据：
- 商品实时行情
- 历史价格数据
- 多周期支持（日/周/月）

**覆盖品种**

| 品种 | 代码 | 说明 |
|-----|------|------|
| 黄金 | AU0 | 贵金属标杆 |
| 白银 | AG0 | 贵金属 |
| 铜 | CU0 | 工业金属 |
| 铝 | AL0 | 工业金属 |
| 原油 | SC0 | 能源商品 |
| 螺纹钢 | RB0 | 建材商品 |

**用户价值**

- 💰 **资产配置**：商品与股票的相关性分析
- 📊 **通胀对冲**：商品作为通胀保护工具
- 🌍 **宏观分析**：商品价格反映经济周期
- 📈 **跨市场策略**：商品与股市的联动交易

#### 资金流向数据

**功能描述**

提供个股、板块、市场三个层面的资金流向数据：
- 主力资金净流入/流出
- 超大单、大单、中单、小单分类
- 资金占比分析

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 主力净流入 | 大单资金净额 | 主力动向 |
| 超大单流入 | 超大单买入 | 机构行为 |
| 大单流入 | 大单买入 | 大资金动向 |
| 中单流入 | 中单买入 | 中户行为 |
| 小单流入 | 小单买入 | 散户行为 |
| 净占比 | 净流入占比 | 强度评估 |

**用户价值**

- 🎯 **主力追踪**：识别主力资金动向
- 📊 **筹码分析**：了解市场参与者结构
- 📈 **选股参考**：资金持续流入的个股
- 📉 **风险识别**：资金大幅流出的预警

#### 重要新闻数据

**功能描述**

提供多维度财经新闻和资讯：
- 全球财经新闻
- A 股公告和快讯
- 个股相关新闻

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 标题 | 新闻标题 | 快速浏览 |
| 内容 | 新闻正文 | 深度阅读 |
| 发布时间 | 时间戳 | 时效性评估 |
| 来源 | 信息来源 | 可信度评估 |
| 相关股票 | 关联个股 | 事件驱动分析 |

**用户价值**

- 📰 **资讯获取**：及时获取市场重要信息
- 📊 **事件驱动**：基于新闻的事件驱动策略
- 🔔 **风险预警**：负面新闻及时提醒
- 📈 **机会发现**：利好消息带来的交易机会

#### 市场情绪数据

**功能描述**

提供全面的市场情绪指标，感知市场温度：
- 涨跌家数统计
- 涨停/跌停股票列表
- 综合市场情绪指数

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 上涨家数 | 涨幅 > 0 的股票数量 | 市场热度 |
| 下跌家数 | 跌幅 < 0 的股票数量 | 市场恐慌 |
| 平盘家数 | 涨跌幅 = 0 的股票数量 | 观望情绪 |
| 涨停家数 | 涨停股票数量 | 赚钱效应 |
| 跌停家数 | 跌停股票数量 | 风险释放 |

**用户价值**

- 🌡️ **市场温度**：直观感知市场整体情绪
- 📊 **情绪周期**：识别情绪的高点和低点
- 🎯 **交易择时**：情绪极值常伴随反转机会
- ⚠️ **风险预警**：大面积跌停时谨慎操作

#### 港股指数数据

**功能描述**

提供港股主要指数的实时行情和历史数据：
- 恒生指数
- 恒生科技指数
- 恒生国企指数
- 其他港股主要指数

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 指数代码 | 唯一标识 | 数据关联 |
| 指数名称 | 中文名称 | 展示识别 |
| 最新价 | 当前点位 | 实时监控 |
| 涨跌额 | 绝对变化 | 波动分析 |
| 涨跌幅 | 百分比变化 | 趋势判断 |
| 成交量 | 成交股数 | 流动性分析 |
| 成交额 | 成交金额 | 活跃度评估 |

**用户价值**

- 🌍 **跨市场分析**：A 股与港股联动分析
- 📈 **港股投资**：港股走势监控
- 🔗 **互联互通**：沪深港通相关分析
- 📊 **估值对比**：A/H 股溢价分析

#### 美股指数数据

**功能描述**

提供美股主要指数的实时行情和历史数据：
- 道琼斯工业平均指数
- 纳斯达克综合指数
- 标准普尔 500 指数
- 全球主要指数

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 指数代码 | 唯一标识 | 数据关联 |
| 指数名称 | 中文名称 | 展示识别 |
| 最新价 | 当前点位 | 实时监控 |
| 涨跌额 | 绝对变化 | 波动分析 |
| 涨跌幅 | 百分比变化 | 趋势判断 |
| 成交量 | 成交股数 | 流动性分析 |
| 成交额 | 成交金额 | 活跃度评估 |

**用户价值**

- 🌐 **全球视角**：美股作为全球市场风向标
- 📈 **外盘参考**：美股走势影响 A 股开盘
- 🔗 **跨市场联动**：中美股市关联性分析
- 📊 **宏观参考**：美股反映全球经济状况

#### 汇率数据

**功能描述**

提供主要货币对的实时汇率和历史数据：
- 美元兑人民币（USD/CNY）
- 美元兑离岸人民币（USD/CNH）
- 欧元、日元、港币等主要货币
- 多周期历史数据

**数据字段**

| 字段 | 说明 | 应用场景 |
|-----|------|---------|
| 货币对代码 | 唯一标识 | 数据关联 |
| 货币对名称 | 中文名称 | 展示识别 |
| 最新价 | 当前汇率 | 实时监控 |
| 涨跌额 | 绝对变化 | 波动分析 |
| 涨跌幅 | 百分比变化 | 趋势判断 |
| 最高价 | 时段最高 | 波动分析 |
| 最低价 | 时段最低 | 波动分析 |

**用户价值**

- 💱 **汇率监控**：实时关注汇率走势
- 🌍 **外贸分析**：进出口企业汇率风险管理
- 📊 **宏观分析**：汇率反映经济基本面
- 🔗 **资产配置**：汇率影响跨境资产配置

### 2.4 适用场景与价值

#### 量化分析

**场景描述**：量化分析师需要大量历史数据进行策略回测和模型训练。

**FinScraper 提供的价值**：
- 📊 **历史数据**：获取多品种、多维度的历史数据
- 🔄 **数据更新**：定期更新数据，保持策略时效性
- 📈 **多因子**：指数、资金流向、板块等多因子数据
- 💾 **格式灵活**：支持 Parquet 等高效格式，适合大数据处理

#### 市场监控

**场景描述**：投资者需要实时监控市场动态，及时发现机会和风险。

**FinScraper 提供的价值**：
- ⚡ **实时数据**：分钟级更新的实时行情
- 🔔 **多维度**：指数、板块、资金流向同时监控
- 📊 **可视化**：数据可导出到 Grafana 等监控工具
- 🔄 **自动化**：定时任务自动获取和更新

#### 资讯收集

**场景描述**：研究员需要收集和整理财经新闻，进行舆情分析。

**FinScraper 提供的价值**：
- 📰 **全面覆盖**：全球新闻、公告、个股新闻
- ⏰ **实时获取**：新闻发布后即时获取
- 🔍 **精准筛选**：按个股、板块筛选相关新闻
- 💾 **结构化存储**：便于后续的 NLP 分析

#### 数据归档

**场景描述**：机构需要定期备份金融数据，建立数据资产。

**FinScraper 提供的价值**：
- 📦 **批量获取**：一键获取多类型数据
- 💾 **可靠存储**：支持多种格式，便于长期保存
- 🔄 **增量更新**：支持增量更新，节省资源
- 📊 **数据完整性**：自动重试确保数据完整

---

## 3. 安装

### 系统要求

- Python 3.10+
- Windows / macOS / Linux

### 安装步骤

```bash
# 克隆项目（或下载源码）
git clone <repository-url>
cd FinScraper

# 创建虚拟环境（推荐）
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 安装项目
pip install -e .

# 验证安装
finscraper --version
```

### 开发模式安装

如需开发或运行测试：

```bash
pip install -e ".[dev]"
```

---

## 4. 快速入门

### 4.1 第一个命令

获取 A 股指数实时行情：

```bash
finscraper index spot
```

输出示例：
```
代码      名称           最新价     涨跌额    涨跌幅
--------  -----------  -------  -------  -------
sh000001  上证指数      3050.23    12.45     0.41
sz399001  深证成指      9850.12    45.67     0.47
sz399006  创业板指      1980.56    15.23     0.78
```

### 4.2 保存数据到文件

```bash
# 保存为 CSV（默认）
finscraper index spot --output-path data/indices.csv

# 保存为 JSON
finscraper index spot -o json -p data/indices.json

# 保存为 Parquet（适合大数据）
finscraper index spot -o parquet -p data/indices.parquet

# 保存到 SQLite 数据库
finscraper index spot -o sqlite -p data/finance.db
```

### 4.3 获取历史数据

```bash
# 获取上证指数历史数据
finscraper index history 000001 \
  --start-date 20240101 \
  --end-date 20241231
```

---

## 5. CLI 命令详解

### 5.1 全局选项

所有命令都支持以下全局选项：

| 选项 | 简写 | 说明 | 示例 |
|-----|------|------|------|
| `--version` | `-V` | 显示版本 | `finscraper -V` |
| `--verbose` | `-v` | 详细日志（可叠加） | `finscraper -v index spot` |
| `--quiet` | `-q` | 安静模式（只显示错误） | `finscraper -q index spot` |
| `--config` | `-c` | 指定配置文件 | `finscraper -c config.yaml index spot` |

**日志级别说明：**
- 默认：WARNING 级别
- `-v`：INFO 级别（显示进度信息）
- `-vv`：DEBUG 级别（显示详细调试信息）

### 5.2 指数命令 (index)

#### 列出所有指数

```bash
# 表格格式（默认）
finscraper index list

# JSON 格式
finscraper index list --format json
finscraper index list -f json
```

#### 获取实时行情

```bash
# 获取所有指数
finscraper index spot

# 获取指定指数
finscraper index spot --symbols sh000001,sz399001
finscraper index spot -s sh000001

# 保存到文件
finscraper index spot -p data/spot.csv
```

#### 获取历史数据

```bash
# 基本用法
finscraper index history 000001

# 指定日期范围
finscraper index history 000001 \
  --start-date 20240101 \
  --end-date 20241231

# 指定周期
finscraper index history 000001 --period daily    # 日线（默认）
finscraper index history 000001 --period weekly   # 周线
finscraper index history 000001 --period monthly  # 月线

# 保存到文件
finscraper index history 000001 -p data/sh000001_history.csv
```

**常用指数代码：**
- `000001` - 上证指数
- `399001` - 深证成指
- `399006` - 创业板指
- `000300` - 沪深300
- `000016` - 上证50
- `000905` - 中证500

### 5.3 北向资金命令 (north-flow)

北向资金（沪深港通）反映外资对 A 股的投资动向。

#### 获取日数据

```bash
# 获取最近 20 个交易日的北向资金数据
finscraper north-flow daily

# 保存到文件
finscraper north-flow daily -p data/north_flow_daily.csv
```

数据字段说明：
- 沪股通流入/流出
- 深股通流入/流出
- 北向资金净流入
- 当日余额

#### 获取日内数据

```bash
# 获取当日实时北向资金流向
finscraper north-flow intraday

# 保存到文件
finscraper north-flow intraday -p data/north_flow_intraday.csv
```

### 5.4 板块命令 (sector)

#### 获取板块列表和行情

```bash
# 获取板块实时行情（包含板块列表）
finscraper sector spot

# 保存到文件
finscraper sector spot -p data/sectors.csv
```

数据包含：
- 板块名称、代码
- 涨跌幅、涨跌额
- 领涨股、领跌股
- 成交额、换手率

#### 获取板块成分股

```bash
# 获取指定板块的成分股
finscraper sector stocks <板块代码>

# 示例
finscraper sector stocks BK0428
```

### 5.5 大宗商品命令 (commodity)

#### 列出所有商品

```bash
# 表格格式
finscraper commodity list

# JSON 格式
finscraper commodity list -f json
```

#### 获取实时行情

```bash
# 获取所有商品实时行情
finscraper commodity spot

# 保存到文件
finscraper commodity spot -p data/commodities.csv
```

#### 获取历史数据

```bash
# 基本用法
finscraper commodity history AU0

# 指定日期范围
finscraper commodity history AU0 \
  --start-date 20240101 \
  --end-date 20241231

# 指定周期
finscraper commodity history AU0 --period daily
```

**常用商品代码：**
- `AU0` - 黄金
- `AG0` - 白银
- `CU0` - 铜
- `AL0` - 铝
- `ZN0` - 锌
- `NI0` - 镍
- `RB0` - 螺纹钢
- `SC0` - 原油

### 5.6 资金流向命令 (money-flow)

#### 个股资金流向

```bash
# 获取个股资金流向排名
finscraper money-flow stock

# 保存到文件
finscraper money-flow stock -p data/stock_money_flow.csv
```

数据包含：
- 主力净流入/流出
- 超大单、大单、中单、小单流向
- 净占比

#### 板块资金流向

```bash
# 获取板块资金流向
finscraper money-flow sector

# 保存到文件
finscraper money-flow sector -p data/sector_money_flow.csv
```

#### 市场资金流向

```bash
# 获取两市整体资金流向
finscraper money-flow market

# 保存到文件
finscraper money-flow market -p data/market_money_flow.csv
```

### 5.7 新闻命令 (news)

#### 获取全球财经新闻

```bash
# 获取全球财经资讯
finscraper news global

# 保存到文件
finscraper news global -p data/global_news.csv
```

#### 获取新闻快讯

```bash
# 获取 A 股公告和快讯
finscraper news alert

# 保存到文件
finscraper news alert -p data/news_alert.csv
```

#### 获取个股新闻

```bash
# 获取指定个股的新闻
finscraper news stock 000001

# 保存到文件
finscraper news stock 000001 -p data/stock_000001_news.csv
```

#### 专题新闻筛选

FinScraper 支持按特定主题筛选新闻，帮助你快速获取关注领域的资讯。

##### 列出所有可用专题

```bash
finscraper news topics
```

##### 获取指定专题的新闻

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

##### Python API 使用

```python
from finscraper.filters import TopicFilter
import akshare as ak

# 获取新闻数据
df = ak.stock_info_global_em()

# 创建筛选器
filter = TopicFilter()

# 列出可用专题
topics = filter.list_topics()
print(topics)  # ['中东地缘', '全国两会', '美联储', ...]

# 筛选专题新闻
filtered_df = filter.filter_by_topic(df, topic="中东地缘")

# 获取 URL 列表
urls = filter.get_topic_urls(df, topic="中东地缘")
```

##### 内置专题

- **中东地缘**: 中东地区相关新闻（以色列、巴勒斯坦、伊朗、沙特等）
- **全国两会**: 全国人大、政协相关新闻
- **美联储**: 美联储货币政策相关新闻
- **人工智能**: AI、大模型相关新闻
- **新能源**: 光伏、风电、电动车等相关新闻
- **房地产**: 房地产行业相关新闻

### 5.7 市场情绪命令 (`sentiment`)

获取市场情绪相关数据，包括涨跌家数、涨停跌停等。

```bash
# 查看帮助
finscraper sentiment --help
```

##### 获取综合市场情绪数据

```bash
# 获取综合市场情绪数据（涨跌家数、涨停跌停等）
finscraper sentiment spot

# 保存到文件
finscraper sentiment spot --output csv --output-path sentiment.csv
```

##### 获取涨跌家数数据

```bash
# 获取所有A股实时行情数据（用于统计涨跌家数）
finscraper sentiment up-down

# 保存到文件
finscraper sentiment up-down -p up_down.csv
```

##### 获取涨停股票列表

```bash
# 获取今日涨停股票
finscraper sentiment limit-up

# 获取指定日期涨停股票
finscraper sentiment limit-up --date 20250308

# 保存到文件
finscraper sentiment limit-up -p limit_up.csv
```

##### 获取跌停股票列表

```bash
# 获取今日跌停股票
finscraper sentiment limit-down

# 获取指定日期跌停股票
finscraper sentiment limit-down --date 20250308

# 保存到文件
finscraper sentiment limit-down -p limit_down.csv
```

##### Python API 使用

```python
from finscraper.fetchers import MarketSentimentFetcher

fetcher = MarketSentimentFetcher()

# 获取综合市场情绪数据
sentiment = fetcher.fetch_sentiment()
print(sentiment)

# 获取所有A股数据
all_stocks = fetcher.fetch_up_down_count()
print(f"上涨: {(all_stocks['change_percent'] > 0).sum()}")
print(f"下跌: {(all_stocks['change_percent'] < 0).sum()}")

# 获取涨停股票
limit_up = fetcher.fetch_limit_up()
print(f"涨停数: {len(limit_up)}")

# 获取跌停股票
limit_down = fetcher.fetch_limit_down()
print(f"跌停数: {len(limit_down)}")
```

### 5.8 港股命令 (`hk`)

获取港股/恒生指数相关数据。

```bash
# 查看帮助
finscraper hk --help
```

##### 获取港股指数实时行情

```bash
# 获取港股指数实时行情
finscraper hk spot

# 保存到文件
finscraper hk spot --output csv --output-path hk_indices.csv
```

##### Python API 使用

```python
from finscraper.fetchers import HKIndexFetcher

fetcher = HKIndexFetcher()

# 获取港股指数实时行情
hk_data = fetcher.fetch_spot()
print(hk_data[hk_data['name'].str.contains('恒生')])
```

### 5.9 美股命令 (`us`)

获取美股指数相关数据。

```bash
# 查看帮助
finscraper us --help
```

##### 获取美股指数实时行情

```bash
# 获取美股指数实时行情（道指、纳指、标普500）
finscraper us spot

# 保存到文件
finscraper us spot --output csv --output-path us_indices.csv
```

##### 获取全球指数实时行情

```bash
# 获取全球指数实时行情
finscraper us global

# 保存到文件
finscraper us global -p global_indices.csv
```

##### Python API 使用

```python
from finscraper.fetchers import USIndexFetcher

fetcher = USIndexFetcher()

# 获取美股指数实时行情
us_data = fetcher.fetch_spot()
print(us_data)

# 获取全球指数实时行情
global_data = fetcher.fetch_global()
print(global_data)
```

### 5.10 汇率命令 (`fx`)

获取汇率相关数据。

```bash
# 查看帮助
finscraper fx --help
```

##### 获取汇率实时行情

```bash
# 获取汇率实时行情
finscraper fx spot

# 保存到文件
finscraper fx spot --output csv --output-path forex.csv
```

##### 获取汇率历史数据

```bash
# 获取美元兑离岸人民币历史数据（默认近一年）
finscraper fx history USDCNH

# 指定日期范围
finscraper fx history USDCNH --start-date 20240101 --end-date 20241231

# 保存到文件
finscraper fx history USDCNH -p usdcnh_history.csv
```

##### Python API 使用

```python
from finscraper.fetchers import ForexFetcher

fetcher = ForexFetcher()

# 获取汇率实时行情
fx_data = fetcher.fetch_spot()
print(fx_data[fx_data['symbol'] == 'USDCNH'])

# 获取汇率历史数据
history = fetcher.fetch_history(
    symbol="USDCNH",
    start_date="20240101",
    end_date="20241231",
)
print(history.head())
```

### 5.11 输出格式选项

#### 屏幕输出格式

```bash
# 表格格式（默认）
finscraper index list --format table

# JSON 格式
finscraper index list --format json
finscraper index list -f json
```

**注意：** 只有 `index list` 和 `commodity list` 命令支持 `--format` 选项。

#### 文件保存格式

```bash
# CSV 格式（默认）
finscraper index spot --output csv -p data/spot.csv

# JSON 格式
finscraper index spot --output json -p data/spot.json
finscraper index spot -o json -p data/spot.json

# Parquet 格式（适合大数据）
finscraper index spot -o parquet -p data/spot.parquet

# SQLite 格式
finscraper index spot -o sqlite -p data/finance.db
```

### 5.9 实用技巧

#### 组合使用示例

```bash
# 获取指数数据并保存为 JSON
finscraper index spot -o json -p data/indices.json

# 详细日志模式获取数据
finscraper -vv index history 000001 --start-date 20240101

# 安静模式运行（适合脚本）
finscraper -q north-flow daily -p data/north.csv
```

#### 批量获取数据

```bash
# 创建数据目录
mkdir -p data/$(date +%Y%m%d)

# 批量获取各类数据（传统数据源）
finscraper index spot -p data/$(date +%Y%m%d)/indices.csv
finscraper north-flow daily -p data/$(date +%Y%m%d)/north_flow.csv
finscraper sector spot -p data/$(date +%Y%m%d)/sectors.csv
finscraper commodity spot -p data/$(date +%Y%m%d)/commodities.csv

# 批量获取新增数据源
finscraper sentiment spot -p data/$(date +%Y%m%d)/sentiment.csv
finscraper hk spot -p data/$(date +%Y%m%d)/hk_indices.csv
finscraper us spot -p data/$(date +%Y%m%d)/us_indices.csv
finscraper fx spot -p data/$(date +%Y%m%d)/forex.csv
```

---

## 6. Python API 使用

FinScraper 提供简洁的 Python API，方便在代码中集成。

### 6.1 基础用法

```python
from finscraper.fetchers import IndexFetcher

# 创建获取器
fetcher = IndexFetcher()

# 获取数据
data = fetcher.fetch_spot()
print(data.head())
```

### 6.2 各数据类型 API

#### A 股指数

```python
from finscraper.fetchers import IndexFetcher

fetcher = IndexFetcher()

# 获取实时行情
spot_data = fetcher.fetch_spot()

# 获取历史数据
history_data = fetcher.fetch_history(
    symbol="000001",
    start_date="20240101",
    end_date="20241231",
    period="daily"  # daily, weekly, monthly
)
```

#### 北向资金

```python
from finscraper.fetchers import NorthFlowFetcher

fetcher = NorthFlowFetcher()

# 获取日数据
daily_data = fetcher.fetch_daily()

# 获取日内数据
intraday_data = fetcher.fetch_intraday()
```

#### 板块数据

```python
from finscraper.fetchers import SectorFetcher

fetcher = SectorFetcher()

# 获取板块列表
sector_list = fetcher.fetch_list()

# 获取板块实时行情
spot_data = fetcher.fetch_spot()

# 获取板块成分股
stocks = fetcher.fetch_stocks("BK0428")
```

#### 大宗商品

```python
from finscraper.fetchers import CommodityFetcher

fetcher = CommodityFetcher()

# 获取实时行情
spot_data = fetcher.fetch_spot()

# 获取历史数据
history_data = fetcher.fetch_history(
    symbol="AU0",
    start_date="20240101",
    end_date="20241231"
)
```

#### 资金流向

```python
from finscraper.fetchers import MoneyFlowFetcher

fetcher = MoneyFlowFetcher()

# 个股资金流向
stock_flow = fetcher.fetch_stock()

# 板块资金流向
sector_flow = fetcher.fetch_sector()

# 市场资金流向
market_flow = fetcher.fetch_market()
```

#### 新闻数据

```python
from finscraper.fetchers import NewsFetcher

fetcher = NewsFetcher()

# 全球新闻
global_news = fetcher.fetch_global()

# 新闻快讯
alerts = fetcher.fetch_alert()

# 个股新闻
stock_news = fetcher.fetch_stock("000001")
```

#### 市场情绪

```python
from finscraper.fetchers import MarketSentimentFetcher

fetcher = MarketSentimentFetcher()

# 获取综合市场情绪数据
sentiment = fetcher.fetch_sentiment()
print(sentiment)

# 获取所有A股数据
all_stocks = fetcher.fetch_up_down_count()
print(f"上涨: {(all_stocks['change_percent'] > 0).sum()}")
print(f"下跌: {(all_stocks['change_percent'] < 0).sum()}")

# 获取涨停股票
limit_up = fetcher.fetch_limit_up()
print(f"涨停数: {len(limit_up)}")

# 获取跌停股票
limit_down = fetcher.fetch_limit_down()
print(f"跌停数: {len(limit_down)}")
```

#### 港股指数

```python
from finscraper.fetchers import HKIndexFetcher

fetcher = HKIndexFetcher()

# 获取港股指数实时行情
hk_data = fetcher.fetch_spot()
print(hk_data[hk_data['name'].str.contains('恒生')])
```

#### 美股指数

```python
from finscraper.fetchers import USIndexFetcher

fetcher = USIndexFetcher()

# 获取美股指数实时行情
us_data = fetcher.fetch_spot()
print(us_data)

# 获取全球指数实时行情
global_data = fetcher.fetch_global()
print(global_data)
```

#### 汇率数据

```python
from finscraper.fetchers import ForexFetcher

fetcher = ForexFetcher()

# 获取汇率实时行情
fx_data = fetcher.fetch_spot()
print(fx_data[fx_data['symbol'] == 'USDCNH'])

# 获取汇率历史数据
history = fetcher.fetch_history(
    symbol="USDCNH",
    start_date="20240101",
    end_date="20241231",
)
print(history.head())
```

### 6.3 在代码中保存数据

```python
from finscraper.fetchers import IndexFetcher
from finscraper.storage.csv_storage import CSVStorage
from finscraper.storage.json_storage import JSONStorage

# 获取数据
fetcher = IndexFetcher()
data = fetcher.fetch_spot()

# 保存为 CSV
storage = CSVStorage()
storage.save(data, "data/indices.csv")

# 保存为 JSON
json_storage = JSONStorage()
json_storage.save(data, "data/indices.json")

# 从文件加载
loaded_data = storage.load("data/indices.csv")
```

### 6.4 错误处理

```python
from finscraper.fetchers import IndexFetcher
from finscraper.core.exceptions import NetworkError, DataError

fetcher = IndexFetcher()

try:
    data = fetcher.fetch_spot()
    print(data)
except NetworkError as e:
    print(f"网络错误: {e}")
except DataError as e:
    print(f"数据错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 7. 数据存储

### 7.1 存储格式对比

| 格式 | 优点 | 缺点 | 适用场景 |
|-----|------|------|---------|
| CSV | 通用、易读 | 无类型、大文件慢 | 小数据、人工查看 |
| JSON | 结构化、易解析 | 文件大 | API 接口、配置文件 |
| Parquet | 压缩率高、查询快 | 需专用库 | 大数据、分析 |
| SQLite | 关系型、支持 SQL | 需 SQL 知识 | 复杂查询、多表关联 |

### 7.2 存储路径

默认数据存储在项目根目录的 `data/` 文件夹下：

```
data/
├── indices/
│   ├── spot.csv
│   └── history/
├── north_flow/
│   ├── daily.csv
│   └── intraday.csv
├── sectors/
├── commodities/
├── money_flow/
└── news/
```

可以通过配置修改数据目录：

```bash
# 环境变量
export FINSCRAPER_DATA_DIR="/path/to/data"

# 或配置文件
# config.yaml
data_dir: "/path/to/data"
```

---

## 8. 配置选项

### 8.1 环境变量配置

所有配置项都可以通过 `FINSCRAPER_` 前缀的环境变量设置：

```bash
# 设置超时时间（秒）
export FINSCRAPER_REQUEST_TIMEOUT=60

# 设置最大重试次数
export FINSCRAPER_MAX_RETRIES=5

# 设置日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
export FINSCRAPER_LOG_LEVEL=DEBUG

# 设置数据目录
export FINSCRAPER_DATA_DIR="/path/to/data"

# 设置日志文件路径
export FINSCRAPER_LOG_FILE="/path/to/logs/finscraper.log"
```

### 8.2 配置文件

创建 `config.yaml` 文件：

```yaml
# 请求超时时间（秒）
request_timeout: 60

# 最大重试次数
max_retries: 5

# 请求 User-Agent
user_agent: "FinScraper/1.0.0"

# 数据存储目录
data_dir: "data"

# 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
log_level: "INFO"

# 日志文件路径
log_file: "logs/finscraper.log"
```

使用配置文件：

```bash
finscraper -c config.yaml index spot
```

### 8.3 配置优先级

配置优先级从高到低：

1. 命令行参数
2. 环境变量
3. 配置文件
4. 默认值

---

## 9. 常见问题

### Q1: 安装失败怎么办？

**A:** 确保 Python 版本 >= 3.10，并尝试以下步骤：

```bash
# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -e .

# 如果仍失败，尝试单独安装 akshare
pip install akshare
```

### Q2: 获取数据时超时？

**A:** 增加超时时间：

```bash
# 环境变量方式
export FINSCRAPER_REQUEST_TIMEOUT=60

# 或配置文件方式
# config.yaml
request_timeout: 60
```

### Q3: 如何查看详细日志？

**A:** 使用 `-v` 或 `-vv` 选项：

```bash
# INFO 级别
finscraper -v index spot

# DEBUG 级别
finscraper -vv index spot
```

### Q4: 数据保存到哪里了？

**A:** 默认保存到当前目录的 `data/` 文件夹。可以通过 `--output-path` 指定完整路径：

```bash
finscraper index spot -p /full/path/to/file.csv
```

### Q5: 如何定期自动获取数据？

**A:** 使用系统的定时任务功能：

**Linux/macOS (crontab):**
```bash
# 每天 15:30 获取数据
30 15 * * * cd /path/to/FinScraper && finscraper -q index spot -p data/$(date +\%Y\%m\%d)/indices.csv
```

**Windows (任务计划程序):**
创建批处理文件 `fetch_data.bat`：
```batch
@echo off
cd /d D:\Code\FinScraper
finscraper -q index spot -p data\%date:~0,4%%date:~5,2%%date:~8,2%\indices.csv
```

### Q6: 如何获取特定股票的数据？

**A:** 使用 `news` 命令获取个股新闻：

```bash
finscraper news stock 000001
```

个股的历史行情数据可以通过指数命令获取（个股代码作为 symbol）：

```bash
finscraper index history 000001
```

### Q7: 数据更新频率是多少？

**A:** 数据更新频率取决于 akshare 数据源：

- 实时行情：每分钟更新
- 日数据：收盘后更新
- 历史数据：固定不变

### Q8: 如何处理网络错误？

**A:** FinScraper 内置了自动重试机制。如需调整：

```yaml
# config.yaml
max_retries: 5      # 增加重试次数
request_timeout: 60  # 增加超时时间
```

---

## 9. 最佳实践

### 10.1 数据组织

按日期组织数据文件：

```bash
# 创建日期目录
DATE=$(date +%Y%m%d)
mkdir -p data/$DATE

# 获取各类数据
finscraper index spot -p data/$DATE/indices.csv
finscraper north-flow daily -p data/$DATE/north_flow.csv
finscraper sector spot -p data/$DATE/sectors.csv
```

### 10.2 日志管理

定期清理日志文件：

```bash
# 保留最近 30 天的日志
find logs/ -name "*.log" -mtime +30 -delete
```

### 10.3 错误监控

在脚本中添加错误处理：

```bash
#!/bin/bash
set -e

DATE=$(date +%Y%m%d)
mkdir -p data/$DATE

# 获取数据，失败时发送通知
if ! finscraper -q index spot -p data/$DATE/indices.csv; then
    echo "数据获取失败: $(date)" | mail -s "FinScraper Error" admin@example.com
    exit 1
fi
```

---

## 10. 获取帮助

### 命令行帮助

```bash
# 查看总体帮助
finscraper --help

# 查看特定命令组帮助
finscraper index --help
finscraper north-flow --help

# 查看具体命令帮助
finscraper index history --help
```

### 项目资源

- 📖 完整文档：[README.md](../README.md)
- 📝 发布说明：[RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)
- 🔧 项目规格：[PROJECT_SPEC.md](PROJECT_SPEC.md)
- 💻 示例脚本：[scripts/example.py](../scripts/example.py)

---

**祝您使用愉快！如有问题，欢迎反馈。** 🚀
