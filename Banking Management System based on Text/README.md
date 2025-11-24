
# Banking Management System (Text-Based, C++)

## Overview
A console application implementing a simple banking/account management workflow. It uses fundamental data structures (queues for pending transactions, a binary search tree for account lookup) and text file persistence to store account records.

## Features
- Create, view, update, and delete accounts.
- Deposit and withdraw operations.
- Queue-based transaction staging (if implemented in code).
- Binary Search Tree for fast account search by key (e.g., account number).
- Plain text file storage (portable, human-readable).

## Project Structure
- `main (2).cpp` – Entry point and core logic (menus, data handling).
- (Additional helper structures may be embedded directly inside the main file.)

## Build & Run
Using g++ (MinGW or similar) on Windows PowerShell:
```powershell
g++ "main (2).cpp" -std=c++17 -O2 -o banking
./banking.exe
```
On Linux/macOS:
```bash
g++ "main (2).cpp" -std=c++17 -O2 -o banking
./banking
```

## Data Handling
Accounts and transactions are stored in plain text files (filenames defined in the source). BST nodes represent accounts, enabling efficient searches and updates. Queues manage ordering of pending or recent transactions.

## Possible Extensions
- Switch to binary or SQLite storage for scalability.
- Add authentication and basic encryption of sensitive fields.
- Implement reporting (daily summaries, top accounts by balance).

## Learning Focus
Demonstrates C++ file I/O, custom data structures, and a menu-driven CLI application pattern.

