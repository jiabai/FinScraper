import typer
from typing_extensions import Annotated
from finscraper.fetchers.north_flow import NorthFlowFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

north_flow_app = typer.Typer(
    name="north-flow",
    help="北向资金命令",
)


@north_flow_app.command("daily")
def daily_north_flow(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取北向资金日数据"""
    try:
        fetcher = NorthFlowFetcher()
        data = fetcher.fetch_daily()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条北向资金日数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取北向资金日数据失败: {e}")
        raise typer.Exit(code=1)


@north_flow_app.command("intraday")
def intraday_north_flow(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            "-p",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取北向资金日内数据"""
    try:
        fetcher = NorthFlowFetcher()
        data = fetcher.fetch_intraday()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条北向资金日内数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取北向资金日内数据失败: {e}")
        raise typer.Exit(code=1)
