import typer
from typing_extensions import Annotated
from finscraper.fetchers.sector import SectorFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

sector_app = typer.Typer(
    name="sector",
    help="板块数据命令",
)


@sector_app.command("list")
def list_sectors(
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="输出格式 (table|json)",
        ),
    ] = "table",
):
    """列出可用板块"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output = output_data(data, format=format)
        typer.echo(output)
        print_success(f"成功获取 {len(data)} 条板块数据")
        
    except Exception as e:
        print_error(f"获取板块列表失败: {e}")
        raise typer.Exit(code=1)


@sector_app.command("spot")
def spot_sectors(
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
    """获取板块实时行情（包含板块列表）"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条板块实时行情数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取板块实时行情失败: {e}")
        raise typer.Exit(code=1)


@sector_app.command("stocks")
def sector_stocks(
    sector_code: Annotated[
        str,
        typer.Argument(help="板块代码"),
    ],
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
    """获取板块成分股"""
    try:
        fetcher = SectorFetcher()
        data = fetcher.fetch_spot()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format=format)
        typer.echo(output_data_str)
        print_success(f"成功获取板块成分股数据")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取板块成分股失败: {e}")
        raise typer.Exit(code=1)
