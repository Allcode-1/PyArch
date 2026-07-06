from pathlib import Path

from src.config.manifest import find_project_root, load_manifest


def add_integration(
    integration_name: str,
    start: Path | None = None,
) -> None:
    project_root = find_project_root(start)
    manifest = load_manifest(project_root)
    normalized_name = integration_name.strip().lower().replace("-", "_")

    if not normalized_name:
        raise ValueError("Integration name cannot be empty")

    if normalized_name in manifest.state.integrations:
        raise FileExistsError(
            f"Integration {normalized_name!r} is already registered"
        )

    raise NotImplementedError(
        f"Integration {normalized_name!r} does not have a generator yet"
    )
