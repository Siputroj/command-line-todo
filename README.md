# Command-line ToDo (TUI)

Interactive command-line todo lists using `prompt_toolkit`, `SQLAlchemy`, and SQLite. You can create lists, add tasks inside a selected list, and toggle completion via a simple full-screen terminal UI.

## Requirements
- Python 3.10+
- Dependencies: `prompt_toolkit`, `SQLAlchemy`

## Setup
1) (Recommended) create and activate a virtual environment:
   - macOS/Linux: `python -m venv venv && source venv/bin/activate`
   - Windows (PowerShell): `python -m venv venv; .\\venv\\Scripts\\Activate.ps1`
2) Install dependencies: `pip install prompt_toolkit SQLAlchemy`

## Run
From the repo root:
```
python command-line-todo/main.py
```
The SQLite database is stored at `mydb.db` in the project root and is created automatically on first run.

## Keyboard shortcuts
- `Ctrl+C` or `Ctrl+Q`: exit the app

## Project layout
- `command-line-todo/main.py`: application entrypoint
- `command-line-todo/app.py`: list and task operations backed by SQLAlchemy models
- `command-line-todo/database.py`: SQLite models/session setup
- `command-line-todo/key_bindings.py`: global key bindings
- `command-line-todo/layout/`: prompt_toolkit UI layout components
- `mydb.db`: SQLite database (created at runtime)
