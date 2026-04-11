# Script for creating fastapi pet-project skeleton

Just run the script and start your project. You will need uv to use this. Read "README.md" file for detail instructions

## Project Status

- Current level: **MVP**

What this means:
- Script can only generate fastapi petproject sceleton.
- It is sync fastapi petproject base.
- No other stack petprojects included.
- Script does not have a exception handlers.

## Features

- Creating a new dir (you set the name)
- Installing all basic libs, packages and frameworks for fastapi petproject.
- Creating a .env file with db and jwt settings.
- Creating clean-architecture folders system.
- Creating a MVP main.py code for fastapi.
- Creating DB connection - app/db/session.py (write down your settings in .env to make it clear).
- Does correct alembic settings for you.

## Security and Integrity Improvements

- Not included.

## Tech Stack

- Python 3.xx

## Quick Start (Local)

1. Run the script
```bash
    uv run main.py
```

2. Write down the dir for project
```bash
    # Where create project? Leave empty for current folder:
    C:/your_path
```

3. Write down the name of project
```bash
    # Name your project: 
    your_project_name
```

4. Open the "README.md" for details

## Created PetProject Structure

```text
app/
  api/          # HTTP layer (routers + deps)
  core/         # settings and security
  db/           # session/base
  models/       # SQLAlchemy models
  repositories/ # data access layer
  schemas/      # API DTOs (request/response)
  services/     # business logic
tests/
alembic/        # migrations settings (pre-ready)
```

## Notes

- This script was made personally for me, it may not work on your devices.
- The goal is to create nice skeleton for my fastapi prtprojects using script.
