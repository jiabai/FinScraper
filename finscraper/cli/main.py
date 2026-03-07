import typer
from typing_extensions import Annotated
from finscraper.cli.utils import configure_logging
from finscraper.cli.commands.index import index_app
from finscraper.cli.commands.north_flow import north_flow_app
from finscraper.cli.commands.sector import sector_app
from finscraper.cli.commands.commodity import commodity_app
from finscraper.cli.commands.money_flow import money_flow_app
from finscraper.cli.commands.news import news_app
from finscraper.cli.commands.fetch_all import fetch_all_app

app = typer.Typer(
    name="finscraper",
    help="基于 akshare 的金融数据获取工具",
    add_completion=False,
)


def version_callback(value: bool):
    if value:
        typer.echo("FinScraper v1.0.0")
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
    configure_logging(verbose, quiet)


app.add_typer(index_app, name="index", help="A 股指数命令")
app.add_typer(north_flow_app, name="north-flow", help="北向资金命令")
app.add_typer(sector_app, name="sector", help="板块数据命令")
app.add_typer(commodity_app, name="commodity", help="大宗商品命令")
app.add_typer(money_flow_app, name="money-flow", help="资金流向命令")
app.add_typer(news_app, name="news", help="新闻命令")
app.add_typer(fetch_all_app, name="fetch-all", help="一键获取所有数据")


if __name__ == "__main__":
    app()
