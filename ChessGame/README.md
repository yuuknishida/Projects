
# ChessGame (Python + Stockfish)

## Overview
This project combines custom Python chess logic with the Stockfish engine. It manages board state, move validation, and optionally integrates an AI engine for analysis or automated play. A PyQt5-based interface can be used for a graphical board (libraries are present in the environment).

## Features
- Board representation and move handling.
- Integration with Stockfish for best-move suggestions and evaluation.
- Potential GUI via PyQt5 (see installed packages and `window.py`).
- Modular source layout under `src/`.
- Logging of errors/events (`ErrorLog.py`).

## Directory Layout
- `src/App.py` – Possible entry script for launching the application.
- `src/chessBoardManager.py` – Board state and move coordination.
- `src/chessEngine.py` – Interface layer to Stockfish engine.
- `src/window.py` – GUI constructs (PyQt5 windows/widgets).
- `stockfish/` – Engine source and documentation.
- `resources/` – Cursor assets and other UI resources.

## Environment
The folder contains a Python virtual environment (`pyvenv.cfg`, `Scripts/`, `Lib/`). Activate it before running.

### Activate (Windows PowerShell)
```powershell
cd ChessGame
Scripts\activate
```
### Activate (Unix/macOS)
```bash
cd ChessGame
source bin/activate
```

## Run
If `App.py` is the main entry:
```powershell
python src/App.py
```
Or run individual modules for testing:
```powershell
python src/chessEngine.py
```

## Stockfish Integration
`chessEngine.py` likely spawns a Stockfish process, passes FEN positions or move sequences, and parses returned evaluations (score, best move). Adjust path to the Stockfish binary if needed.

## Possible Enhancements
- Time controls and move clocks.
- PGN import/export.
- Opening book integration.
- Multi-variant support (Chess960, etc.).

## Learning Focus
Illustrates engine integration, event-driven GUI design, and separation of board logic from UI concerns.

