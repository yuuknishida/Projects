
# TicTacToeAI (Python)

## Overview
Implementation of a Tic-Tac-Toe game with an AI opponent using the Minimax algorithm. The AI evaluates possible move trees to select optimal plays, ensuring an unbeatable strategy under normal rules.

## Features
- Human vs AI gameplay.
- Board state management and win/draw detection.
- Minimax recursive search (optional depth pruning if added).
- Simple CLI interaction (in `game.py`).

## File
- `game.py` – Core game loop, board representation, Minimax logic.

## Run
Activate any virtual environment if required, then:
```powershell
python game.py
```
Follow on-screen prompts to enter moves (row/column or numeric cell IDs).

## Minimax Summary
For each available move, the algorithm simulates subsequent opponent responses, scoring terminal outcomes (+1 win, 0 draw, -1 loss, commonly). It chooses the move yielding the highest guaranteed outcome assuming optimal opponent play.

## Possible Enhancements
- Alpha-beta pruning for search efficiency.
- GUI (PyQt5 or Tkinter) board.
- Move history and replay functionality.
- Adjustable AI difficulty (random mistakes, reduced depth).

## Learning Focus
Demonstrates classic deterministic game search, evaluation heuristics, and clean separation of game mechanics from AI logic.
