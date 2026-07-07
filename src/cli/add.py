from typing import Annotated

import typer

from src.cli.common import console, execute_or_exit
from src.services.add_integration import add_integration


app = typer.Typer(no_args_is_help=True)


@app.command("integration")
def add_integration_command(
    integration_name: Annotated[
        str,
        typer.Argument(help="Integration name."),
    ],
) -> None:
    """Add a supported integration to the current project."""

    project_root, created_files = execute_or_exit(lambda: add_integration(integration_name))
    console.print(
        f"[green]Added integration[/green] [bold]{integration_name}[/bold]"
        f" in {project_root}"
    )
    for file_path in created_files:
        console.print(f"  [dim]{file_path.relative_to(project_root)}[/dim]")
