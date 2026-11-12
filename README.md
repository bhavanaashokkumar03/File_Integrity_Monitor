# File Integrity Monitoring System (FIM)

## Project Overview
A Python-based File Integrity Monitoring System that monitors files and detects unauthorized changes by comparing current file states with a previously created baseline.

## Features
- Create file integrity baselines.
- Detect modified files.
- Detect newly created files.
- Detect deleted files.
- Record detected events in log files.

## Technologies Used
- Python
- JSON
- SHA-256 Hashing
- VS Code

## Project Structure

```text
FILE_INTEGRITY_MONITOR/
│
├── monitored_files/
│   └── test.txt
│
├── baseline.json
├── integrity.py
├── logs.txt
├── main.py
└── README.md
```

## How to Run

1. Install Python.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run:

```bash
py main.py
```

5. Select option 1 to create a baseline.
6. Select option 2 to scan and detect changes.

## Testing
The following tests were performed:

- File modification detection
- New file detection
- File deletion detection
- Event logging

## Project Objective
To understand file integrity, cryptographic hashing, baseline comparison, and basic security monitoring using Python.

## Disclaimer
This is an educational cybersecurity project developed for learning purposes.