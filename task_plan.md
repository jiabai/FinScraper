# 任务计划：修复东方财富接口

## 目标
修复 FinScraper 项目中东方财富接口失效问题

## 阶段

### Phase 1: 根因调查 ✓ (完成)
- 已分析 AkShare v1.18.35 可用函数
- 已识别失效函数和替代方案

### Phase 2: 更新失效函数调用 (进行中)
1. 更新 `fetch_commodity_spot_em` - 使用 `futures_zh_spot`
2. 更新 `fetch_news_global_em` - 移除或替代
3. 更新 `fetch_news_alert_em` - 移除或替代
4. 保留 `fetch_money_flow_stock_em` 和 `fetch_money_flow_sector_em` - 网络问题暂不处理

### Phase 3: 验证修复
- 运行测试脚本验证修复效果
- 确保不破坏现有功能

## 失效函数修复方案

| 原函数 | 问题 | 修复方案 |
|--------|------|----------|
| `futures_zh_spot_em` | 不存在 | 替换为 `futures_zh_spot` |
| `news_global` | 不存在 | 移除该接口（无可用替代） |
| `stock_em_info_aj_em` | 不存在 | 移除该接口（无可用替代） |
| `stock_individual_fund_flow_rank` | 连接问题 | 保留，网络问题待后续处理 |
| `stock_sector_fund_flow_rank` | 连接问题 | 保留，网络问题待后续处理 |
