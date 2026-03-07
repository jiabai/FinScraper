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
