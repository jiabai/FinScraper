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
