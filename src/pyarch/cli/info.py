import typer

from rich.table import Table
from pyarch.cli.common import console, execute_or_exit
from pyarch.config.manifest import load_current_manifest


app = typer.Typer(no_args_is_help=True)


@app.command("help")
def show_info() -> None:
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


