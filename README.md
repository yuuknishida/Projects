# Projects Portfolio

This repository aggregates several software and embedded systems projects implemented in C, C++, and Python. Each subfolder contains its own focused application demonstrating specific concepts: data structures, algorithms, UI design, microcontroller peripheral control, and game AI.

## Project Index

| Folder | Description | Primary Tech |
|--------|-------------|--------------|
| `Banking Management System based on Text` | Text-based banking/account management CLI using file persistence plus data structures (queues, BST). | C++ |
| `ChessGame` | Python chess logic integrated with the Stockfish engine and a GUI layer (PyQt5). | Python, Stockfish |
| `LightCntrPrj` | TM4C123 microcontroller firmware: ADC sampling, PWM output, timers, UART comms, moving average filtering, temperature sensor (TMP102). | Embedded C |
| `task-manager` | Task management application (Flask backend + PyQt5 / HTML templates) with CRUD operations for tasks. | Python (Flask, PyQt5) |
| `TicTacToeAI` | Tic-Tac-Toe game with an AI opponent implemented via Minimax search. | Python |

## Quick Start

Clone the repository and navigate into a project folder of interest:

```powershell
git clone https://github.com/yuuknishida/Projects.git
cd Projects/ChessGame
```

See each project's `README.md` for build/run instructions.

## Technology Highlights

- Data structures (queues, binary search trees) for transaction handling.
- Game AI integration and search (Stockfish; Minimax for Tic-Tac-Toe).
- Peripheral programming on TM4C (ADC, PWM, timers, UART, I2C sensor).
- Python desktop/web UI patterns (Flask routes, templates, PyQt5 widgets).
- Code organization into modular components (e.g., separate drivers and managers).

## Folder Overview

- `Banking Management System based on Text/` – Standalone C++ source file implementing menu-driven banking operations.
- `ChessGame/src/` – Core chess logic, board management, engine interaction.
- `LightCntrPrj/` – Firmware modules per peripheral (e.g., `ADC0.c`, `PWM.c`).
- `task-manager/task-manager/` – Application entry (`app.py`), configuration, and templates.
- `TicTacToeAI/` – `game.py` encapsulating board state and AI moves.

## License / Usage

Unless otherwise stated in subfolders, these projects are provided for personal learning and demonstration. Feel free to explore and adapt ideas.

---
For deeper details, open the specific project README files.

