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
