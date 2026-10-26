# Chronicle
[![version][version-badge]][CHANGELOG]

## Introduction

Chronicle is a web application for teams to share their daily work updates in one place. Team members log what they worked on under a topic, and everyone can browse and filter the updates of the whole team.

The idea behind it is simple: don't rely on memory or scattered emails to keep track of work, let the software keep the record.

## Features

- Login for team members (accounts are created by an administrator, there is no public sign-up)
- Add work updates under a topic, with markdown support in the description
- Add new topics, each with a short description that appears as a hint on the update form
- Home page showing your own recent updates
- Team feed of all updates, grouped by date with the newest first
- Filter updates by user, topic, a single date or a date range
- Change password
- Updates cannot be edited or deleted after submission, so the record stays trustworthy

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy and Alembic (database operations & migrations)
- PostgreSQL
- Jinja2 templates
- HTMX
- Tailwind CSS
- uv (project dependency manager)

## Getting started

Follow these steps to run Chronicle locally.

1. Clone the repository (HTTPS or SSH): 
    ```
    git clone https://github.com/Rishil96/chronicle.git     # HTTPS
    git clone git@github.com:Rishil96/chronicle.git         # SSH
    ``` 
2. Install the uv package manager using one of the methods on the official site: [uv Installation Methods](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
3. Run `uv sync` to create a virtual environment and install all dependencies.
4. Configure a PostgreSQL database. For local development, a Docker container works well (use your own password):
   ```
   docker run --name chronicle-pg -e POSTGRES_USER=<username> -e POSTGRES_PASSWORD=<your-password> -e POSTGRES_DB=<database-name> -p 5432:5432 -v chronicle_pgdata:/var/lib/postgresql/data -d postgres:16
   ```
      Pin a major version of Postgres and avoid the `latest` tag. A data volume only works with the major version that created it.

5. Create a `.env` file in the project root, using `.env.example` as the template. The database variables must match what you used in step 4.

6. Create all database tables by running migrations:
   ```
   uv run alembic upgrade head
   ```

7. Create a user account for each team member:
   ```
   uv run scripts\create_user.py
   ```
   The script asks for the first name, last name, email and password.
8. Start the application:
   ```
   uv run fastapi dev app.py
   ```

9. Open the address shown in the terminal and log in.

## Database Migrations

Schema changes are managed with Alembic. After changing a model in `src/db/models.py`:

1. Generate a migration: `uv run alembic revision --autogenerate -m "short description"`
2. Read the generated file in `alembic/versions/` and check that it contains only your change.
3. Apply it: `uv run alembic upgrade head`

To roll back one step during development, use `uv run alembic downgrade -1`. Never edit a migration that has already been applied. Add a new one instead.


[CHANGELOG]: ./CHANGELOG.md
[version-badge]: https://img.shields.io/badge/version-2.0.0-green.svg