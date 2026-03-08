# FinScraper 新数据源扩展任务计划

> **日期**: 2026-03-08  
> **目标**: 扩展 FinScraper 支持市场情绪、港股、美股、汇率等数据源，以满足完整的市场概览需求

---

## 概述

本任务计划旨在扩展 FinScraper 项目，添加以下新的数据获取器（Fetcher）：

1. **MarketSentimentFetcher** - 市场情绪数据（涨跌家数、涨停跌停数）
2. **HKIndexFetcher** - 港股/恒生指数数据
3. **USIndexFetcher** - 美股指数数据（道指、纳指、标普500）
4. **ForexFetcher** - 汇率数据（美元、欧元、港币等）

---

## 现状分析

### 当前已支持的数据类型
- ✅ A 股指数（IndexFetcher）
- ✅ 北向资金（NorthFlowFetcher）
- ✅ 板块数据（SectorFetcher）
- ✅ 大宗商品（CommodityFetcher）
- ✅ 资金流向（MoneyFlowFetcher）
- ✅ 重要新闻（NewsFetcher）

### 缺少的数据类型
- ❌ 市场情绪（涨跌家数、涨停跌停）
- ❌ 港股/恒生指数
- ❌ 美股指数
- ❌ 汇率数据

---

## 任务分解

### Phase 1: 文档先行（当前阶段）

| 任务 | 状态 | 说明 |
|-----|------|------|
| 1.1 创建 findings.md | `pending` | 记录调研发现 |
| 1.2 创建开发计划文档 | `pending` | 详细的开发步骤 |
| 1.3 更新 API_REFERENCE.md | `pending` | 添加新 fetcher 说明 |
| 1.4 更新 USER_GUIDE.md | `pending` | 添加新功能使用说明 |

### Phase 2: 核心代码实现

| 任务 | 状态 | 说明 |
|-----|------|------|
| 2.1 更新 AkShareClient | `pending` | 添加新数据类型的接口 |
| 2.2 更新 DataCleaner | `pending` | 添加新数据类型的清洗方法 |
| 2.3 创建数据模型（models） | `pending` | 添加新数据类型的 Pydantic 模型 |
| 2.4 实现 MarketSentimentFetcher | `pending` | 市场情绪数据获取器 |
| 2.5 实现 HKIndexFetcher | `pending` | 港股指数数据获取器 |
| 2.6 实现 USIndexFetcher | `pending` | 美股指数数据获取器 |
| 2.7 实现 ForexFetcher | `pending` | 汇率数据获取器 |

### Phase 3: CLI 集成

| 任务 | 状态 | 说明 |
|-----|------|------|
| 3.1 添加 CLI 命令模块 | `pending` | 在 cli/commands/ 下添加新命令 |
| 3.2 集成到主 CLI | `pending` | 在 cli/main.py 中注册新命令 |

### Phase 4: 测试与文档

| 任务 | 状态 | 说明 |
|-----|------|------|
| 4.1 编写测试用例 | `pending` | 为新 fetcher 编写单元测试 |
| 4.2 运行所有测试 | `pending` | 确保所有测试通过 |
| 4.3 最终文档检查 | `pending` | 确保文档完整准确 |

---

## 新 Fetcher 详细说明

### 1. MarketSentimentFetcher（市场情绪）

**数据源（akshare）**：
- `stock_zh_a_spot_em()` - 获取全部A股数据，统计涨跌家数
- `stock_zt_pool_em()` - 涨停股池
- `stock_zt_pool_em()` - 跌停股池（参数调整）

**功能**：
- `fetch_sentiment()` - 获取综合市场情绪数据
- `fetch_up_down_count()` - 获取涨跌家数
- `fetch_limit_up()` - 获取涨停股票列表
- `fetch_limit_down()` - 获取跌停股票列表

### 2. HKIndexFetcher（港股）

**数据源（akshare）**：
- `index_hk_spot_em()` - 港股实时行情

**功能**：
- `fetch_spot()` - 获取港股实时行情
- `fetch_history()` - 获取港股历史数据

### 3. USIndexFetcher（美股）

**数据源（akshare）**：
- `index_us_spot()` - 美股实时行情
- `index_global_spot()` - 全球指数

**功能**：
- `fetch_spot()` - 获取美股实时行情（道指、纳指、标普500）
- `fetch_history()` - 获取美股历史数据

### 4. ForexFetcher（汇率）

**数据源（akshare）**：
- `forex_spot_em()` - 外汇实时行情
- `forex_hist_em()` - 外汇历史数据

**功能**：
- `fetch_spot()` - 获取汇率实时行情
- `fetch_history()` - 获取汇率历史数据

---

## 开发标准

### 代码风格
- 遵循现有 `CODING_STANDARDS.md` 规范
- 使用 Google 风格的文档字符串
- 完整的类型注解
- 继承 `BaseFetcher` 基类

### 文档要求
- 更新 `API_REFERENCE.md` - 添加新 fetcher 的 API 文档
- 更新 `USER_GUIDE.md` - 添加使用示例
- 创建 `docs/plans/2026-03-08-phase8-new-data-sources.md` - 详细开发计划

---

## 下一步

1. ✅ 完成本任务计划文档
2. ⏳ 创建 `findings.md` 记录调研发现
3. ⏳ 创建详细的开发计划文档
4. ⏳ 更新用户文档
