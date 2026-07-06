from pathlib import Path


def create_empty_dir(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def create_empty_file(file: Path) -> Path:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch(exist_ok=True)
    return file


def init_py_module(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    init = directory / "__init__.py"
    init.touch(exist_ok=True)
    return init


def create_module_path(directory: Path) -> Path:
    create_empty_dir(directory)
    init_py_module(directory)
    return directory


def insert_line_before_marker(
    file_path: Path,
    marker: str,
    line: str,
) -> bool:
    content = file_path.read_text(encoding="utf-8")

    if line in content.splitlines():
        return False

    if marker not in content:
        raise ValueError(f"Marker {marker!r} was not found in {file_path}")

    updated_content = content.replace(marker, f"{line}\n{marker}", 1)
    file_path.write_text(updated_content, encoding="utf-8")
    return True
