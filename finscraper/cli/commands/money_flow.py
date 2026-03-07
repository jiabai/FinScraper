import typer
from typing_extensions import Annotated
from finscraper.fetchers.money_flow import MoneyFlowFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

money_flow_app = typer.Typer(
    name="money-flow",
    help="资金流向命令",
)


@money_flow_app.command("stock")
def stock_money_flow(
    symbol: Annotated[
        str,
        typer.Argument(help="股票代码"),
    ] = "",
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
    """个股资金流"""
    try:
        fetcher = MoneyFlowFetcher()
        data = fetcher.fetch_stock()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条个股资金流数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取个股资金流失败: {e}")
        raise typer.Exit(code=1)


@money_flow_app.command("sector")
def sector_money_flow(
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
    """板块资金流"""
    try:
        fetcher = MoneyFlowFetcher()
        data = fetcher.fetch_sector()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条板块资金流数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取板块资金流失败: {e}")
        raise typer.Exit(code=1)


@money_flow_app.command("market")
def market_money_flow(
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
    """两市资金流"""
    try:
        fetcher = MoneyFlowFetcher()
        data = fetcher.fetch_market()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条两市资金流数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取两市资金流失败: {e}")
        raise typer.Exit(code=1)
