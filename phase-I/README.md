# Phase I: In-Memory Python Console Todo Application

A simple command-line todo management system with in-memory storage.

## Description

This is Phase I of the Hackathon II Todo Application project. It provides a console-based interface for managing todos with basic CRUD operations. All data is stored in memory and will be lost when the application exits.

## Features

- ✅ Create new todo items
- ✅ View all todos with their status
- ✅ Mark todos as complete
- ✅ Edit todo titles
- ✅ Delete todos
- ✅ Help system with command reference
- ✅ Input validation and error handling

## Requirements

- Python 3.8 or higher
- No external dependencies (uses standard library only)

## Installation

No installation required. Simply run the application with Python.

## How to Run

```bash
cd phase-I
python -m src.main
```

## Available Commands

| Command | Example | Description |
|---------|---------|-------------|
| `add <title>` | `add Buy groceries` | Create a new todo |
| `list` | `list` | Display all todos |
| `complete <id>` | `complete 1` | Mark todo as completed |
| `edit <id> <new_title>` | `edit 1 Buy milk instead` | Update todo title |
| `delete <id>` | `delete 1` | Remove a todo |
| `help` | `help` | Show available commands |
| `exit` or `quit` | `exit` | Exit the application |

## Usage Examples

### Creating Todos

```
> add Buy groceries
✓ Todo created with ID 1: "Buy groceries" (pending)

> add Call mom
✓ Todo created with ID 2: "Call mom" (pending)
```

### Listing Todos

```
> list

Your Todos:
  1. [ ] Buy groceries
  2. [ ] Call mom
```

### Completing Todos

```
> complete 1
✓ Todo 1 marked as completed

> list

Your Todos:
  1. [X] Buy groceries
  2. [ ] Call mom
```

### Editing Todos

```
> edit 2 Call mom at 3pm
✓ Todo 2 updated

> list

Your Todos:
  1. [X] Buy groceries
  2. [ ] Call mom at 3pm
```

### Deleting Todos

```
> delete 1
✓ Todo 1 deleted

> list

Your Todos:
  1. [ ] Call mom at 3pm
```

## Validation Rules

- **Title length**: Maximum 500 characters
- **Empty titles**: Not allowed (whitespace-only titles rejected)
- **Invalid IDs**: Negative numbers or out-of-range IDs rejected
- **Invalid commands**: Display error message with help suggestion

## Phase I Scope Notes

**Included**:
- Console-based interface only
- In-memory data storage (no persistence)
- Basic CRUD operations
- Input validation and error handling

**Not Included** (Future Phases):
- File or database persistence
- Web interface
- Multi-user support
- Authentication
- Categories, tags, or priorities
- Due dates or reminders
- Search or filter functionality

## Architecture

```
phase-I/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # Entry point and main loop
│   ├── cli.py            # Command parsing and display
│   ├── todo_manager.py   # Business logic (CRUD operations)
│   ├── models.py         # Todo data model and validation
│   ├── storage.py        # In-memory storage layer
│   └── constants.py      # Configuration constants
├── tests/                # Optional unit tests
└── README.md            # This file
```

## Project Information

- **Phase**: Phase I - In-Memory Python Console App
- **Technology Stack**: Python (standard library only)
- **Created**: 2025-12-31
- **Hackathon**: Hackathon II - Todo Application

## License

This is a hackathon project for educational purposes.
