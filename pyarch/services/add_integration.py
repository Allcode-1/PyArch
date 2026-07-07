from pathlib import Path

from pyarch.config.manifest import find_project_root, load_manifest, save_manifest
from pyarch.generators.integration.auth import (
    AUTH_INTEGRATION_NAME,
    create_auth_integration,
)


def add_integration(
    integration_name: str,
    start: Path | None = None,
) -> tuple[Path, tuple[Path, ...]]:
    project_root = find_project_root(start)
    manifest = load_manifest(project_root)
    normalized_name = integration_name.strip().lower().replace("-", "_")

    if not normalized_name:
        raise ValueError("Integration name cannot be empty")

    if normalized_name in manifest.state.integrations:
        raise FileExistsError(
            f"Integration {normalized_name!r} is already registered"
        )

    if normalized_name != AUTH_INTEGRATION_NAME:
        raise NotImplementedError(
            f"Integration {normalized_name!r} does not have a generator yet"
        )

    created_files = create_auth_integration(
        project_root,
        manifest.database.engine,
    )
    manifest.state.integrations.append(normalized_name)
    save_manifest(project_root, manifest)
    return project_root, created_files
