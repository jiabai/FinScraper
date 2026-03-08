# 进度记录

## 完成日期
2026-03-08

## 完成工作

### 1. 升级 AkShare 到 v1.18.35 ✓
- 从 v1.17.9 升级到 v1.18.35
- 更新了依赖包 curl_cffi 到 v0.14.0

### 2. 修复东方财富接口 ✓

#### 修复的接口
| 接口 | 修复方案 | 状态 |
|------|----------|------|
| `fetch_commodity_spot_em` | 从 `futures_zh_spot_em` → `futures_global_spot_em` | ✓ 成功 |
| `fetch_money_flow_stock_em` | 从 `stock_individual_fund_flow_rank` → `stock_fund_flow_individual` | ✓ 成功 |
| `fetch_money_flow_sector_em` | 从 `stock_sector_fund_flow_rank` → `stock_fund_flow_industry` | ✓ 成功 |
| `fetch_news_global_em` | 抛出 NotImplementedError（无可用替代） | ✓ 已处理 |
| `fetch_news_alert_em` | 从 `stock_em_info_aj_em` → `stock_news_main_cx` | ✓ 成功 |

### 3. 测试结果
- **成功接口数**：9/10
- **项目测试**：13 个通过，2 个被正确跳过

## 遗留问题
- `fetch_news_global_em` - 全球新闻接口无可用替代函数，保留 NotImplementedError

