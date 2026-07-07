from pathlib import Path

from src.generators.common.commands import run_command
from src.generators.common.filesystem import create_empty_dir, create_empty_file
from src.generators.common.gitignore import (
    BASE_GITIGNORE_ENTRIES,
    ensure_gitignore_entries,
)
from src.generators.common.renderer import create_file_from_template


def create_base_dir(project_name: str) -> Path:
    """
    create base dir with all README.md, gitignore, ,env.example and etc files
    """

    project_dir = Path.cwd() / project_name

    # creating base uv app
    run_command("uv", "init", project_name)
    ensure_gitignore_entries(project_dir, "base", BASE_GITIGNORE_ENTRIES)

    # files shared by all supported architectures
    create_empty_file(project_dir / "Dockerfile")
    create_empty_file(project_dir / "docker-compose.yml")

    create_docs_dir(project_dir)

    return project_dir


def create_docs_dir(project_dir: Path) -> None:
    """
    creating files where you can describe your project, rbac roles etc.
    """

    docs_dir = create_empty_dir(project_dir / "docs")
    create_empty_file(docs_dir / "RBAC.md")
    create_empty_file(docs_dir / "ARCHITECTURE.md")


def create_readme_file(
    project_dir: Path,
    project_name: str,
    database: str,
) -> None:
    create_file_from_template(
        template_name="project/base/README.md.j2",
        output_path=project_dir / "README.md",
        project_name=project_name,
        database=database,
    )
