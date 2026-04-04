# Chronicle
[![version][version-badge]][CHANGELOG]

## Introduction

Chronicle is a simple locally hosted web application + CLI tool which can be used to keep track of your daily accomplishments by adding one-liner log messages.
The thought behind creating this project is to not try to remember everything that we do but have the software remember it for us.

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- HTML
- Tailwind CSS
- HTMX
- Typer
- uv (project dependency manager)

## Getting started

Follow these steps to get Chronicle up and running in your local system:-

1. Clone the repository (HTTPS or SSH): `git clone https://github.com/Rishil96/chronicle.git` or `git clone git@github.com:Rishil96/chronicle.git`
2. Install uv package manager via any one of the methods shown on their official site:- https://docs.astral.sh/uv/getting-started/installation/#installation-methods
3. Run `uv sync` to create the virtual environment and install all project dependencies in one go.
4. Create a `.env` file and add all the required variables as shown in the `.env.example` file (can be found at project root directory).
5. Configure `CHRONICLE_CONFIG = 'your-env-file-absolute-path-created-in-step-4'` into your user/system environment variables for the project code to load these variables via the .env path.
6. To run the web application locally, use `uv run fastapi dev app.py`.
7. To configure CLI tool, simply run `uv tool install .` from the project root directory, this will install chronicle as a CLI tool.
8. Run `uv tool update-shell` to make chronicle globally available on Windows.
9. To check if Chronicle CLI tool was installed successfully, run `chronicle --help`.
10. To enhance your logs via LLM processing, set `USE_LLM=True` and add all required LLM details including the API KEY in the .env file and if not simply set `USE_LLM=False` which will not require any of the other LLM related environment variables for the app to run.

[CHANGELOG]: ./CHANGELOG.md
[version-badge]: https://img.shields.io/badge/version-1.0.0-green.svg