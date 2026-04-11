from pathlib import Path
import subprocess
import shutil


# creating a pf
print("Name your project: ")
project_name = input()
base = Path('C:\olzhas\python')
project_dir = base / project_name
subprocess.run(["uv", "init", project_name], cwd=base, check=True)
subprocess.run(["uv", "add", "fastapi", "uvicorn", "sqlalchemy", "psycopg[binary]", "alembic", "pytest", "ruff", "mypy"], cwd=project_dir, check=True)
subprocess.run(["uv", "run", "alembic", "init", "alembic"], cwd=project_dir, check=True)

# creating files structure
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
    "from fastapi import FastAPI"
)










