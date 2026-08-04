from typing import Annotated

import typer

from pyarch.cli.common import console, execute_or_exit
from pyarch.services.create_module import create_module


app = typer.Typer(no_args_is_help=True)


@app.command("module")
def generate_module(
    module_name: Annotated[str, typer.Argument(help="Module name.")],
    protected: Annotated[
        bool,
        typer.Option(
            "--protected",
            help="Protect generated routes with the auth integration.",
        ),
    ] = False,
) -> None:
    """Generate a CRUD module using the project's manifest."""

    project_root, created_files = execute_or_exit(
        lambda: create_module(module_name, protected=protected)
    )

    console.print(
        f"[green]Created module[/green] [bold]{module_name}[/bold] "
        f"in {project_root}"
    )
    for file_path in created_files:
        console.print(f"  [dim]{file_path.relative_to(project_root)}[/dim]")
