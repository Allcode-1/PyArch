import subprocess
from collections.abc import Callable
from typing import Never, TypeVar

import typer
from rich.console import Console


console = Console()
ResultT = TypeVar("ResultT")


def execute_or_exit(action: Callable[[], ResultT]) -> ResultT:
    try:
        return action()
    except (
        FileExistsError,
        FileNotFoundError,
        NotImplementedError,
        subprocess.CalledProcessError,
        ValueError,
    ) as error:
        abort(str(error))


def abort(message: str) -> Never:
    console.print(f"[bold red]Error:[/bold red] {message}")
    raise typer.Exit(code=1)
