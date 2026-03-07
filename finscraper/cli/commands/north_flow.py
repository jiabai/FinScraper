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
