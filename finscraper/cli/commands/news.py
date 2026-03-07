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
