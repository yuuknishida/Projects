
# Task Manager (Python)

## Overview
Python application providing task CRUD (Create, Read, Update, Delete) functionality. The structure suggests a Flask-based backend (presence of `templates/`) possibly combined with a PyQt5 or web interface for interaction. It demonstrates routing, form/template rendering, and state management for task objects.

## Features
- Add, list, update, and remove tasks.
- HTML templates for rendering task lists and forms (`templates/`).
- Config abstraction via `config.py`.
- Modular entry point (`app.py`).

## Project Structure
- `task-manager/app.py` – Main application factory or route definitions.
- `task-manager/config.py` – Configuration (environment variables, settings).
- `templates/` – Jinja2 HTML templates (`home.html`, `add_task.html`, `base.html`).
- `pyvenv.cfg`, `Scripts/`, `Lib/` – Virtual environment assets.

## Environment Setup
Activate the virtual environment before running (if populated):
```powershell
cd task-manager
Scripts\activate
```
If dependencies are not yet installed (no explicit requirements file provided), install any needed packages manually, e.g.:
```powershell
pip install flask pyqt5
```

## Run
From inside the environment:
```powershell
python task-manager\app.py
```
Then open the local server URL printed (commonly `http://127.0.0.1:5000/`).

## Possible Enhancements
- Persistent storage (SQLite or PostgreSQL) vs in-memory/dictionary.
- User authentication and session management.
- Task tagging, prioritization, and filtering.
- REST API endpoints for integration.

## Learning Focus
Demonstrates Python web app structure, template rendering, and simple state management patterns.

