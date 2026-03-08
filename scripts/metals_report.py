"""有色金属/贵金属行情报告脚本.

获取并展示黄金、白银、铜、铝等金属的实时行情数据.
"""
import sys
import pandas as pd
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from finscraper.fetchers.commodity import CommodityFetcher


# 关注的金属品种配置
METALS_CONFIG = {
    "黄金": {
        "keywords": ["黄金"],
        "codes": ["GC00Y", "MGC00Y", "QO00Y", "JAU00Y"],  # 主要黄金合约
    },
    "白银": {
        "keywords": ["白银"],
        "codes": ["SI00Y", "QI00Y"],  # 主要白银合约
    },
    "铜": {
        "keywords": ["铜"],
        "codes": ["HG00Y", "LCPT"],  # 主要铜合约
    },
    "铝": {
        "keywords": ["铝"],
        "codes": ["LALT"],  # 主要铝合约
    },
}


def fetch_metals_data():
    """获取所有金属数据."""
    print("正在获取大宗商品数据...")
    fetcher = CommodityFetcher()
    df = fetcher.fetch_spot()
    print(f"成功获取 {len(df)} 条商品数据\n")
    return df


def filter_metals(df, metal_type=None):
    """筛选金属数据.

    Args:
        df: 商品数据DataFrame
        metal_type: 金属类型 (黄金/白银/铜/铝)，None表示全部

    Returns:
        筛选后的DataFrame
    """
    if metal_type and metal_type in METALS_CONFIG:
        config = METALS_CONFIG[metal_type]
        # 按名称关键词筛选
        pattern = "|".join(config["keywords"])
        filtered = df[df["名称"].str.contains(pattern, na=False, regex=True)].copy()
        # 优先显示主力合约
        codes = config["codes"]
        filtered["sort_key"] = filtered["代码"].apply(
            lambda x: codes.index(x) if x in codes else 999
        )
        filtered = filtered.sort_values("sort_key").drop("sort_key", axis=1)
        return filtered
    else:
        # 筛选所有配置的金属
        all_keywords = []
        for config in METALS_CONFIG.values():
            all_keywords.extend(config["keywords"])
        pattern = "|".join(set(all_keywords))
        return df[df["名称"].str.contains(pattern, na=False, regex=True)]


def display_metals(df, metal_type=None):
    """展示金属数据.

    Args:
        df: 金属数据DataFrame
        metal_type: 金属类型标题
    """
    if df.empty:
        print("未找到相关数据")
        return

    # 选择要展示的列
    display_cols = ["代码", "名称", "最新价", "涨跌额", "涨跌幅", "最高", "最低", "成交量"]
    available_cols = [col for col in display_cols if col in df.columns]
    display_df = df[available_cols].copy()

    # 格式化数值列
    if "最新价" in display_df.columns:
        display_df["最新价"] = display_df["最新价"].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
    if "涨跌额" in display_df.columns:
        display_df["涨跌额"] = display_df["涨跌额"].apply(lambda x: f"{x:+.2f}" if pd.notna(x) else "-")
    if "涨跌幅" in display_df.columns:
        display_df["涨跌幅"] = display_df["涨跌幅"].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "-")
    if "最高" in display_df.columns:
        display_df["最高"] = display_df["最高"].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
    if "最低" in display_df.columns:
        display_df["最低"] = display_df["最低"].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")

    title = f"{metal_type}行情" if metal_type else "有色金属/贵金属行情"
    print("=" * 80)
    print(f"{title:^80}")
    print("=" * 80)
    print(display_df.to_string(index=False))
    print()


def main():
    """主函数."""
    import argparse

    parser = argparse.ArgumentParser(
        description="获取有色金属/贵金属行情数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/metals_report.py           # 获取所有金属数据
  python scripts/metals_report.py -t 黄金   # 仅获取黄金数据
  python scripts/metals_report.py -t 白银   # 仅获取白银数据
  python scripts/metals_report.py -t 铜     # 仅获取铜数据
  python scripts/metals_report.py -t 铝     # 仅获取铝数据
        """
    )
    parser.add_argument(
        "-t", "--type",
        choices=["黄金", "白银", "铜", "铝"],
        help="指定金属类型 (默认: 全部)"
    )
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (CSV格式)"
    )

    args = parser.parse_args()

    # 获取数据
    df = fetch_metals_data()

    # 筛选数据
    filtered_df = filter_metals(df, args.type)

    # 展示数据
    display_metals(filtered_df, args.type)

    # 保存到文件
    if args.output:
        filtered_df.to_csv(args.output, index=False, encoding="utf-8-sig")
        print(f"数据已保存到: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
