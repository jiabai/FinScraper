# Phase 4: CLI Command Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement CLI commands that connect to the data fetchers (Phase 5) to provide real financial data via the command line.

**Architecture:** Each CLI command imports the corresponding Fetcher, fetches data, uses output utilities to format and display/save the data.

**Tech Stack:** Typer, Rich, pandas, existing fetchers

---

## Task 1: Implement Index Command Group

**Files:**
- Modify: `finscraper/cli/commands/index.py`
- Test: `tests/test_cli/test_index.py`

**Step 1: Update index.py implementation**

```python
import typer
from typing_extensions import Annotated
from finscraper.fetchers.index import IndexFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

index_app = typer.Typer(
    name="index",
    help="A 股指数命令",
)


@index_app.command("list")
def list_indices(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
):
    """列出可用指数"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output = output_data(data, format=format)
        typer.echo(output)
        print_success(f"成功获取 {len(data)} 条指数数据")
        
    except Exception as e:
        print_error(f"获取指数列表失败: {e}")
        raise typer.Exit(code=1)


@index_app.command("spot")
def spot_indices(
    symbols: Annotated[
        str,
        typer.Option(
            "--symbols",
            "-s",
            help="指数代码（逗号分隔）",
        ),
    ] = None,
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取实时行情"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        if symbols:
            symbol_list = [s.strip() for s in symbols.split(",")]
            if "代码" in data.columns:
                data = data[data["代码"].isin(symbol_list)]
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条实时行情数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取实时行情失败: {e}")
        raise typer.Exit(code=1)


@index_app.command("history")
def history_index(
    symbol: Annotated[
        str,
        typer.Argument(help="指数代码"),
    ],
    start_date: Annotated[
        str,
        typer.Option(
            "--start-date",
            help="开始日期 (YYYYMMDD)",
        ),
    ] = "",
    end_date: Annotated[
        str,
        typer.Option(
            "--end-date",
            help="结束日期 (YYYYMMDD)",
        ),
    ] = "",
    period: Annotated[
        str,
        typer.Option(
            "--period",
            help="周期 (daily|weekly|monthly)",
        ),
    ] = "daily",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取历史数据"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_history(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            period=period,
        )
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条历史数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取历史数据失败: {e}")
        raise typer.Exit(code=1)
```

**Step 2: Create test file**

```python
# tests/test_cli/test_index.py
import pytest
from typer.testing import CliRunner
from finscraper.cli.main import app


def test_index_list_command():
    runner = CliRunner()
    result = runner.invoke(app, ["index", "list", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output


def test_index_spot_command():
    runner = CliRunner()
    result = runner.invoke(app, ["index", "spot", "--help"])
    assert result.exit_code == 0
    assert "spot" in result.output


def test_index_history_command():
    runner = CliRunner()
    result = runner.invoke(app, ["index", "history", "--help"])
    assert result.exit_code == 0
    assert "history" in result.output
```

**Step 3: Run tests**

Run: `pytest tests/test_cli/test_index.py -v`
Expected: All tests pass

**Step 4: Commit**

```bash
git add finscraper/cli/commands/index.py tests/test_cli/test_index.py
git commit -m "feat: implement index command group with real data"
```

---

## Task 2: Implement North-Flow Command Group

**Files:**
- Modify: `finscraper/cli/commands/north_flow.py`
- Test: `tests/test_cli/test_north_flow.py`

**Step 1: Update north_flow.py implementation**

```python
import typer
from typing_extensions import Annotated
from finscraper.fetchers.north_flow import NorthFlowFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

north_flow_app = typer.Typer(
    name="north-flow",
    help="北向资金命令",
)


@north_flow_app.command("daily")
def daily_north_flow(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取北向资金日数据"""
    try:
        fetcher = NorthFlowFetcher()
        data = fetcher.fetch_daily()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条北向资金日数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取北向资金日数据失败: {e}")
        raise typer.Exit(code=1)


@north_flow_app.command("intraday")
def intraday_north_flow(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取北向资金日内数据"""
    try:
        fetcher = NorthFlowFetcher()
        data = fetcher.fetch_intraday()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条北向资金日内数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取北向资金日内数据失败: {e}")
        raise typer.Exit(code=1)
```

**Step 2: Create test file**

```python
# tests/test_cli/test_north_flow.py
import pytest
from typer.testing import CliRunner
from finscraper.cli.main import app


def test_north_flow_daily_command():
    runner = CliRunner()
    result = runner.invoke(app, ["north-flow", "daily", "--help"])
    assert result.exit_code == 0
    assert "daily" in result.output


def test_north_flow_intraday_command():
    runner = CliRunner()
    result = runner.invoke(app, ["north-flow", "intraday", "--help"])
    assert result.exit_code == 0
    assert "intraday" in result.output
```

**Step 3: Run tests**

Run: `pytest tests/test_cli/test_north_flow.py -v`
Expected: All tests pass

**Step 4: Commit**

```bash
git add finscraper/cli/commands/north_flow.py tests/test_cli/test_north_flow.py
git commit -m "feat: implement north-flow command group with real data"
```

---

## Task 3: Implement Sector Command Group

**Files:**
- Modify: `finscraper/cli/commands/sector.py`
- Test: `tests/test_cli/test_sector.py`

**Step 1: Update sector.py implementation**

```python
import typer
from typing_extensions import Annotated
from finscraper.fetchers.sector import SectorFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

sector_app = typer.Typer(
    name="sector",
    help="板块数据命令",
)


@sector_app.command("list")
def list_sectors(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
):
    """列出板块列表"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_list()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 个板块")
        
    except Exception as e:
        print_error(f"获取板块列表失败: {e}")
        raise typer.Exit(code=1)


@sector_app.command("spot")
def spot_sectors(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取板块实时行情"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条板块实时行情数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取板块实时行情失败: {e}")
        raise typer.Exit(code=1)


@sector_app.command("stocks")
def sector_stocks(
    sector: Annotated[
        str,
        typer.Argument(help="板块代码或名称"),
    ],
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取板块成分股"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_stocks(sector=sector)
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 只成分股")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取板块成分股失败: {e}")
        raise typer.Exit(code=1)
```

**Step 2: Create test file**

```python
# tests/test_cli/test_sector.py
import pytest
from typer.testing import CliRunner
from finscraper.cli.main import app


def test_sector_list_command():
    runner = CliRunner()
    result = runner.invoke(app, ["sector", "list", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output


def test_sector_spot_command():
    runner = CliRunner()
    result = runner.invoke(app, ["sector", "spot", "--help"])
    assert result.exit_code == 0
    assert "spot" in result.output


def test_sector_stocks_command():
    runner = CliRunner()
    result = runner.invoke(app, ["sector", "stocks", "--help"])
    assert result.exit_code == 0
    assert "stocks" in result.output
```

**Step 3: Run tests**

Run: `pytest tests/test_cli/test_sector.py -v`
Expected: All tests pass

**Step 4: Commit**

```bash
git add finscraper/cli/commands/sector.py tests/test_cli/test_sector.py
git commit -m "feat: implement sector command group with real data"
```

---

## Task 4: Run All CLI Tests

**Step 1: Run full CLI test suite**

Run: `pytest tests/test_cli/ -v`
Expected: All tests pass

**Step 2: Test CLI commands manually**

Run: `finscraper index --help`
Expected: Shows index command help

**Step 3: Commit**

```bash
git add tests/test_cli/
git commit -m "test: ensure all CLI tests pass"
```

---

## Task 5: Update Documentation

**Files:**
- Update: `README.md`

**Step 1: Update README with working CLI examples**

```markdown
### CLI 使用

```bash
# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231

# 保存数据到文件
finscraper index spot --output-path data/index_spot.csv

# 获取北向资金日数据
finscraper north-flow daily

# 获取板块列表
finscraper sector list

# 获取板块实时行情
finscraper sector spot

# JSON 输出
finscraper index spot --format json
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with working CLI examples"
```

---

## Summary

This plan implements the core CLI commands:

1. ✅ Index command group (list, spot, history) - connects to IndexFetcher
2. ✅ North-Flow command group (daily, intraday) - connects to NorthFlowFetcher
3. ✅ Sector command group (list, spot, stocks) - connects to SectorFetcher
4. ✅ Run all CLI tests
5. ✅ Update documentation

**Note:** Commodity, Money-Flow, and News commands remain as stubs until their corresponding Fetchers are implemented in Phase 6.

**Next Steps:** Proceed to Phase 6 (Full Data Fetchers) after completing this plan.
