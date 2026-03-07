import typer
from typing_extensions import Annotated
from finscraper.fetchers.news import NewsFetcher
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)

news_app = typer.Typer(
    name="news",
    help="新闻命令",
)


@news_app.command("global")
def global_news(
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
    """全球财经资讯"""
    try:
        fetcher = NewsFetcher()
        data = fetcher.fetch_global()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条全球财经资讯")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取全球财经资讯失败: {e}")
        raise typer.Exit(code=1)


@news_app.command("alert")
def stock_alert(
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
    """A 股公告"""
    try:
        fetcher = NewsFetcher()
        data = fetcher.fetch_alert()
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条 A 股公告")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取 A 股公告失败: {e}")
        raise typer.Exit(code=1)


@news_app.command("stock")
def stock_news(
    symbol: Annotated[
        str,
        typer.Argument(help="股票代码"),
    ],
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
    """个股资讯"""
    try:
        fetcher = NewsFetcher()
        data = fetcher.fetch_stock(symbol=symbol)
        
        if data is None or data.empty:
            print_info("暂无数据")
            return
        
        output_data_str = output_data(data, format="table")
        typer.echo(output_data_str)
        print_success(f"成功获取 {len(data)} 条个股资讯")
        
        if output_path:
            save_data(data, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取个股资讯失败: {e}")
        raise typer.Exit(code=1)
