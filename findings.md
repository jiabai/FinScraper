# 调查发现

## AkShare v1.18.35 函数分析

### 商品现货相关
- ❌ 旧函数：`futures_zh_spot_em`（不存在）
- ✅ 可用函数：`futures_zh_spot`、`futures_global_spot_em`

### 资金流向相关
- ✅ 函数存在：`stock_individual_fund_flow_rank`、`stock_sector_fund_flow_rank`
- ❌ 问题：连接被远程关闭（网络问题）

### 新闻相关
- ❌ 旧函数：`news_global`（不存在）
- ❌ 旧函数：`stock_em_info_aj_em`（不存在）
- ✅ 可用函数：`stock_news_em`（已正常工作）

### 其他可用函数
- `futures_zh_spot` - 中国期货现货
- `futures_global_spot_em` - 全球期货现货
- `stock_individual_info_em` - 个股信息
- `stock_info_global_em` - 全球股票信息
