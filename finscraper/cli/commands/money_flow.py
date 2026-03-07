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
