import subprocess
from pathlib import Path


def run_command(*command: str, cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd or Path.cwd(), check=True)
