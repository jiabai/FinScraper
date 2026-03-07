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
