from typing import Annotated

import typer

from pyarch.cli.common import console, execute_or_exit
from pyarch.config.models import DatabaseEngine
from pyarch.services.create_project import create_project


app = typer.Typer(no_args_is_help=True)


@app.command("init")
def init_project(
    project_name: Annotated[
        str,
        typer.Argument(help="New project directory name."),
    ],
    database: Annotated[
        DatabaseEngine,
        typer.Option(
            "--database",
            "-d",
            help="Database backend.",
            case_sensitive=False,
        ),
    ] = DatabaseEngine.POSTGRES,
) -> None:
    """Create a new Layered FastAPI project."""

    console.print(
        f"Creating [bold]{project_name}[/bold] "
        f"with [cyan]{database.value}[/cyan]..."
    )
    project_dir = execute_or_exit(
        lambda: create_project(project_name, database)
    )
    console.print(f"[bold green]Project created:[/bold green] {project_dir}")
