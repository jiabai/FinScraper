# Phase 7: 完善与优化 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 完善项目，包括创建一键获取脚本、示例脚本、完善文档、代码审查和提高测试覆盖率

**Architecture:** 遵循现有架构，创建 scripts 目录，完善现有文档

**Tech Stack:** Python, Typer, pytest-cov

---

## Task 1: 创建 scripts 目录和 __init__.py

**Files:**
- Create: `scripts/__init__.py`

**Step 1: Create scripts directory and __init__.py**

```python
"""Scripts directory for FinScraper project."""
```

**Step 2: Commit**

```bash
git add scripts/__init__.py
git commit -m "feat: add scripts directory"
```

---

## Task 2: 实现一键获取脚本 (scripts/fetch_all.py)

**Files:**
- Create: `scripts/fetch_all.py`

**Step 1: Write fetch_all.py**

```python
"""Fetch all financial data in one go (legacy script for backward compatibility)."""
import datetime
import os
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
    CommodityFetcher,
    MoneyFlowFetcher,
    NewsFetcher,
)
from finscraper.storage.csv_storage import CSVStorage


def main():
    """Main function to fetch all data."""
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    storage = CSVStorage()
    
    print("=" * 60)
    print("FinScraper - 一键获取所有数据")
    print("=" * 60)
    
    try:
        print("\n[1/6] 获取指数数据...")
        index_fetcher = IndexFetcher()
        index_data = index_fetcher.fetch_spot()
        index_path = os.path.join(data_dir, f"index_spot_{today}.csv")
        storage.save(index_data, index_path)
        print(f"   已保存到: {index_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[2/6] 获取北向资金数据...")
        north_flow_fetcher = NorthFlowFetcher()
        north_flow_data = north_flow_fetcher.fetch_daily()
        north_flow_path = os.path.join(data_dir, f"north_flow_daily_{today}.csv")
        storage.save(north_flow_data, north_flow_path)
        print(f"   已保存到: {north_flow_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[3/6] 获取板块数据...")
        sector_fetcher = SectorFetcher()
        sector_data = sector_fetcher.fetch_list()
        sector_path = os.path.join(data_dir, f"sector_list_{today}.csv")
        storage.save(sector_data, sector_path)
        print(f"   已保存到: {sector_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[4/6] 获取大宗商品数据...")
        commodity_fetcher = CommodityFetcher()
        commodity_data = commodity_fetcher.fetch_spot()
        commodity_path = os.path.join(data_dir, f"commodity_spot_{today}.csv")
        storage.save(commodity_data, commodity_path)
        print(f"   已保存到: {commodity_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[5/6] 获取资金流向数据...")
        money_flow_fetcher = MoneyFlowFetcher()
        money_flow_data = money_flow_fetcher.fetch_market()
        money_flow_path = os.path.join(data_dir, f"money_flow_market_{today}.csv")
        storage.save(money_flow_data, money_flow_path)
        print(f"   已保存到: {money_flow_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    try:
        print("\n[6/6] 获取新闻数据...")
        news_fetcher = NewsFetcher()
        news_data = news_fetcher.fetch_global()
        news_path = os.path.join(data_dir, f"news_global_{today}.csv")
        storage.save(news_data, news_path)
        print(f"   已保存到: {news_path}")
    except Exception as e:
        print(f"   获取失败: {e}")
    
    print("\n" + "=" * 60)
    print("数据获取完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add scripts/fetch_all.py
git commit -m "feat: add fetch_all.py script for backward compatibility"
```

---

## Task 3: 实现示例脚本 (scripts/example.py)

**Files:**
- Create: `scripts/example.py`

**Step 1: Write example.py**

```python
"""FinScraper usage examples."""
from finscraper.fetchers import (
    IndexFetcher,
    NorthFlowFetcher,
    SectorFetcher,
    CommodityFetcher,
    MoneyFlowFetcher,
    NewsFetcher,
)
from finscraper.storage.csv_storage import CSVStorage


def example_index_fetcher():
    """Example: IndexFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 1: IndexFetcher - A 股指数数据")
    print("=" * 60)
    
    try:
        fetcher = IndexFetcher()
        
        print("\n获取指数实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条指数实时数据")
        print(spot_data.head())
        
        print("\n获取上证指数历史数据...")
        history_data = fetcher.fetch_history(
            symbol="000001",
            start_date="20240101",
            end_date="20241231",
        )
        print(f"成功获取 {len(history_data)} 条历史数据")
        print(history_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_north_flow_fetcher():
    """Example: NorthFlowFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 2: NorthFlowFetcher - 北向资金数据")
    print("=" * 60)
    
    try:
        fetcher = NorthFlowFetcher()
        
        print("\n获取北向资金日数据...")
        daily_data = fetcher.fetch_daily()
        print(f"成功获取 {len(daily_data)} 条北向资金日数据")
        print(daily_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_sector_fetcher():
    """Example: SectorFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 3: SectorFetcher - 板块数据")
    print("=" * 60)
    
    try:
        fetcher = SectorFetcher()
        
        print("\n获取板块列表...")
        sector_list = fetcher.fetch_list()
        print(f"成功获取 {len(sector_list)} 个板块")
        print(sector_list.head())
        
        print("\n获取板块实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条板块实时数据")
        print(spot_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_commodity_fetcher():
    """Example: CommodityFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 4: CommodityFetcher - 大宗商品数据")
    print("=" * 60)
    
    try:
        fetcher = CommodityFetcher()
        
        print("\n获取大宗商品实时行情...")
        spot_data = fetcher.fetch_spot()
        print(f"成功获取 {len(spot_data)} 条大宗商品实时数据")
        print(spot_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_money_flow_fetcher():
    """Example: MoneyFlowFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 5: MoneyFlowFetcher - 资金流向数据")
    print("=" * 60)
    
    try:
        fetcher = MoneyFlowFetcher()
        
        print("\n获取市场资金流向...")
        market_data = fetcher.fetch_market()
        print(f"成功获取 {len(market_data)} 条市场资金流向数据")
        print(market_data.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_news_fetcher():
    """Example: NewsFetcher usage."""
    print("\n" + "=" * 60)
    print("示例 6: NewsFetcher - 新闻数据")
    print("=" * 60)
    
    try:
        fetcher = NewsFetcher()
        
        print("\n获取全球新闻...")
        global_news = fetcher.fetch_global()
        print(f"成功获取 {len(global_news)} 条全球新闻")
        print(global_news.head())
    except Exception as e:
        print(f"示例执行失败: {e}")


def example_storage():
    """Example: Storage usage."""
    print("\n" + "=" * 60)
    print("示例 7: 数据存储示例")
    print("=" * 60)
    
    try:
        fetcher = IndexFetcher()
        spot_data = fetcher.fetch_spot()
        
        print("\n保存为 CSV...")
        storage = CSVStorage()
        storage.save(spot_data, "example_index_spot.csv")
        print("已保存到 example_index_spot.csv")
        
        print("\n从 CSV 加载...")
        loaded_data = storage.load("example_index_spot.csv")
        print(f"成功加载 {len(loaded_data)} 条数据")
    except Exception as e:
        print(f"示例执行失败: {e}")


def main():
    """Run all examples."""
    print("FinScraper - 使用示例")
    print("=" * 60)
    
    example_index_fetcher()
    example_north_flow_fetcher()
    example_sector_fetcher()
    example_commodity_fetcher()
    example_money_flow_fetcher()
    example_news_fetcher()
    example_storage()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add scripts/example.py
git commit -m "feat: add example.py script with usage examples"
```

---

## Task 4: 完善 README.md

**Files:**
- Modify: `README.md`

**Step 1: Add more comprehensive documentation to README**

Add sections for:
- 项目介绍
- 功能特点
- 数据类型
- 完整的使用示例

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: enhance README with comprehensive documentation"
```

---

## Task 5: 代码审查与优化

**Files:**
- Review: `finscraper/fetchers/__init__.py`
- Review: `finscraper/cli/commands/__init__.py`
- Review: `finscraper/models/__init__.py`

**Step 1: Check if __init__.py files need updates**

Check if we need to export new fetchers and models in __init__.py files.

**Step 2: Optimize code if needed**

Look for:
- Code duplication
- Missing docstrings
- Potential improvements

**Step 3: Commit**

```bash
git add <optimized files>
git commit -m "refactor: code review and optimizations"
```

---

## Task 6: 检查测试覆盖率并提高到 >80%

**Files:**
- Run: `pytest --cov=finscraper`

**Step 1: Check current test coverage**

```bash
pytest --cov=finscraper --cov-report=term-missing
```

**Step 2: Identify gaps and add missing tests**

Add tests for any uncovered modules or functions.

**Step 3: Verify coverage is >80%**

```bash
pytest --cov=finscraper --cov-fail-under=80
```

**Step 4: Commit**

```bash
git add tests/
git commit -m "test: improve test coverage to >80%"
```

---

## Summary

This plan completes Phase 7 (完善与优化):

1. ✅ Create scripts directory with __init__.py
2. ✅ Implement fetch_all.py (backward compatibility script)
3. ✅ Implement example.py with comprehensive usage examples
4. ✅ Enhance README.md with better documentation
5. ✅ Code review and optimization
6. ✅ Improve test coverage to >80%

**Note:** This completes all phases of the project!

**Next Steps:** The project is ready for v1.0 release!
