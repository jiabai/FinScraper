import typer
import pandas as pd
from typing_extensions import Annotated
from finscraper.fetchers.news import NewsFetcher
from finscraper.filters import TopicFilter, get_topics
from finscraper.cli.utils import (
    output_data,
    save_data,
    print_success,
    print_error,
    print_info,
)
import akshare as ak

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


@news_app.command("topics")
def list_topics():
    """列出所有可用专题"""
    try:
        topics = get_topics()
        print_info("可用专题列表:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
        print_success(f"共 {len(topics)} 个专题")
    except Exception as e:
        print_error(f"获取专题列表失败: {e}")
        raise typer.Exit(code=1)


@news_app.command("topic")
def topic_news(
    name: Annotated[
        str,
        typer.Option("--name", "-n", help="专题名称"),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="输出格式 (table|csv|json|parquet|sqlite)"),
    ] = "table",
    output_path: Annotated[
        str,
        typer.Option("--output-path", "-p", help="输出文件路径"),
    ] = None,
    urls_only: Annotated[
        bool,
        typer.Option("--urls-only", "-u", help="仅输出纯URL列表"),
    ] = False,
    brief: Annotated[
        bool,
        typer.Option("--brief", "-b", help="简要输出（标题、时间、摘要、链接）"),
    ] = False,
    match_content: Annotated[
        bool,
        typer.Option("--match-content", "-c", help="同时匹配新闻内容"),
    ] = False,
):
    """获取指定专题的新闻"""
    try:
        print_info(f"正在获取专题新闻: {name}")
        
        df = ak.stock_info_global_em()
        if df is None or df.empty:
            print_info("暂无新闻数据")
            return
        
        filter = TopicFilter()
        filtered_df = filter.filter_by_topic(
            df, 
            topic=name, 
            title_col="标题", 
            content_col="摘要" if match_content else None,
            match_content=match_content
        )
        
        if filtered_df is None or filtered_df.empty:
            print_info(f"专题 '{name}' 暂无相关新闻")
            return
        
        if urls_only:
            urls = filtered_df["链接"].tolist()
            print_success(f"找到 {len(urls)} 条相关新闻:")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
            
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    for url in urls:
                        f.write(f"{url}\n")
                print_success(f"URL列表已保存到: {output_path}")
            return
        
        if brief:
            print_success(f"找到 {len(filtered_df)} 条相关新闻:")
            print("=" * 80)
            
            output_lines = []
            for idx, row in filtered_df.iterrows():
                print(f"【{idx+1}】标题: {row['标题']}")
                print(f"  时间: {row.get('发布时间', 'N/A')}")
                print(f"  摘要: {row.get('摘要', 'N/A')[:100]}..." if pd.notna(row.get('摘要')) else "  摘要: N/A")
                print(f"  链接: {row['链接']}")
                print("-" * 80)
                
                output_line = f"标题: {row['标题']}\n时间: {row.get('发布时间', 'N/A')}\n摘要: {row.get('摘要', 'N/A')}\n链接: {row['链接']}\n{'='*80}\n"
                output_lines.append(output_line)
            
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.writelines(output_lines)
                print_success(f"数据已保存到: {output_path}")
            return
        
        print_info(f"找到 {len(filtered_df)} 条相关新闻")
        
        if output == "table":
            output_data_str = output_data(filtered_df, format="table")
            typer.echo(output_data_str)
        else:
            print_info(f"使用 {output} 格式输出")
        
        if output_path:
            save_data(filtered_df, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取专题新闻失败: {e}")
        raise typer.Exit(code=1)
