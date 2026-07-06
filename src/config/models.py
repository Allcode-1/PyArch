from dataclasses import dataclass, field
from enum import StrEnum


class Architecture(StrEnum):
    LAYERED = "layered"


class DatabaseEngine(StrEnum):
    POSTGRES = "postgres"
    SQLITE = "sqlite"
    MONGODB = "mongodb"


class DatabaseAccess(StrEnum):
    SYNC = "sync"


@dataclass(frozen=True, slots=True)
class ProjectSettings:
    name: str
    architecture: Architecture = Architecture.LAYERED


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    engine: DatabaseEngine
    access: DatabaseAccess = DatabaseAccess.SYNC


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    application: str = "app"
    tests: str = "tests"
    migrations: str | None = "alembic"


@dataclass(slots=True)
class ProjectState:
    modules: list[str] = field(default_factory=list)
    integrations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ProjectManifest:
    schema_version: int
    pyarch_version: str
    project: ProjectSettings
    database: DatabaseSettings
    paths: ProjectPaths = field(default_factory=ProjectPaths)
    state: ProjectState = field(default_factory=ProjectState)
