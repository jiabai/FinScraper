import akshare as ak
import pandas as pd
from datetime import datetime

def get_v1_18_35_report():
    print(f"重要消息 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)

    # --- 1. 国内宏观 & 权威政策 (使用新闻联播文字) ---
    print("【国内宏观 & 权威政策】")
    try:
        lpr = ak.macro_china_lpr().iloc[-1]
        print(f"● 货币环境：LPR 1Y {lpr['LPR1Y']}% | 5Y {lpr['LPR5Y']}%")
    except: pass

    try:
        # 获取昨天的焦点新闻（新闻联播文字版，绝对权威，接口稳定）
        date_str = datetime.now().strftime("%Y%m%d")
        cctv_news = ak.news_cctv(date=date_str)
        if cctv_news.empty: # 如果今日还没出，取昨天的
            from datetime import timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            cctv_news = ak.news_cctv(date=yesterday)
        
        # 过滤包含 政策、会议、规划、国务院 等关键词
        keywords = ["政策", "会议", "规划", "国务院", "印发", "支持"]
        filtered = cctv_news[cctv_news['content'].str.contains('|'.join(keywords), na=False)].head(3)
        
        if not filtered.empty:
            for _, row in filtered.iterrows():
                print(f"● [权威发布] {row['title']} | {row['content'][:60]}...")
        else:
            print(f"● [今日摘要] {cctv_news.iloc[0]['title']}...")
    except:
        print("● 政策接口受限，建议关注龙头公告动态")

    # --- 2. 海外动态 (硬编码基准 + 指数实时) ---
    print("\n【海外动态 & 美联储】")
    print("● 美联储基准：3.50%-3.75% (下次会议 3月18-19日)")
    try:
        # v1.18.35 下建议使用该接口获取美指
        us_index = ak.index_us_stock_sina(symbol=".IXIC").iloc[-1]
        print(f"● 纳指表现：{us_index['close']} (日期:{us_index['date']})")
    except: pass

    # --- 3. 核心行业龙头实时快照 ---
    print("\n【核心行业 & 龙头表现】")
    industries = {
        "半导体": "603501", "新能源": "300750", "电力": "600900", 
        "航运": "601919", "机器人": "002050"
    }
    try:
        # 这个接口在 v1.18.35 中非常稳健
        spot = ak.stock_zh_a_spot_em()
        for name, code in industries.items():
            target = spot[spot['代码'] == code]
            if not target.empty:
                t = target.iloc[0]
                tag = "▲" if t['涨跌幅'] > 0 else "▼"
                print(f"● [{name}] {t['名称']}: {t['最新价']} ({tag}{t['涨跌幅']}%) | 成交:{round(t['成交额']/1e8, 2)}亿")
    except: pass
    
    print("="*50)

if __name__ == "__main__":
    get_v1_18_35_report()
