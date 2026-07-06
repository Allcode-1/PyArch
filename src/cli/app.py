from typing import Annotated

import typer
from rich.table import Table

from src.cli.add import app as add_app
from src.cli.common import console, execute_or_exit
from src.cli.generate import app as generate_app
from src.config.manifest import find_project_root, load_manifest
from src.config.models import DatabaseEngine
from src.services.create_project import create_project


app = typer.Typer(
    name="pyarch",
    help="Generate and extend Layered FastAPI projects.",
    no_args_is_help=True,
)
app.add_typer(
    generate_app,
    name="generate",
    help="Generate project components.",
)
app.add_typer(
    add_app,
    name="add",
    help="Add project integrations.",
)


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


@app.command()
def info() -> None:
    """Show information from the current project's manifest."""

    project_root, manifest = execute_or_exit(load_current_manifest)

    table = Table(title="PyArch project", show_header=False)
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Root", str(project_root))
    table.add_row("Name", manifest.project.name)
    table.add_row("Architecture", manifest.project.architecture.value)
    table.add_row("Database", manifest.database.engine.value)
    table.add_row("DB access", manifest.database.access.value)
    table.add_row("Modules", ", ".join(manifest.state.modules) or "none")
    table.add_row(
        "Integrations",
        ", ".join(manifest.state.integrations) or "none",
    )
    console.print(table)


def load_current_manifest():
    project_root = find_project_root()
    return project_root, load_manifest(project_root)
