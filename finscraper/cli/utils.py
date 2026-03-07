import os
import json
import pandas as pd
from finscraper.core.logger import set_log_level
from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from rich.text import Text


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
