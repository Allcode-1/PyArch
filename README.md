# PyArch

PyArch is a small CLI tool for generating and extending FastAPI pet projects.
It is built with Typer and Jinja2 and currently focuses on a single opinionated
Layered Architecture.

The project started as a personal replacement for repeatedly creating the same
FastAPI structure by hand. It is primarily developed for my own workflow and is
not intended to be a universal production-ready scaffolding tool yet (probly never haha).

## Project Status

**MVP+ — early development**

The first working CLI flow is in place, but the project is still at the
beginning of development. Commands, generated code, templates, and the manifest
format may change.

Current limitations:

- only Layered Architecture is supported;
- generated applications use synchronous database access;
- only FastAPI projects are supported;
- integrations are planned, but their generators are not implemented yet;
- generated projects are starter scaffolds and still require manual
  configuration and application-specific code;
- the tool is currently tested mainly against my personal workflow and
  environment.

## What Works Now

- creating a new Layered FastAPI project;
- choosing PostgreSQL, SQLite, or MongoDB during initialization;
- installing the matching runtime and development dependencies with `uv`;
- generating the application layers, database configuration, test setup, and
  Alembic configuration for relational databases;
- generating a basic CRUD module and registering its model and router;
- keeping project state in `pyarch.toml`;
- displaying the current project configuration through the CLI.

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

For personal use outside the repository, install the current checkout as a
local tool:

```bash
uv tool install --editable .
```

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

The module generator reads `pyarch.toml`, adapts its templates to the selected
database, creates the Layered Architecture files, and registers the generated
model and router.

## Generated Structure

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

`pyarch.toml` records the selected architecture, database backend, generated
modules, enabled integrations, and generator version. This state will be used
to make later generation steps aware of the existing project.

## Roadmap

- implement integration generators;
- improve validation, error handling, and rollback behavior;
- make repeated generation safer and more predictable;
- add dry-run and generated-diff workflows;
- expand automated tests;
- consider additional architectures after the Layered flow becomes stable.

Supporting many architectures is not the immediate goal. The current priority
is to make one Layered FastAPI workflow reliable enough for regular personal
use.

## Disclaimer

PyArch is an experimental personal developer tool. Review generated code before
using it in a real project, and expect breaking changes while the CLI is in its
MVP+ stage.
