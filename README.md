# PyArch

**PyArch is a stateful CLI that creates FastAPI projects and evolves them
through project-aware generation commands.**

It creates a backend project, stores its configuration in `pyarch.toml`, and
later uses that state to add modules and modify the existing application.

The CLI is the interface. The core idea is project-aware backend development
tooling built around a manifest, generators, templates, and FastAPI conventions.

```text
pyarch init
    ↓
Generated FastAPI project
    ↓
pyarch.toml
    ↓
pyarch generate module users
    ↓
Project is extended
    ↓
Manifest is updated
```

## Highlights

- Creates Layered FastAPI projects
- Supports PostgreSQL, SQLite and MongoDB
- Stateful project manifest (`pyarch.toml`)
- Project-aware module generation
- Automatic router and model registration
- Jinja2 template rendering with `StrictUndefined`
- Dependency installation via `uv`

## 30-second demo

```bash
$ pyarch init demo --database postgres

✓ Creating project...
✓ Installing dependencies...
✓ Configuring Alembic...
✓ Writing manifest...
✓ Done.

$ cd demo

$ pyarch generate module users

✓ Creating module...
✓ Registering model...
✓ Registering router...
✓ Updating manifest...
✓ Done.

$ pyarch info

Project: demo
Architecture: Layered
Database: PostgreSQL
Modules:
- users
```

## Why PyArch?

PyArch started as a tool to remove repetitive setup work in FastAPI projects:
database configuration, layered structure, Alembic setup, tests and CRUD wiring.

PyArch was inspired by the developer experience of Nest CLI, but is focused on
FastAPI projects and incremental project evolution.

Unlike one-shot template generators, PyArch keeps project state in a manifest
and uses it for later commands. The goal is not only to create the first project
structure, but also to extend the project after it already exists.

## Project Manifest

PyArch stores selected architecture, database backend, generated modules and
enabled integrations in `pyarch.toml`.

This allows later commands to understand and extend the existing project instead
of treating generation as a one-time template render.

The manifest currently records:

- schema version;
- PyArch version;
- project name;
- selected architecture;
- database engine;
- database access style;
- generated modules;
- enabled integrations;
- generated project paths.

## Generated Module Flow

```bash
pyarch generate module users
```

The module generator:

```text
pyarch generate module users
    ↓
read manifest
    ↓
detect backend
    ↓
render templates
    ↓
register model
    ↓
register router
    ↓
update manifest
```

## Architecture

```text
User
 │
 ▼
Typer CLI
 │
 ▼
Application Services
 │
 ▼
Generators
 │
 ├──────────────┐
 ▼              │
Jinja2          │
Templates       │
 │
 ▼              │
Filesystem      │
 │
 ▼              │
Generated Project
 ▲
 │
pyarch.toml
```

## Design Decisions

### Why a manifest instead of scanning the filesystem?

Scanning the filesystem can show which files exist, but it cannot reliably
explain why they exist or which generator state produced them. The manifest
stores project-level decisions such as architecture, database backend, generated
modules, integrations, paths, schema version, and PyArch version. Later commands
can read that state directly instead of guessing from folders and imports.

### Why marker-based registration instead of AST rewriting?

PyArch currently modifies files it generated itself, so explicit markers are
simple, readable, and predictable. For router and model registration, the tool
only needs stable insertion points, not a full Python code transformation
pipeline. AST rewriting may become useful later if PyArch needs to safely modify
arbitrary user-written code.

### Why Jinja2?

Generated FastAPI files are mostly structured text, and Jinja2 keeps templates
close to the final code that users will read. `StrictUndefined` makes template
errors fail fast when required context is missing. This keeps generators simple
while still making missing data visible during development.

## What Works Now

- creating a new Layered FastAPI project;
- choosing PostgreSQL, SQLite, or MongoDB during initialization;
- installing the matching runtime and development dependencies with `uv`;
- generating application layers, database configuration, test setup, and
  Alembic configuration for relational databases;
- generating a basic CRUD module after project creation;
- registering generated SQLAlchemy models in `app/models/__init__.py`;
- registering generated routers in `app/api/v1/router.py`;
- keeping project state in `pyarch.toml`;
- displaying the current project configuration through the CLI.

## Usage

Create a project:

```bash
pyarch init my_project
```

Select a database explicitly:

```bash
pyarch init my_project --database postgres
pyarch init my_project --database sqlite
pyarch init my_project --database mongodb
```

Move into the generated project and inspect its recorded state:

```bash
cd my_project
pyarch info
```

Generate a CRUD module:

```bash
pyarch generate module users
```

## Roadmap

### v0.2

- safe generation
- validation improvements
- rollback on failed generation
- integration generator foundation
- PyPI package publishing

### v0.3

- auth generator
- Redis integration
- scheduler integration
- dry-run mode

### Later

- new architectures
- plugin system
- async database access

## Generated Structure

<details>
<summary>Show generated project tree</summary>

A generated project currently follows this general structure:

```text
my_project/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── db/
│   ├── dependencies/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── docs/
├── tests/
├── alembic/          # PostgreSQL and SQLite only
├── .env.example
├── pyarch.toml
└── pyproject.toml
```

</details>

## Requirements

- Python 3.13 or newer;
- [uv](https://docs.astral.sh/uv/).

## Local Setup

Clone the repository and install its dependencies:

```bash
git clone <repository-url>
cd pathlib
uv sync
```

Run the CLI directly from the repository:

```bash
uv run pyarch --help
```

Install the current checkout as a local CLI tool:

```bash
uv tool install --editable .
```

## Project Status

**MVP+ — early development**

The first working CLI flow is in place. Commands, generated code, templates, and
the manifest format may still change while the project evolves.

## Current Limitations

- only Layered Architecture is supported;
- generated applications use synchronous database access;
- only FastAPI projects are supported;
- integration generators are planned, but not implemented yet;
- generated projects are starter scaffolds and still require application-specific
  configuration and code;
- the manifest format may change before a stable release.
