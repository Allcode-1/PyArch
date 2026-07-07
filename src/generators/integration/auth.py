from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src.config.models import DatabaseEngine
from src.generators.common.commands import run_command
from src.generators.common.filesystem import (
    append_text_once,
    create_empty_dir,
    create_module_path,
    insert_line_before_marker,
)
from src.generators.common.gitignore import (
    AUTH_GITIGNORE_ENTRIES,
    ensure_gitignore_entries,
)
from src.generators.common.renderer import create_file_from_template
from src.generators.module.layered import ensure_layered_project, register_model


AUTH_INTEGRATION_NAME = "auth"
AUTH_ENV_MARKER = "# PyArch auth integration"
AUTH_ENV_BLOCK = f"""
{AUTH_ENV_MARKER}
AUTH_JWT__ALGORITHM=RS256
AUTH_JWT__ACCESS_TOKEN_EXPIRE_MINUTES=15
AUTH_JWT__REFRESH_TOKEN_EXPIRE_DAYS=30
# AUTH_JWT__PUBLIC_KEY_PATH=certs/public.pem
# AUTH_JWT__PRIVATE_KEY_PATH=certs/private.pem
"""
AUTH_RUNTIME_DEPENDENCIES = (
    "pyjwt",
    "bcrypt",
    "pydantic[email]",
    "python-multipart",
    "cryptography",
)


def create_auth_integration(
    project_dir: Path,
    database: DatabaseEngine | str,
) -> tuple[Path, ...]:
    database = DatabaseEngine(database)
    if database is DatabaseEngine.MONGODB:
        raise ValueError("Auth integration is not supported for MongoDB projects yet")

    app_path = project_dir / "app"
    auth_path = app_path / "auth"
    models_init = app_path / "models" / "__init__.py"
    main_router = app_path / "api" / "v1" / "router.py"

    ensure_layered_project(models_init, main_router)

    auth_targets = (
        ("layered/auth/dependencies.py.j2", auth_path / "dependencies.py"),
        ("layered/auth/routes.py.j2", auth_path / "routes.py"),
        ("layered/auth/schemas.py.j2", auth_path / "schemas.py"),
        ("layered/auth/service.py.j2", auth_path / "service.py"),
        ("layered/auth/tokens.py.j2", auth_path / "tokens.py"),
        ("layered/auth/utils.py.j2", auth_path / "utils.py"),
        ("layered/auth/user_model.py.j2", app_path / "models" / "user.py"),
        (
            "layered/auth/refresh_session_model.py.j2",
            app_path / "models" / "refresh_session.py",
        ),
    )
    generated_targets = [path for _, path in auth_targets]
    generated_targets.extend(
        (
            project_dir / "certs" / "private.pem",
            project_dir / "certs" / "public.pem",
        )
    )

    existing_targets = [path for path in generated_targets if path.exists()]
    if existing_targets:
        existing = ", ".join(str(path) for path in existing_targets)
        raise FileExistsError(f"Auth integration files already exist: {existing}")

    install_auth_dependencies(project_dir)

    created_files: list[Path] = []
    create_module_path(auth_path)
    created_files.append(auth_path / "__init__.py")

    created_files.extend(
        create_file_from_template(template_name, output_path)
        for template_name, output_path in auth_targets
    )
    created_files.append(
        create_file_from_template(
            template_name="layered/auth/config.py.j2",
            output_path=app_path / "core" / "config.py",
        )
    )
    created_files.extend(create_auth_key_pair(project_dir / "certs"))

    register_model(models_init, "user", "User")
    register_model(models_init, "refresh_session", "RefreshSession")
    register_auth_router(main_router)
    created_files.append(append_auth_env_example(project_dir / ".env.example"))
    created_files.append(
        ensure_gitignore_entries(project_dir, "auth", AUTH_GITIGNORE_ENTRIES)
    )

    return tuple(created_files)


def install_auth_dependencies(project_dir: Path) -> None:
    run_command("uv", "add", *AUTH_RUNTIME_DEPENDENCIES, cwd=project_dir)


def create_auth_key_pair(certs_dir: Path) -> tuple[Path, Path]:
    create_empty_dir(certs_dir)
    private_path = certs_dir / "private.pem"
    public_path = certs_dir / "public.pem"

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    public_path.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

    return private_path, public_path


def register_auth_router(main_router: Path) -> None:
    insert_line_before_marker(
        main_router,
        "# pyarch:router-imports",
        "from app.auth.routes import router as auth_router",
    )
    insert_line_before_marker(
        main_router,
        "# pyarch:router-includes",
        "v1_router.include_router(auth_router)",
    )


def append_auth_env_example(env_example: Path) -> Path:
    append_text_once(env_example, AUTH_ENV_MARKER, AUTH_ENV_BLOCK)
    return env_example
