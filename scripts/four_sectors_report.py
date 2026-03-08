"""四大行业(航运、石油、电力、煤炭)数据获取与报告生成脚本.

获取航运、石油、电力、煤炭四大行业的板块行情数据.
输出 Markdown 格式报告，供大模型生成分析报告.
"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from finscraper.fetchers.sector import SectorFetcher
from finscraper.fetchers.commodity import CommodityFetcher


# 四大行业配置
FOUR_SECTORS_CONFIG = {
    "航运": {
        "keywords": ["航运", "港口", "海运", "物流", "船舶", "码头", "集装箱", "水运"],
        "max_sectors": 5,
    },
    "石油": {
        "keywords": ["石油", "原油", "石化", "油气", "能源"],
        "max_sectors": 5,
    },
    "电力": {
        "keywords": ["电力", "发电", "电网", "火电", "水电", "核电", "风电", "光伏", "新能源"],
        "max_sectors": 5,
    },
    "煤炭": {
        "keywords": ["煤炭", "煤矿", "焦炭", "焦煤", "动力煤", "煤化工"],
        "max_sectors": 5,
    },
}

# 能源类大宗商品配置
ENERGY_COMMODITIES_CONFIG = {
    "原油": {
        "keywords": ["原油", "SC", "WTI", "Brent"],
        "max_contracts": 3,
    },
    "天然气": {
        "keywords": ["天然气", "NG"],
        "max_contracts": 3,
    },
    "煤炭": {
        "keywords": ["煤炭", "焦炭", "焦煤", "动力煤"],
        "max_contracts": 3,
    },
}


def fetch_sector_data():
    """获取板块行情数据."""
    print("正在获取板块数据...", file=sys.stderr)
    fetcher = SectorFetcher()
    df = fetcher.fetch_spot()
    print(f"成功获取 {len(df)} 个板块数据\n", file=sys.stderr)
    return df


def fetch_commodity_data():
    """获取大宗商品数据."""
    print("正在获取大宗商品数据...", file=sys.stderr)
    fetcher = CommodityFetcher()
    df = fetcher.fetch_spot()
    print(f"成功获取 {len(df)} 条商品数据\n", file=sys.stderr)
    return df


def filter_sectors_by_type(df, sector_type):
    """筛选指定类型的板块数据.

    Args:
        df: 板块数据DataFrame
        sector_type: 行业类型 (航运/石油/电力/煤炭)

    Returns:
        筛选后的DataFrame
    """
    if sector_type not in FOUR_SECTORS_CONFIG:
        return pd.DataFrame()

    config = FOUR_SECTORS_CONFIG[sector_type]
    pattern = "|".join(config["keywords"])

    # 确定板块名称列
    name_col = "板块"
    if "板块" not in df.columns:
        for col in ["名称", "sector", "name"]:
            if col in df.columns:
                name_col = col
                break

    filtered = df[df[name_col].str.contains(pattern, na=False, regex=True, case=False)].copy()

    if filtered.empty:
        return filtered

    # 按涨跌幅排序
    sort_col = "涨跌幅"
    if sort_col not in filtered.columns:
        for col in ["change_pct", "涨跌"]:
            if col in filtered.columns:
                sort_col = col
                break

    filtered = filtered.sort_values(sort_col, ascending=False)

    # 限制数量
    max_sectors = config.get("max_sectors", 5)
    return filtered.head(max_sectors)


def filter_commodities_by_type(df, commodity_type):
    """筛选指定类型的大宗商品数据.

    Args:
        df: 商品数据DataFrame
        commodity_type: 商品类型 (原油/天然气/煤炭)

    Returns:
        筛选后的DataFrame
    """
    if commodity_type not in ENERGY_COMMODITIES_CONFIG:
        return pd.DataFrame()

    config = ENERGY_COMMODITIES_CONFIG[commodity_type]
    pattern = "|".join(config["keywords"])

    if "名称" not in df.columns:
        return pd.DataFrame()

    filtered = df[df["名称"].str.contains(pattern, na=False, regex=True, case=False)].copy()

    if filtered.empty:
        return filtered

    # 按成交量排序
    if "成交量" in filtered.columns:
        filtered = filtered.sort_values("成交量", ascending=False)

    # 限制数量
    max_contracts = config.get("max_contracts", 3)
    return filtered.head(max_contracts)


def generate_markdown_report(sectors_df, commodities_df, sector_type=None):
    """生成 Markdown 格式的行情报告.

    Args:
        sectors_df: 板块数据DataFrame
        commodities_df: 商品数据DataFrame
        sector_type: 行业类型，None表示全部

    Returns:
        Markdown 格式的字符串
    """
    lines = []
    lines.append("# 四大行业(航运、石油、电力、煤炭)市场分析报告")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    if sector_type:
        # 单一行业类型
        sector_df = filter_sectors_by_type(sectors_df, sector_type)
        if not sector_df.empty:
            lines.append(_generate_sector_section(sector_type, sector_df))
            lines.append("")

        # 相关大宗商品
        if sector_type == "石油":
            commodity_df = filter_commodities_by_type(commodities_df, "原油")
            if not commodity_df.empty:
                lines.append(_generate_commodity_section("原油", commodity_df))
        elif sector_type == "煤炭":
            commodity_df = filter_commodities_by_type(commodities_df, "煤炭")
            if not commodity_df.empty:
                lines.append(_generate_commodity_section("煤炭", commodity_df))
    else:
        # 所有行业类型
        for s_type in FOUR_SECTORS_CONFIG.keys():
            sector_df = filter_sectors_by_type(sectors_df, s_type)
            if not sector_df.empty:
                lines.append(_generate_sector_section(s_type, sector_df))
                lines.append("")

        # 大宗商品部分
        lines.append("## 能源类大宗商品")
        lines.append("")
        for c_type in ENERGY_COMMODITIES_CONFIG.keys():
            commodity_df = filter_commodities_by_type(commodities_df, c_type)
            if not commodity_df.empty:
                lines.append(_generate_commodity_section(c_type, commodity_df))
                lines.append("")

    return "\n".join(lines)


def _generate_sector_section(sector_type, df):
    """生成单个行业类型的 Markdown 部分."""
    lines = []
    lines.append(f"## {sector_type}")
    lines.append("")

    # 确定列名
    name_col = "板块"
    if "板块" not in df.columns:
        for col in ["名称", "sector", "name"]:
            if col in df.columns:
                name_col = col
                break

    lines.append(f"| {name_col} | 涨跌幅 | 涨跌额 | 总成交额 | 公司家数 | 领涨股 |")
    lines.append("|------|--------|--------|----------|----------|--------|")

    for _, row in df.iterrows():
        name = str(row.get(name_col, "-"))
        change_pct = _format_pct(row.get("涨跌幅"))
        change = _format_change(row.get("涨跌额"))
        amount = _format_amount(row.get("总成交额"))
        count = _format_int(row.get("公司家数"))
        leader = str(row.get("领涨股", "-")) if "领涨股" in row.index else "-"

        lines.append(f"| {name} | {change_pct} | {change} | {amount} | {count} | {leader} |")

    return "\n".join(lines)


def _generate_commodity_section(commodity_type, df):
    """生成单个商品类型的 Markdown 部分."""
    lines = []
    lines.append(f"### {commodity_type}")
    lines.append("")
    lines.append("| 代码 | 名称 | 最新价 | 涨跌额 | 涨跌幅 | 今开 | 最高 | 最低 | 昨结 | 成交量 |")
    lines.append("|------|------|--------|--------|--------|------|------|------|------|--------|")

    for _, row in df.iterrows():
        code = row.get("代码", "-")
        name = row.get("名称", "-")
        latest = _format_price(row.get("最新价"))
        change = _format_change(row.get("涨跌额"))
        change_pct = _format_pct(row.get("涨跌幅"))
        open_price = _format_price(row.get("今开"))
        high = _format_price(row.get("最高"))
        low = _format_price(row.get("最低"))
        prev_close = _format_price(row.get("昨结"))
        volume = _format_volume(row.get("成交量"))

        lines.append(f"| {code} | {name} | {latest} | {change} | {change_pct} | {open_price} | {high} | {low} | {prev_close} | {volume} |")

    return "\n".join(lines)


def _format_price(value):
    """格式化价格."""
    if pd.isna(value):
        return "-"
    return f"{value:.2f}"


def _format_change(value):
    """格式化涨跌额."""
    if pd.isna(value):
        return "-"
    return f"{value:+.2f}"


def _format_pct(value):
    """格式化涨跌幅."""
    if pd.isna(value):
        return "-"
    return f"{value:+.2f}%"


def _format_volume(value):
    """格式化成交量."""
    if pd.isna(value) or value == 0:
        return "-"
    if value >= 10000:
        return f"{value/10000:.1f}万"
    return str(int(value))


def _format_amount(value):
    """格式化成交额."""
    if pd.isna(value) or value == 0:
        return "-"
    if value >= 100000000:
        return f"{value/100000000:.2f}亿"
    if value >= 10000:
        return f"{value/10000:.2f}万"
    return f"{value:.2f}"


def _format_int(value):
    """格式化整数."""
    if pd.isna(value):
        return "-"
    return str(int(value))


def main():
    """主函数."""
    import argparse

    parser = argparse.ArgumentParser(
        description="获取四大行业(航运、石油、电力、煤炭)行情数据，输出 Markdown 格式报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/four_sectors_report.py              # 获取所有行业数据
  python scripts/four_sectors_report.py -t 航运      # 仅获取航运行业数据
  python scripts/four_sectors_report.py -t 石油      # 仅获取石油行业数据
  python scripts/four_sectors_report.py -t 电力      # 仅获取电力行业数据
  python scripts/four_sectors_report.py -t 煤炭      # 仅获取煤炭行业数据
  python scripts/four_sectors_report.py -o report.md # 保存到文件
        """
    )
    parser.add_argument(
        "-t", "--type",
        choices=["航运", "石油", "电力", "煤炭"],
        help="指定行业类型 (默认: 全部)"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (Markdown格式)"
    )

    args = parser.parse_args()

    # 获取数据
    sectors_df = fetch_sector_data()
    commodities_df = fetch_commodity_data()

    # 生成 Markdown 报告
    markdown = generate_markdown_report(sectors_df, commodities_df, args.type)

    # 打印到控制台
    print(markdown)

    # 保存到文件
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"\n报告已保存到: {args.output}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
