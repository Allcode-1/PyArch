
from pathlib import Path

from pyarch.config.manifest import create_manifest
from pyarch.config.models import DatabaseEngine
from pyarch.generators.project.base import create_base_dir, create_readme_file
from pyarch.generators.project.layered import create_layered_project


def create_project(
    project_name: str,
    database: DatabaseEngine | str = DatabaseEngine.POSTGRES,
) -> Path:
    database = DatabaseEngine(database)

    project_dir = create_base_dir(project_name)
    create_layered_project(project_dir, database)
    create_readme_file(project_dir, project_name, database.value)
    create_manifest(project_dir, project_name, database)
    return project_dir
