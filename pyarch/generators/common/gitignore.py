from pathlib import Path


BASE_GITIGNORE_ENTRIES = (
    ".env",
    ".env.*",
    "!.env.example",
    ".venv",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    ".coverage",
    "htmlcov/",
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "dist/",
    "build/",
    "*.egg-info",
)

AUTH_GITIGNORE_ENTRIES = (
    "certs/",
    "*.pem",
    "*.key",
)


def ensure_gitignore_entries(
    project_dir: Path,
    section_name: str,
    entries: tuple[str, ...],
) -> Path:
    gitignore_path = project_dir / ".gitignore"
    content = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    lines = content.splitlines()
    existing_entries = {line.strip() for line in lines}

    missing_entries = [entry for entry in entries if entry not in existing_entries]
    if not missing_entries:
        return gitignore_path

    marker = f"# pyarch:{section_name}"
    if marker in lines:
        insert_at = find_section_end(lines, marker)
        updated_lines = [*lines[:insert_at], *missing_entries, *lines[insert_at:]]
    else:
        updated_lines = [*lines]
        if updated_lines and updated_lines[-1] != "":
            updated_lines.append("")
        updated_lines.extend((marker, *missing_entries))

    gitignore_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    return gitignore_path


def find_section_end(lines: list[str], marker: str) -> int:
    marker_index = lines.index(marker)

    for index in range(marker_index + 1, len(lines)):
        line = lines[index]
        if line == "" or line.startswith("# pyarch:"):
            return index

    return len(lines)
