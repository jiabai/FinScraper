"""有色金属/贵金属行情报告脚本.

获取并展示黄金、白银、铜、铝等金属的实时行情数据.
输出 Markdown 格式报告，供大模型生成分析报告.
"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from finscraper.fetchers.commodity import CommodityFetcher


# 关注的金属品种配置
METALS_CONFIG = {
    "黄金": {
        "keywords": ["黄金"],
        "main_codes": ["GC00Y", "MGC00Y", "QO00Y", "JAU00Y"],  # 主力合约
        "max_contracts": 5,  # 最多显示的合约数量
    },
    "白银": {
        "keywords": ["白银"],
        "main_codes": ["SI00Y", "QI00Y"],
        "max_contracts": 5,
    },
    "铜": {
        "keywords": ["铜"],
        "main_codes": ["HG00Y", "LCPT"],
        "max_contracts": 5,
    },
    "铝": {
        "keywords": ["铝"],
        "main_codes": ["LALT"],
        "max_contracts": 3,
    },
}


def fetch_metals_data():
    """获取所有金属数据."""
    print("正在获取大宗商品数据...", file=sys.stderr)
    fetcher = CommodityFetcher()
    df = fetcher.fetch_spot()
    print(f"成功获取 {len(df)} 条商品数据\n", file=sys.stderr)
    return df


def filter_metals_by_type(df, metal_type):
    """筛选指定类型的金属数据，返回主力合约和近月合约.

    Args:
        df: 商品数据DataFrame
        metal_type: 金属类型 (黄金/白银/铜/铝)

    Returns:
        筛选后的DataFrame，按主力合约优先排序
    """
    if metal_type not in METALS_CONFIG:
        return pd.DataFrame()

    config = METALS_CONFIG[metal_type]
    pattern = "|".join(config["keywords"])
    filtered = df[df["名称"].str.contains(pattern, na=False, regex=True)].copy()

    if filtered.empty:
        return filtered

    # 主力合约优先排序
    main_codes = config["main_codes"]
    filtered["sort_key"] = filtered["代码"].apply(
        lambda x: main_codes.index(x) if x in main_codes else 999
    )
    # 按排序键和成交量排序
    filtered = filtered.sort_values(["sort_key", "成交量"], ascending=[True, False])

    # 限制合约数量
    max_contracts = config.get("max_contracts", 5)
    return filtered.head(max_contracts)


def generate_markdown_report(df, metal_type=None):
    """生成 Markdown 格式的行情报告.

    Args:
        df: 商品数据DataFrame
        metal_type: 金属类型，None表示全部

    Returns:
        Markdown 格式的字符串
    """
    lines = []
    lines.append("# 有色金属/贵金属行情报告")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    if metal_type:
        # 单一金属类型
        metal_df = filter_metals_by_type(df, metal_type)
        if not metal_df.empty:
            lines.append(_generate_metal_section(metal_type, metal_df))
    else:
        # 所有金属类型
        for m_type in METALS_CONFIG.keys():
            metal_df = filter_metals_by_type(df, m_type)
            if not metal_df.empty:
                lines.append(_generate_metal_section(m_type, metal_df))
                lines.append("")

    return "\n".join(lines)


def _generate_metal_section(metal_type, df):
    """生成单个金属类型的 Markdown 部分."""
    lines = []
    lines.append(f"## {metal_type}")
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


def main():
    """主函数."""
    import argparse

    parser = argparse.ArgumentParser(
        description="获取有色金属/贵金属行情数据，输出 Markdown 格式报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/metals_report.py              # 获取所有金属数据
  python scripts/metals_report.py -t 黄金      # 仅获取黄金数据
  python scripts/metals_report.py -t 白银      # 仅获取白银数据
  python scripts/metals_report.py -t 铜        # 仅获取铜数据
  python scripts/metals_report.py -t 铝        # 仅获取铝数据
  python scripts/metals_report.py -o report.md # 保存到文件
        """
    )
    parser.add_argument(
        "-t", "--type",
        choices=["黄金", "白银", "铜", "铝"],
        help="指定金属类型 (默认: 全部)"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (Markdown格式)"
    )

    args = parser.parse_args()

    # 获取数据
    df = fetch_metals_data()

    # 生成 Markdown 报告
    markdown = generate_markdown_report(df, args.type)

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
