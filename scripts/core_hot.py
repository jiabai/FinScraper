"""核心热点数据获取脚本.

获取当日市场核心热点数据：
- 领涨/领跌板块
- 涨跌停统计和股票列表
- 市场情绪统计
- 板块资金流向
- 财经新闻

输出 Markdown 格式报告，供人工分析使用。
"""
import sys
import os

os.environ["FINSCRAPER_LOG_LEVEL"] = "CRITICAL"

import pandas as pd
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from finscraper.fetchers.sector import SectorFetcher
from finscraper.fetchers.market_sentiment import MarketSentimentFetcher
from finscraper.fetchers.money_flow import MoneyFlowFetcher
from finscraper.fetchers.news import NewsFetcher


def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_subsection(title: str):
    print(f"\n## {title}")
    print('-' * 40)


def format_change(val: float) -> str:
    if pd.isna(val):
        return "N/A"
    if val > 0:
        return f"+{val:.2f}%"
    elif val < 0:
        return f"{val:.2f}%"
    return "0.00%"


def format_number(val) -> str:
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, float)):
        if abs(val) >= 1e8:
            return f"{val/1e8:.2f}亿"
        elif abs(val) >= 1e4:
            return f"{val/1e4:.2f}万"
        return f"{val:.2f}"
    return str(val)


def fetch_sectors() -> pd.DataFrame:
    """获取板块数据."""
    print("正在获取板块数据...", file=sys.stderr)
    try:
        fetcher = SectorFetcher()
        df = fetcher.fetch_spot()
        print(f"成功获取 {len(df)} 个板块数据", file=sys.stderr)
        return df
    except Exception as e:
        print(f"获取板块数据失败: {e}", file=sys.stderr)
        return pd.DataFrame()


def fetch_sentiment() -> dict:
    """获取市场情绪数据."""
    print("正在获取市场情绪数据...", file=sys.stderr)
    try:
        fetcher = MarketSentimentFetcher()
        result = fetcher.fetch_sentiment()
        if result is not None and not result.empty:
            data = result.iloc[0].to_dict()
            print("成功获取市场情绪数据", file=sys.stderr)
            return data
    except Exception as e:
        print(f"获取市场情绪数据失败: {e}", file=sys.stderr)
    return {}


def fetch_limit_up() -> pd.DataFrame:
    """获取涨停股票列表."""
    print("正在获取涨停股票...", file=sys.stderr)
    try:
        fetcher = MarketSentimentFetcher()
        df = fetcher.fetch_limit_up()
        if df is not None:
            print(f"成功获取 {len(df)} 只涨停股", file=sys.stderr)
            return df
    except Exception as e:
        print(f"获取涨停股票失败: {e}", file=sys.stderr)
    return pd.DataFrame()


def fetch_limit_down() -> pd.DataFrame:
    """获取跌停股票列表."""
    print("正在获取跌停股票...", file=sys.stderr)
    try:
        fetcher = MarketSentimentFetcher()
        df = fetcher.fetch_limit_down()
        if df is not None:
            print(f"成功获取 {len(df)} 只跌停股", file=sys.stderr)
            return df
    except Exception as e:
        print(f"获取跌停股票失败: {e}", file=sys.stderr)
    return pd.DataFrame()


def fetch_money_flow_sector() -> pd.DataFrame:
    """获取板块资金流向."""
    print("正在获取板块资金流向...", file=sys.stderr)
    try:
        fetcher = MoneyFlowFetcher()
        df = fetcher.fetch_sector()
        if df is not None:
            print(f"成功获取 {len(df)} 个板块资金流向数据", file=sys.stderr)
            return df
    except Exception as e:
        print(f"获取板块资金流向失败: {e}", file=sys.stderr)
    return pd.DataFrame()


def fetch_news() -> pd.DataFrame:
    """获取财经新闻."""
    print("正在获取财经新闻...", file=sys.stderr)
    try:
        fetcher = NewsFetcher()
        df = fetcher.fetch_alert()
        if df is not None:
            print(f"成功获取 {len(df)} 条新闻", file=sys.stderr)
            return df
    except Exception as e:
        print(f"获取财经新闻失败: {e}", file=sys.stderr)
    return pd.DataFrame()


def generate_sector_report(df: pd.DataFrame):
    """生成板块涨跌报告."""
    print_subsection("领涨板块 (Top 10)")
    
    if df is None or df.empty:
        print("暂无数据")
        return
    
    cols = df.columns.tolist()
    name_col = next((c for c in ['板块', '板块名称', '名称'] if c in cols), None)
    change_col = next((c for c in ['涨跌幅', '涨跌幅'] if c in cols), None)
    lead_stock_col = next((c for c in ['股票名称', '领涨股', '名称'] if c in cols), None)
    lead_change_col = next((c for c in ['个股-涨跌幅', '领涨股涨幅'] if c in cols), None)
    
    if name_col is None or change_col is None:
        print(f"无法识别的列: {cols[:5]}")
        return
    
    df_sorted = df.sort_values(change_col, ascending=False)
    
    print(f"| 板块名称 | 涨跌幅 | 领涨股 | 领涨股涨幅 |")
    print(f"|----------|--------|--------|------------|")
    
    for _, row in df_sorted.head(10).iterrows():
        name = row.get(name_col, 'N/A')
        change = format_change(row.get(change_col, 0))
        lead_stock = row.get(lead_stock_col, 'N/A')
        lead_change = format_change(row.get(lead_change_col, 0))
        print(f"| {name} | {change} | {lead_stock} | {lead_change} |")
    
    print_subsection("领跌板块 (Top 10)")
    
    print(f"| 板块名称 | 涨跌幅 | 领涨股 | 领涨股涨幅 |")
    print(f"|----------|--------|--------|------------|")
    
    for _, row in df_sorted.tail(10).iloc[::-1].iterrows():
        name = row.get(name_col, 'N/A')
        change = format_change(row.get(change_col, 0))
        lead_stock = row.get(lead_stock_col, 'N/A')
        lead_change = format_change(row.get(lead_change_col, 0))
        print(f"| {name} | {change} | {lead_stock} | {lead_change} |")


def generate_sentiment_report(sentiment: dict, limit_up: pd.DataFrame, limit_down: pd.DataFrame):
    """生成市场情绪报告."""
    print_subsection("市场情绪概览")
    
    print(f"- 上涨股票: {sentiment.get('up_count', 'N/A')} 只")
    print(f"- 下跌股票: {sentiment.get('down_count', 'N/A')} 只")
    print(f"- 平盘股票: {sentiment.get('flat_count', 'N/A')} 只")
    print(f"- 涨停股票: {sentiment.get('limit_up_count', 'N/A')} 只")
    print(f"- 跌停股票: {sentiment.get('limit_down_count', 'N/A')} 只")
    
    up = sentiment.get('up_count', 0)
    down = sentiment.get('down_count', 0)
    if up + down > 0:
        ratio = up / (up + down) * 100
        print(f"- 涨跌比例: {ratio:.1f}% (上涨/下跌)")
    
    print_subsection("涨停股票 (Top 20)")
    
    if limit_up is not None and not limit_up.empty:
        cols = limit_up.columns.tolist()
        name_col = next((c for c in ['股票名称', '名称', 'name', '股票简称'] if c in cols), None)
        change_col = next((c for c in ['涨跌幅', '涨幅', 'change'] if c in cols), None)
        
        if name_col:
            print(f"| # | 股票名称 | 涨跌幅 |")
            print(f"|---|----------|--------|")
            for i, row in limit_up.head(20).iterrows():
                name = row.get(name_col, 'N/A')
                change = format_change(row.get(change_col, 0)) if change_col else 'N/A'
                print(f"| {i+1} | {name} | {change} |")
    else:
        print("暂无涨停股票数据")
    
    print_subsection("跌停股票 (Top 20)")
    
    if limit_down is not None and not limit_down.empty:
        cols = limit_down.columns.tolist()
        name_col = next((c for c in ['股票名称', '名称', 'name', '股票简称'] if c in cols), None)
        change_col = next((c for c in ['涨跌幅', '跌幅', 'change'] if c in cols), None)
        
        if name_col:
            print(f"| # | 股票名称 | 涨跌幅 |")
            print(f"|---|----------|--------|")
            for i, row in limit_down.head(20).iterrows():
                name = row.get(name_col, 'N/A')
                change = format_change(row.get(change_col, 0)) if change_col else 'N/A'
                print(f"| {i+1} | {name} | {change} |")
    else:
        print("暂无跌停股票数据 (市场无跌停股或数据获取失败)")


def generate_money_flow_report(df: pd.DataFrame):
    """生成资金流向报告."""
    print_subsection("主力资金净流入 (Top 10)")
    
    if df is None or df.empty:
        print("暂无数据")
        return
    
    cols = df.columns.tolist()
    name_col = next((c for c in ['行业', '名称', '板块名称'] if c in cols), None)
    flow_col = next((c for c in ['净额', '流入资金', '主力净流入'] if c in cols), None)
    
    if name_col is None or flow_col is None:
        print(f"无法识别的列: {cols[:5]}")
        return
    
    df_sorted = df.sort_values(flow_col, ascending=False)
    
    print(f"| 板块名称 | 资金净额 |")
    print(f"|----------|----------|")
    
    for _, row in df_sorted.head(10).iterrows():
        name = row.get(name_col, 'N/A')
        flow = format_number(row.get(flow_col, 0))
        print(f"| {name} | {flow} |")
    
    print_subsection("主力资金净流出 (Top 10)")
    
    print(f"| 板块名称 | 资金净额 |")
    print(f"|----------|----------|")
    
    for _, row in df_sorted.tail(10).iloc[::-1].iterrows():
        name = row.get(name_col, 'N/A')
        flow = format_number(row.get(flow_col, 0))
        print(f"| {name} | {flow} |")


def generate_news_report(df: pd.DataFrame):
    """生成新闻报告."""
    print_subsection("最新财经新闻 (Top 30)")
    
    if df is None or df.empty:
        print("暂无新闻数据")
        return
    
    cols = df.columns.tolist()
    title_col = next((c for c in ['新闻标题', '标题', 'title'] if c in cols), None)
    time_col = next((c for c in ['发布时间', '时间', 'time', 'datetime'] if c in cols), None)
    source_col = next((c for c in ['来源', 'source'] if c in cols), None)
    
    if title_col:
        for i, row in df.head(30).iterrows():
            title = row.get(title_col, 'N/A')
            time = row.get(time_col, '')
            source = row.get(source_col, '')
            print(f"- {title}")
            if time or source:
                print(f"  - {source} {time}")
    else:
        print(df.head(30).to_string())


def main():
    now = datetime.now()
    print(f"# 核心热点数据报告")
    print(f"**生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"**数据来源**: AkShare (东方财富)")
    
    sectors = fetch_sectors()
    sentiment = fetch_sentiment()
    limit_up = fetch_limit_up()
    limit_down = fetch_limit_down()
    money_flow = fetch_money_flow_sector()
    news = fetch_news()
    
    print_section("板块涨跌")
    generate_sector_report(sectors)
    
    print_section("市场情绪与涨跌停")
    generate_sentiment_report(sentiment, limit_up, limit_down)
    
    print_section("板块资金流向")
    generate_money_flow_report(money_flow)
    
    print_section("财经新闻")
    generate_news_report(news)
    
    print("\n" + "="*60)
    print("  报告生成完毕")
    print("="*60)


if __name__ == "__main__":
    main()
