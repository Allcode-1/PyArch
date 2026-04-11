from pathlib import Path
import subprocess
import shutil
from textwrap import dedent

# base dir
base_path = input("Where create project? Leave empty for current folder: ").strip()
base = Path(base_path).expanduser().resolve() if base_path else Path.cwd()
if not base.exists():
    raise FileNotFoundError(f"Base path does not exist: {base}")

# creating a pf
print("Name your project: ")
project_name = input()
project_dir = base / project_name
subprocess.run(["uv", "init", project_name], cwd=base, check=True)
subprocess.run(["uv", "add", "fastapi", "uvicorn", "sqlalchemy", "psycopg[binary]", "alembic", "dotenv"], cwd=project_dir, check=True)
subprocess.run(["uv", "add", "--dev", "pytest", "mypy", "ruff"], cwd=project_dir, check=True)
subprocess.run(["uv", "run", "alembic", "init", "alembic"], cwd=project_dir, check=True)

# creating a .env file
env = project_dir / ".env"
env.touch(exist_ok=True)
env.write_text(dedent("""
    # db and test db
    DATABASE_URL=postgresql+psycopg://yourname:password@localhost:5432/db-name
    TEST_DATABASE_URL=postgresql+psycopg://yourname:password@localhost:5432/test-db-name


    # jwt things
    SECRET_KEY=your_secret_key
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    """).strip() + "\n",
    encoding="utf-8",
)

gitignore = project_dir / ".gitignore"
gitignore.write_text(dedent("""
    # Python-generated files
    __pycache__/
    *.py[oc]
    build/
    dist/
    wheels/
    *.egg-info

    # Virtual environments
    .venv
    .env
    """).strip() + "\n",
    encoding="utf-8",
)

# creating files structure (clean architecture)
app_dir = project_dir / "app"
app_dir.mkdir(exist_ok=True)

files = ["core", "db", "schemas", "models", "api", "services", "repositories"]
for i in files:
    file = app_dir / i
    file.mkdir(exist_ok=True)

tests_dir = project_dir / "tests"
tests_dir.mkdir(exist_ok=True)

# move main.py to app
src = project_dir / "main.py"
target_dir = app_dir

new_path = Path(shutil.move(str(src), str(target_dir / src.name)))
print(f"file main.py is redirected correctly, {new_path}")

# rewrite main.py
main_py = app_dir / "main.py"
main_py.write_text(
    dedent("""
        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/health")
        def healthcheck():
            return {"status": "ok"}
        """).strip() + "\n", 
    encoding="utf-8",
)

# creating session.py for db connection (postgresql)
session = app_dir / "db" / "session.py"
session.touch(exist_ok=True)
session.write_text(dedent("""
    import os

    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.orm import DeclarativeBase, sessionmaker

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

    class Base(DeclarativeBase):
        pass

    engine = create_engine(
        DATABASE_URL,
        echo=True
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    """).strip() + "\n",
    encoding="utf-8",
)

# creating a __ for tests db
tests_init = tests_dir / "__init__.py"
tests_init.touch(exist_ok=True)
tests_db = tests_dir / "conftest.py"
tests_db.touch(exist_ok=True)
tests_db.write_text(dedent("""
    import os

    import pytest
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.engine import make_url
    from sqlalchemy.orm import Session

    from app.db.session import Base, get_db
    from app.main import app as fastapi_app
    import app.models #noqa: F401


    DATABASE_URL = os.getenv("DATABASE_URL")
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
    if not TEST_DATABASE_URL:
        raise ValueError("TEST_DATABASE_URL is not set")


    def validate_test_database_url() -> None:
        test_url = make_url(TEST_DATABASE_URL)

        if DATABASE_URL:
            main_url = make_url(DATABASE_URL)
            if (
                test_url.drivername == main_url.drivername
                and test_url.username == main_url.username
                and test_url.host == main_url.host
                and test_url.port == main_url.port
                and test_url.database == main_url.database
            ):
                raise RuntimeError(
                    "TEST_DATABASE_URL points to the main database. "
                    "Refusing to run destructive test setup."
                )

        if not test_url.database or "test" not in test_url.database.lower():
            raise RuntimeError(
                "TEST_DATABASE_URL must point to a dedicated test database "
                "(database name should contain 'test')."
            )


    validate_test_database_url()


    engine = create_engine(TEST_DATABASE_URL, echo=False)


    @pytest.fixture(scope="session")
    def test_engine():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield engine
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


    @pytest.fixture(scope="function")
    def db_session(test_engine):
        connection = test_engine.connect()
        transaction = connection.begin()

        session = Session(
            bind=connection,
            autoflush=False,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        yield session

        session.close()
        transaction.rollback()
        connection.close()


    @pytest.fixture(scope="function")
    def client(db_session: Session):
        def override_get_db():
            yield db_session

        fastapi_app.dependency_overrides[get_db] = override_get_db

        with TestClient(fastapi_app) as test_client:
            yield test_client
        
        fastapi_app.dependency_overrides.clear()

    """).strip() + "\n",
    encoding="utf-8",
)

#creating __init__ for models to make alembic models import easy
models_init = app_dir / "models" / "__init__.py"
models_init.touch(exist_ok=True)
models_init.write_text(dedent("""
    # from app.models.yourmodel import modelClass
    # from app.models.yourmodel2 import modelClass2
    # from app.models.yourmodel3 import modelClass3

    # __all__ = ("modelClass", "modelClass2", ...)
    """).strip() + "\n",
    encoding="utf-8",
)

# rewriting alembic env.py file (db connection, models import, smmall settings)
alembic_env = project_dir / "alembic" / "env.py"
alembic_env.write_text(dedent("""
    from logging.config import fileConfig
    import os
    from dotenv import load_dotenv

    from sqlalchemy import engine_from_config
    from sqlalchemy import pool

    from alembic import context

    from app.db.session import Base
    import app.models #noqa: F401

    load_dotenv()

    config = context.config

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("database_url is not set")

    config.set_main_option("sqlalchemy.url", database_url)

    target_metadata = Base.metadata

    def run_migrations_offline() -> None:
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


    def run_migrations_online() -> None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata, compare_type=True
            )

            with context.begin_transaction():
                context.run_migrations()


    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
    """).strip() + "\n",
    encoding="utf-8",
)

readme = project_dir / "README.md"
readme.write_text(dedent("""
    ## After Running the Script

    If you opened this file, you probably already ran the script. Follow these steps to make your project skeleton work.

    ### 1. Configure your database settings in `.env`

    - Create a database in PGAdmin.
    - Put your username, password, and database name into `DATABASE_URL`.
    - Do the same for `TEST_DATABASE_URL` if you want to run tests.
    - You can skip the JWT settings for now. They are only needed for JWT-based auth.


    ### 2. Create and apply your first Alembic migration
    AFTER creating your SQLAlchemy models in app/models, run:

    ```bash
    uv run alembic revision --autogenerate -m "your message"
    uv run alembic upgrade head
    ```
    
    These commands will push your models into the database.

    Done
    Now your pet project is ready to go.

    Write anything you want there, even ToDo lists.
    """).strip() + "\n",
    encoding="utf-8",
)















