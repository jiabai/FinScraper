import typer
from typing_extensions import Annotated
from finscraper.fetchers.index import IndexFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

index_app = typer.Typer(
    name="index",
    help="A 股指数命令",
)


@index_app.command("list")
def list_indices(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
):
    """列出可用指数"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output = output_data(data, format=format)
        typer.echo(output)
        print_success(f"成功获取 {len(data)} 条指数数据")
        
    except Exception as e:
        print_error(f"获取指数列表失败: {e}")
        raise typer.Exit(code=1)


@index_app.command("spot")
def spot_indices(
    symbols: Annotated[
        str,
        typer.Option(
            "--symbols",
            "-s",
            help="指数代码（逗号分隔）",
        ),
    ] = None,
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
    """获取实时行情"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        if symbols:
            symbol_list = [s.strip() for s in symbols.split(",")]
            if "代码" in data.columns:
                data = data[data["代码"].isin(symbol_list)]
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条实时行情数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取实时行情失败: {e}")
        raise typer.Exit(code=1)


@index_app.command("history")
def history_index(
    symbol: Annotated[
        str,
        typer.Argument(help="指数代码"),
    ],
    start_date: Annotated[
        str,
        typer.Option(
            "--start-date",
            help="开始日期 (YYYYMMDD)",
        ),
    ] = "",
    end_date: Annotated[
        str,
        typer.Option(
            "--end-date",
            help="结束日期 (YYYYMMDD)",
        ),
    ] = "",
    period: Annotated[
        str,
        typer.Option(
            "--period",
            help="周期 (daily|weekly|monthly)",
        ),
    ] = "daily",
    output: Annotated[
        str,
        typer.Option(
            "--output",
            help="输出格式 (csv|json|parquet|sqlite)",
        ),
    ] = "csv",
    output_path: Annotated[
        str,
        typer.Option(
            "--output-path",
            help="输出文件路径",
        ),
    ] = None,
):
    """获取历史数据"""
    try:
        fetcher = IndexFetcher()
        data = fetcher.fetch_history(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            period=period,
        )
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条历史数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取历史数据失败: {e}")
        raise typer.Exit(code=1)
