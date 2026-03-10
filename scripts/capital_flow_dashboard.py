"""
资金流向看板 - 板块实时监控

通过新浪财经和东方财富接口获取 A 股实时行情数据，监控：
1. 核心板块（半导体、新能源、具身智能、电力）的资金流向、涨跌情况
2. 北向/南向资金数据
3. 大盘主力资金流向
4. 深交所融资融券余额数据

用法:
    python capital_flow_dashboard.py
"""

import os
import akshare as ak
import pandas as pd

# 过滤代理设置：清除系统代理，确保 akshare 请求不走代理
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    if key in os.environ:
        del os.environ[key]

def get_sina_final_fix_v2():
    # 1. 配置核心标的
    config = {
        "半导体": {"stocks": ["603501", "688012", "688981"], "etf": "512480"},
        "新能源": {"stocks": ["300750", "601012", "002460"], "etf": "516160"},
        "具身智能": {"stocks": ["300024", "603911", "002031"], "etf": "159770"},
        "电力": {"stocks": ["600023", "600900", "600011"], "etf": "512670"}
    }

    print("📡 正在获取新浪实时行情...")
    try:
        market_df = ak.stock_zh_a_spot()
        market_df['代码'] = market_df['代码'].astype(str).str.extract(r'(\d+)')[0].str.zfill(6)
    except Exception as e:
        print("⚠️ 数据源暂时不可用，请稍后重试")
        return None

    print("📡 正在获取 ETF 实时数据...")
    try:
        etf_market = ak.fund_etf_category_sina(symbol="ETF基金")
    except Exception as e:
        print("⚠️ ETF 数据暂时不可用")
        return None

    report = []
    for sector, info in config.items():
        # A. 匹配个股
        s_data = market_df[market_df['代码'].isin(info['stocks'])].copy()
        
        if not s_data.empty:
            # 强制数值转换
            s_data['涨跌幅'] = pd.to_numeric(s_data['涨跌幅'], errors='coerce')
            s_data['成交额'] = pd.to_numeric(s_data['成交额'], errors='coerce')
            
            avg_pct = s_data['涨跌幅'].mean()
            # 新浪个股成交额单位为“元”，需除以 1e8 换算为“亿元”
            total_amount_yi = s_data['成交额'].sum() / 1e8
        else:
            avg_pct, total_amount_yi = 0.0, 0.0
            
        # B. 匹配 ETF 并消除 NumPy 警告
        e_codes = ["sh" + info['etf'], "sz" + info['etf']]
        e_data = etf_market[etf_market['代码'].isin(e_codes)]
        
        if not e_data.empty:
            # 【核心修复 2】解决 DeprecationWarning，提取首个元素
            etf_turnover_val = e_data['成交额'].iloc[0]
            etf_turnover = float(etf_turnover_val) / 1e8
        else:
            etf_turnover = 0.0

        report.append({
            "板块": sector,
            "均涨跌": f"{avg_pct:.2f}%",
            "核心股成交(亿)": round(total_amount_yi, 2),
            "ETF成交(亿)": round(etf_turnover, 2),
            "状态": "放量" if total_amount_yi > 0.5 else "缩量"
        })
    
    return pd.DataFrame(report)

def get_hsgt_data():
    """获取北向/南向资金数据"""
    print("📡 正在获取北向/南向资金数据...")
    try:
        hsgt_df = ak.stock_hsgt_hist_em(symbol='南向资金')
        north_df = ak.stock_hsgt_hist_em(symbol="北向资金")
        return hsgt_df, north_df
    except Exception as e:
        print("⚠️ 北向/南向资金数据暂时不可用")
        return None, None

def get_main_fund_flow():
    """获取今日大盘主力资金流向"""
    print("📡 正在获取大盘主力资金流向...")
    try:
        main_fund_df = ak.stock_market_fund_flow()
        return main_fund_df
    except Exception as e:
        print("⚠️ 主力资金数据暂时不可用")
        return None

def get_margin_trading_data():
    """获取深交所融资融券余额数据"""
    print("📡 正在获取融资融券数据...")
    try:
        margin_df = ak.macro_china_market_margin_sz()
        return margin_df
    except Exception as e:
        print("⚠️ 融资融券数据暂时不可用")
        return None

# 执行监控
print("\n" + "🛡️ " * 5 + " 看板数据 (v1.18.35) " + "🛡️ " * 5)
result = get_sina_final_fix_v2()
if result is not None:
    print(result.to_string())
else:
    print("\n📊 请稍后刷新重试")

# 北向/南向资金数据
print("\n" + "📊 " * 5 + " 沪深港通资金 " + "📊 " * 5)
hsgt_df, north_df = get_hsgt_data()
if hsgt_df is not None and north_df is not None:
    print("\n南向资金:")
    print(hsgt_df.tail(3).to_string())
    print("\n北向资金:")
    print(north_df.tail(3).to_string())

# 大盘主力资金流向
print("\n" + "📊 " * 5 + " 大盘主力资金 " + "📊 " * 5)
main_fund_df = get_main_fund_flow()
if main_fund_df is not None:
    print(main_fund_df.tail().to_string())

# 融资融券余额数据
print("\n" + "📊 " * 5 + " 融资融券数据 " + "📊 " * 5)
margin_df = get_margin_trading_data()
if margin_df is not None:
    print(margin_df.tail().to_string())
