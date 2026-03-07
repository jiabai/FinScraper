# Phase 3: CLI Framework Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the CLI framework using Typer, including main entry point, global options, and utility functions.

**Architecture:** Command-based CLI with Typer framework. Global options (--version, --help, --verbose, --config) handle logging and configuration. Utility functions provide output formatting, progress bars, and color output.

**Tech Stack:** Python 3.10+, Typer 0.12+, Rich 13.0+

---

## Task 1: Verify Typer Dependency

**Files:**
- Verify: `pyproject.toml`

**Step 1: Check pyproject.toml for typer dependency**

Read: `pyproject.toml`
Verify: `"typer>=0.12.0"` exists in dependencies

**Step 2: Verify entry points configuration**

Check: `[project.scripts]` section exists
Verify: `finscraper = "finscraper.cli.main:app"` configured

**Step 3: Install dependencies if needed**

Run: `pip install -e .`
Expected: Typer and dependencies installed

**Step 4: Verify installation**

Run: `python -c "import typer; print(typer.__version__)"`
Expected: Typer version printed

**Step 5: Commit (if changes needed)**

```bash
git add pyproject.toml
git commit -m "chore: ensure typer dependency is present"
```

---

## Task 2: Create CLI Main Entry Point

**Files:**
- Create: `finscraper/cli/__init__.py`
- Create: `finscraper/cli/main.py`
- Create: `tests/test_cli/__init__.py`
- Create: `tests/test_cli/test_main.py`

**Step 1: Write the failing test**

```python
# tests/test_cli/test_main.py
import pytest
from typer.testing import CliRunner
from finscraper.cli.main import app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "FinScraper" in result.output
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_main.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Create CLI module structure**

Create: `finscraper/cli/__init__.py`
Create: `tests/test_cli/__init__.py`

**Step 4: Write minimal implementation**

```python
# finscraper/cli/main.py
import typer
from typing_extensions import Annotated

app = typer.Typer(
    name="finscraper",
    help="基于 akshare 的金融数据获取工具",
    add_completion=False,
)


def version_callback(value: bool):
    if value:
        typer.echo("FinScraper v0.1.0")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="显示版本信息",
        ),
    ] = False,
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
            help="详细日志级别 (-v=INFO, -vv=DEBUG)",
        ),
    ] = 0,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="安静模式，只显示错误",
        ),
    ] = False,
    config: Annotated[
        str,
        typer.Option(
            "--config",
            "-c",
            help="指定配置文件路径",
            exists=True,
            file_okay=True,
            dir_okay=False,
        ),
    ] = None,
):
    """FinScraper CLI - 金融数据获取工具"""
    pass


if __name__ == "__main__":
    app()
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_cli/test_main.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/cli/ tests/test_cli/
git commit -m "feat: add CLI main entry point with basic commands"
```

---

## Task 3: Implement Global Options Handler

**Files:**
- Create: `finscraper/cli/utils.py`
- Create: `tests/test_cli/test_utils.py`

**Step 1: Write the failing test**

```python
# tests/test_cli/test_utils.py
import pytest
from finscraper.cli.utils import get_log_level, configure_logging


def test_get_log_level():
    assert get_log_level(0) == "WARNING"
    assert get_log_level(1) == "INFO"
    assert get_log_level(2) == "DEBUG"
    assert get_log_level(3) == "DEBUG"


def test_configure_logging():
    import os
    from finscraper.core.logger import get_logger
    
    configure_logging(verbose=1, quiet=False)
    
    # Check that log level is set
    assert "FINSCRAPER_LOG_LEVEL" in os.environ
    assert os.environ["FINSCRAPER_LOG_LEVEL"] == "INFO"
    
    # Reset
    configure_logging(verbose=0, quiet=False)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_utils.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# finscraper/cli/utils.py
import os
from finscraper.core.logger import set_log_level


def get_log_level(verbose: int) -> str:
    """Get log level from verbose count."""
    if verbose >= 2:
        return "DEBUG"
    elif verbose == 1:
        return "INFO"
    return "WARNING"


def configure_logging(verbose: int, quiet: bool):
    """Configure logging based on CLI options."""
    if quiet:
        level = "ERROR"
    else:
        level = get_log_level(verbose)
    
    set_log_level(level)
    os.environ["FINSCRAPER_LOG_LEVEL"] = level


def format_table(data, headers=None):
    """Format data as a table."""
    if not data:
        return "No data"
    
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    table = Table()
    
    if headers:
        for header in headers:
            table.add_column(header)
    else:
        for key in data[0].keys():
            table.add_column(str(key))
    
    for row in data:
        table.add_row(*[str(value) for value in row.values()])
    
    with console.capture() as capture:
        console.print(table)
    
    return capture.get()
```

**Step 4: Update main.py to use logging configuration**

```python
# finscraper/cli/main.py
from finscraper.cli.utils import configure_logging

@app.callback()
def main(
    ...,
):
    """FinScraper CLI - 金融数据获取工具"""
    configure_logging(verbose, quiet)
    pass
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_cli/test_utils.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/cli/utils.py tests/test_cli/test_utils.py finscraper/cli/main.py
git commit -m "feat: add global options handler and logging config"
```

---

## Task 4: Implement Output Formatting Utilities

**Files:**
- Modify: `finscraper/cli/utils.py`
- Create: `tests/test_cli/test_output.py`

**Step 1: Write the failing test**

```python
# tests/test_cli/test_output.py
import pytest
import pandas as pd
from finscraper.cli.utils import (
    format_table,
    format_json,
    output_data,
)


def test_format_table():
    data = [
        {"symbol": "000001", "name": "上证指数", "price": 3000.0},
        {"symbol": "399001", "name": "深证成指", "price": 10000.0},
    ]
    
    result = format_table(data)
    assert "000001" in result
    assert "上证指数" in result


def test_format_json():
    data = [
        {"symbol": "000001", "name": "上证指数", "price": 3000.0},
    ]
    
    result = format_json(data)
    assert '"symbol": "000001"' in result


def test_output_data():
    df = pd.DataFrame({
        "symbol": ["000001", "399001"],
        "name": ["上证指数", "深证成指"],
        "price": [3000.0, 10000.0],
    })
    
    result = output_data(df, format="table")
    assert "000001" in result
    
    result = output_data(df, format="json")
    assert '"symbol": "000001"' in result
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_output.py -v`
Expected: FAIL with missing functions

**Step 3: Write implementation**

```python
# finscraper/cli/utils.py
import json
import pandas as pd
from rich.console import Console
from rich.table import Table


def format_table(data, headers=None):
    """Format data as a table."""
    if not data:
        return "No data"
    
    console = Console()
    table = Table()
    
    if headers:
        for header in headers:
            table.add_column(header)
    else:
        for key in data[0].keys():
            table.add_column(str(key))
    
    for row in data:
        table.add_row(*[str(value) for value in row.values()])
    
    with console.capture() as capture:
        console.print(table)
    
    return capture.get()


def format_json(data):
    """Format data as JSON."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def output_data(data, format="table"):
    """Output data in specified format."""
    if isinstance(data, pd.DataFrame):
        data = data.to_dict("records")
    
    if format == "json":
        return format_json(data)
    elif format == "table":
        return format_table(data)
    else:
        return format_table(data)


def save_data(data, path, format="csv"):
    """Save data to file."""
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        df = pd.DataFrame(data)
    
    if format == "csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
    elif format == "json":
        df.to_json(path, orient="records", force_ascii=False, indent=2)
    elif format == "parquet":
        df.to_parquet(path, index=False)
    elif format == "sqlite":
        import sqlite3
        conn = sqlite3.connect(path)
        df.to_sql("data", conn, if_exists="replace", index=False)
        conn.close()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli/test_output.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/cli/utils.py tests/test_cli/test_output.py
git commit -m "feat: add output formatting utilities"
```

---

## Task 5: Implement Progress Bar Utilities

**Files:**
- Modify: `finscraper/cli/utils.py`
- Create: `tests/test_cli/test_progress.py`

**Step 1: Write the failing test**

```python
# tests/test_cli/test_progress.py
import pytest
from finscraper.cli.utils import ProgressBar


def test_progress_bar_init():
    pb = ProgressBar(total=100, description="Downloading")
    assert pb.total == 100
    assert pb.description == "Downloading"


def test_progress_bar_update():
    pb = ProgressBar(total=10, description="Testing")
    pb.update(3)
    assert pb.current == 3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_progress.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write implementation**

```python
# finscraper/cli/utils.py
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)


class ProgressBar:
    """Progress bar wrapper for CLI."""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.current = 0
        self._progress = None
        self._task = None
    
    def __enter__(self):
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
        )
        self._progress.start()
        self._task = self._progress.add_task(
            self.description,
            total=self.total,
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._progress:
            self._progress.stop()
    
    def update(self, advance: int = 1):
        """Update progress bar."""
        self.current += advance
        if self._progress and self._task:
            self._progress.update(self._task, advance=advance)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli/test_progress.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/cli/utils.py tests/test_cli/test_progress.py
git commit -m "feat: add progress bar utilities"
```

---

## Task 6: Implement Color Output Utilities

**Files:**
- Modify: `finscraper/cli/utils.py`
- Create: `tests/test_cli/test_color.py`

**Step 1: Write the failing test**

```python
# tests/test_cli/test_color.py
import pytest
from finscraper.cli.utils import (
    print_success,
    print_warning,
    print_error,
    print_info,
)


def test_print_success():
    from rich.console import Console
    from rich.text import Text
    
    console = Console()
    with console.capture() as capture:
        print_success("Test message")
    
    output = capture.get()
    assert "Test message" in output


def test_print_warning():
    from rich.console import Console
    
    console = Console()
    with console.capture() as capture:
        print_warning("Warning message")
    
    output = capture.get()
    assert "Warning message" in output
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_color.py -v`
Expected: FAIL with "function not found"

**Step 3: Write implementation**

```python
# finscraper/cli/utils.py
from rich.console import Console
from rich.text import Text


console = Console()


def print_success(message: str):
    """Print success message in green."""
    text = Text("✓ ", style="green") + Text(message)
    console.print(text)


def print_warning(message: str):
    """Print warning message in yellow."""
    text = Text("⚠ ", style="yellow") + Text(message)
    console.print(text)


def print_error(message: str):
    """Print error message in red."""
    text = Text("✗ ", style="red") + Text(message)
    console.print(text)


def print_info(message: str):
    """Print info message in blue."""
    text = Text("ℹ ", style="blue") + Text(message)
    console.print(text)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli/test_color.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add finscraper/cli/utils.py tests/test_cli/test_color.py
git commit -m "feat: add color output utilities"
```

---

## Task 7: Add Index Command Group (Stub)

**Files:**
- Create: `finscraper/cli/commands/index.py`
- Modify: `finscraper/cli/main.py`
- Create: `tests/test_cli/test_index.py`

**Step 1: Write the failing test**

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

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli/test_index.py -v`
Expected: FAIL with "No such command"

**Step 3: Create index command module**

```python
# finscraper/cli/commands/index.py
import typer
from typing_extensions import Annotated

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
    typer.echo("Index list command - coming soon")


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
    typer.echo("Index spot command - coming soon")


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
    typer.echo("Index history command - coming soon")
```

**Step 4: Update main.py to add index command group**

```python
# finscraper/cli/main.py
from finscraper.cli.commands.index import index_app

app.add_typer(index_app, name="index", help="A 股指数命令")
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_cli/test_index.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add finscraper/cli/commands/index.py finscraper/cli/main.py tests/test_cli/test_index.py
git commit -m "feat: add index command group (stub)"
```

---

## Task 8: Add Remaining Command Groups (Stubs)

**Files:**
- Create: `finscraper/cli/commands/__init__.py`
- Create: `finscraper/cli/commands/north_flow.py`
- Create: `finscraper/cli/commands/sector.py`
- Create: `finscraper/cli/commands/commodity.py`
- Create: `finscraper/cli/commands/money_flow.py`
- Create: `finscraper/cli/commands/news.py`
- Create: `finscraper/cli/commands/fetch_all.py`
- Modify: `finscraper/cli/main.py`

**Step 1: Create command module structure**

Create: `finscraper/cli/commands/__init__.py`

**Step 2: Create north-flow command**

```python
# finscraper/cli/commands/north_flow.py
import typer
from typing_extensions import Annotated

north_flow_app = typer.Typer(
    name="north-flow",
    help="北向资金命令",
)


@north_flow_app.command("daily")
def north_flow_daily():
    """获取单日数据"""
    typer.echo("North flow daily command - coming soon")


@north_flow_app.command("intraday")
def north_flow_intraday():
    """获取分时数据"""
    typer.echo("North flow intraday command - coming soon")
```

**Step 3: Create sector command**

```python
# finscraper/cli/commands/sector.py
import typer
from typing_extensions import Annotated

sector_app = typer.Typer(
    name="sector",
    help="板块数据命令",
)


@sector_app.command("list")
def list_sectors():
    """列出板块"""
    typer.echo("Sector list command - coming soon")


@sector_app.command("spot")
def spot_sectors():
    """板块实时行情"""
    typer.echo("Sector spot command - coming soon")


@sector_app.command("stocks")
def sector_stocks():
    """板块成分股"""
    typer.echo("Sector stocks command - coming soon")
```

**Step 4: Create commodity command**

```python
# finscraper/cli/commands/commodity.py
import typer
from typing_extensions import Annotated

commodity_app = typer.Typer(
    name="commodity",
    help="大宗商品命令",
)


@commodity_app.command("list")
def list_commodities():
    """列出商品"""
    typer.echo("Commodity list command - coming soon")


@commodity_app.command("spot")
def spot_commodities():
    """实时行情"""
    typer.echo("Commodity spot command - coming soon")


@commodity_app.command("history")
def history_commodity(
    symbol: Annotated[
        str,
        typer.Argument(help="商品代码"),
    ],
):
    """历史数据"""
    typer.echo("Commodity history command - coming soon")
```

**Step 5: Create money-flow command**

```python
# finscraper/cli/commands/money_flow.py
import typer
from typing_extensions import Annotated

money_flow_app = typer.Typer(
    name="money-flow",
    help="资金流向命令",
)


@money_flow_app.command("stock")
def stock_money_flow(
    symbol: Annotated[
        str,
        typer.Argument(help="股票代码"),
    ],
):
    """个股资金流"""
    typer.echo("Stock money flow command - coming soon")


@money_flow_app.command("sector")
def sector_money_flow():
    """板块资金流"""
    typer.echo("Sector money flow command - coming soon")


@money_flow_app.command("market")
def market_money_flow():
    """两市资金流"""
    typer.echo("Market money flow command - coming soon")
```

**Step 6: Create news command**

```python
# finscraper/cli/commands/news.py
import typer
from typing_extensions import Annotated

news_app = typer.Typer(
    name="news",
    help="新闻命令",
)


@news_app.command("global")
def global_news():
    """全球财经资讯"""
    typer.echo("Global news command - coming soon")


@news_app.command("alert")
def stock_alert():
    """A 股公告"""
    typer.echo("Stock alert command - coming soon")


@news_app.command("stock")
def stock_news(
    symbol: Annotated[
        str,
        typer.Argument(help="股票代码"),
    ],
):
    """个股资讯"""
    typer.echo("Stock news command - coming soon")
```

**Step 7: Create fetch-all command**

```python
# finscraper/cli/commands/fetch_all.py
import typer

fetch_all_app = typer.Typer(
    name="fetch-all",
    help="一键获取所有数据",
)


@fetch_all_app.callback(invoke_without_command=True)
def fetch_all():
    """一键获取所有数据"""
    typer.echo("Fetch all command - coming soon")
```

**Step 8: Update main.py to add all command groups**

```python
# finscraper/cli/main.py
from finscraper.cli.commands.north_flow import north_flow_app
from finscraper.cli.commands.sector import sector_app
from finscraper.cli.commands.commodity import commodity_app
from finscraper.cli.commands.money_flow import money_flow_app
from finscraper.cli.commands.news import news_app
from finscraper.cli.commands.fetch_all import fetch_all_app

app.add_typer(north_flow_app, name="north-flow", help="北向资金命令")
app.add_typer(sector_app, name="sector", help="板块数据命令")
app.add_typer(commodity_app, name="commodity", help="大宗商品命令")
app.add_typer(money_flow_app, name="money-flow", help="资金流向命令")
app.add_typer(news_app, name="news", help="新闻命令")
app.add_typer(fetch_all_app, name="fetch-all", help="一键获取所有数据")
```

**Step 9: Test all commands**

Run: `finscraper --help`
Expected: All commands listed

**Step 10: Commit**

```bash
git add finscraper/cli/commands/ finscraper/cli/main.py
git commit -m "feat: add all command groups (stubs)"
```

---

## Task 9: Run All CLI Tests

**Step 1: Run full CLI test suite**

Run: `pytest tests/test_cli/ -v`
Expected: All tests pass

**Step 2: Test CLI invocation**

Run: `finscraper --help`
Expected: Help message displayed

Run: `finscraper --version`
Expected: Version displayed

Run: `finscraper index --help`
Expected: Index command help displayed

**Step 3: Commit**

```bash
git add tests/test_cli/
git commit -m "test: ensure all CLI tests pass"
```

---

## Task 10: Update Documentation

**Files:**
- Update: `README.md`

**Step 1: Update README with CLI usage**

```markdown
# FinScraper

基于 akshare 的金融数据获取工具，支持 CLI 和 Python API。

## 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用

```bash
# 显示帮助
finscraper --help

# 显示版本
finscraper --version

# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101 --end-date 20241231

# 获取北向资金
finscraper north-flow daily

# 获取板块数据
finscraper sector spot

# 获取大宗商品
finscraper commodity spot

# 获取资金流向
finscraper money-flow stock 000001

# 获取新闻
finscraper news global

# 一键获取所有数据
finscraper fetch-all
```

## CLI 命令

### index - A 股指数
```bash
finscraper index list           # 列出可用指数
finscraper index spot           # 获取实时行情
finscraper index history        # 获取历史数据
```

### north-flow - 北向资金
```bash
finscraper north-flow daily     # 获取单日数据
finscraper north-flow intraday  # 获取分时数据
```

### sector - 板块数据
```bash
finscraper sector list          # 列出板块
finscraper sector spot          # 板块实时行情
finscraper sector stocks        # 板块成分股
```

### commodity - 大宗商品
```bash
finscraper commodity list       # 列出商品
finscraper commodity spot       # 实时行情
finscraper commodity history    # 历史数据
```

### money-flow - 资金流向
```bash
finscraper money-flow stock     # 个股资金流
finscraper money-flow sector    # 板块资金流
finscraper money-flow market    # 两市资金流
```

### news - 新闻
```bash
finscraper news global          # 全球财经资讯
finscraper news alert           # A 股公告
finscraper news stock           # 个股资讯
```

### fetch-all - 一键获取
```bash
finscraper fetch-all            # 一键获取所有数据
```

## 全局选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--help` | `-h` | 显示帮助 |
| `--version` | `-V` | 显示版本 |
| `--config` | `-c` | 指定配置文件 |
| `--verbose` | `-v` | 详细日志 (-v=INFO, -vv=DEBUG) |
| `--quiet` | `-q` | 安静模式 |
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README with CLI usage"
```

---

## Summary

This plan implements the CLI framework for FinScraper:

1. ✅ Verify Typer dependency
2. ✅ CLI main entry point with basic commands
3. ✅ Global options handler (--version, --help, --verbose, --config)
4. ✅ Output formatting utilities (table, JSON)
5. ✅ Progress bar utilities
6. ✅ Color output utilities
7. ✅ Index command group (stub)
8. ✅ All command groups (stubs)
9. ✅ Run all CLI tests
10. ✅ Update documentation

**Next Steps:** Proceed to Phase 4 (CLI Command Implementation) after completing this plan.
