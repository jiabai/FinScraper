import typer

fetch_all_app = typer.Typer(
    name="fetch-all",
    help="一键获取所有数据",
)


@fetch_all_app.callback(invoke_without_command=True)
def fetch_all():
    """一键获取所有数据"""
    typer.echo("Fetch all command - coming soon")
