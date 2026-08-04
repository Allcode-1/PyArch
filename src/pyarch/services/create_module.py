from pathlib import Path

from pyarch.config.manifest import find_project_root, load_manifest, save_manifest
from pyarch.config.models import Architecture
from pyarch.generators.integration.auth import AUTH_INTEGRATION_NAME
from pyarch.generators.module.layered import (
    create_layered_module,
    normalize_module_name,
)


def create_module(
    module_name: str,
    start: Path | None = None,
    protected: bool = False,
) -> tuple[Path, tuple[Path, ...]]:
    project_root = find_project_root(start)
    manifest = load_manifest(project_root)
    normalized_name = normalize_module_name(module_name)

    if normalized_name in manifest.state.modules:
        raise FileExistsError(
            f"Module {normalized_name!r} is already registered"
        )

    if manifest.project.architecture is not Architecture.LAYERED:
        raise ValueError(
            f"Unsupported architecture: {manifest.project.architecture.value}"
        )

    if protected and AUTH_INTEGRATION_NAME not in manifest.state.integrations:
        raise ValueError(
            "Protected module requires auth integration. "
            "Run `pyarch add integration auth` first."
        )

    created_files = create_layered_module(
        project_root,
        normalized_name,
        manifest.database.engine,
        protected=protected,
    )

    manifest.state.modules.append(normalized_name)
    save_manifest(project_root, manifest)
    return project_root, created_files
