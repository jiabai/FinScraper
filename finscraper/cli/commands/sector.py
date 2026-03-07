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
