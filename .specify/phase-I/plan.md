# Phase I Implementation Plan: In-Memory Python Console Todo Application

**Phase**: Phase I - In-Memory Python Console App
**Created**: 2025-12-31
**Status**: Active
**Specification**: `.specify/phase-I/specification.md`
**Output Directory**: `/phase-I/`

---

## Executive Summary

This plan outlines the implementation approach for Phase I of the Hackathon II Todo Application. Phase I focuses on building a console-based todo management system using Python with in-memory storage. The implementation strictly adheres to Phase I boundaries—no persistence, no web interfaces, no future-phase features.

**Core Deliverables**:
- Python console application with command-line interface
- In-memory CRUD operations for todos
- Input validation and error handling
- User-friendly console output

**Technology Stack**:
- Python 3.8+ (standard library only for core logic)
- Optional: minimal CLI helpers (e.g., for colored output)

---

## Constitution Check

Per `.specify/memory/constitution.md`:

✅ **Phase Discipline (§2)**: Implementation confined to Phase I scope only
✅ **Output Directory (§2.4)**: All code outputs to `/phase-I/` directory
✅ **Technology Stack (§2.2)**: Python only, no databases, no web interfaces
✅ **Phase Prohibitions (§2.2)**: NO persistence, NO GUI, NO web interfaces
✅ **SpecKitPlus Workflow (§3)**: Following Specification → Planning → Tasks → Implementation
✅ **Agent Behavior (§4)**: No assumptions, all requirements from specification
✅ **Code Quality (§5)**: Clean, readable Python following best practices
✅ **No Phase II+ Features (§2.1)**: Strictly in-memory, console-only

**Compliance Status**: ✅ PASS - All constitutional requirements met

---

## High-Level Architecture

### System Overview

```
┌─────────────────────────────────────────┐
│         Console Interface (CLI)          │
│  - Command parser                        │
│  - User input/output                     │
│  - Help & error messages                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│       Todo Manager (Business Logic)      │
│  - CRUD operations                       │
│  - Validation                            │
│  - Status management                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      In-Memory Storage (Data Layer)      │
│  - Todo list (list/dict)                 │
│  - ID generation                         │
│  - Data access                           │
└─────────────────────────────────────────┘
```

### Core Modules

| Module | Responsibility | Key Functions |
|--------|---------------|---------------|
| `main.py` | Application entry point, main loop | `main()`, `run_app()` |
| `cli.py` | Command parsing, user I/O | `parse_command()`, `display_*()`, `prompt_user()` |
| `todo_manager.py` | Business logic, CRUD operations | `add_todo()`, `list_todos()`, `complete_todo()`, `edit_todo()`, `delete_todo()` |
| `models.py` | Todo data model, validation | `class Todo`, `validate_title()` |
| `storage.py` | In-memory data storage | `class TodoStorage`, `get_next_id()` |
| `constants.py` | Configuration constants | `MAX_TITLE_LENGTH`, `STATUS_PENDING`, `STATUS_COMPLETED` |

---

## Module Breakdown & Task List

### Module 1: Project Setup & Structure

**Purpose**: Initialize project structure and configuration

**Tasks**:
1. Create `/phase-I/` directory structure
   ```
   phase-I/
   ├── src/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── cli.py
   │   ├── todo_manager.py
   │   ├── models.py
   │   ├── storage.py
   │   └── constants.py
   ├── tests/ (optional for Phase I)
   ├── README.md
   └── requirements.txt (optional, for CLI helpers)
   ```

2. Create `constants.py` with configuration
   - `MAX_TITLE_LENGTH = 500`
   - `STATUS_PENDING = "pending"`
   - `STATUS_COMPLETED = "completed"`
   - Command constants

3. Create `README.md` with:
   - Project description
   - How to run
   - Available commands
   - Phase I scope notes

**Dependencies**: None
**Deliverable**: Project structure ready for implementation

---

### Module 2: Data Model & Storage

**Purpose**: Define Todo entity and in-memory storage mechanism

**Tasks**:

1. **Implement `models.py`**:
   - `class Todo`:
     - Attributes: `id` (int), `title` (str), `status` (str), `created` (datetime, optional)
     - Method: `__init__(id, title, status, created)`
     - Method: `to_dict()` - for display formatting
     - Method: `__str__()` - string representation

   - `validate_title(title)`:
     - Check not empty/whitespace only
     - Check length ≤ 500 characters
     - Return (is_valid, error_message)

2. **Implement `storage.py`**:
   - `class TodoStorage`:
     - Attribute: `_todos` (dict: id → Todo)
     - Attribute: `_next_id` (int, starts at 1)
     - Method: `get_next_id()` - return and increment ID
     - Method: `add(todo)` - store todo
     - Method: `get(id)` - retrieve by ID
     - Method: `get_all()` - return all todos as list
     - Method: `delete(id)` - remove todo
     - Method: `exists(id)` - check if ID exists

**Dependencies**: `constants.py`
**Deliverable**: Data model and storage layer complete

**Acceptance Criteria**:
- Todo validation rejects empty titles
- Todo validation rejects titles > 500 characters
- TodoStorage correctly assigns sequential IDs
- TodoStorage maintains data consistency

---

### Module 3: Business Logic (Todo Manager)

**Purpose**: Implement CRUD operations and business rules

**Tasks**:

1. **Implement `todo_manager.py`**:
   - `class TodoManager`:
     - Attribute: `storage` (TodoStorage instance)
     - Method: `add_todo(title)` → (success, message, todo_id)
       - Validate title
       - Create Todo with pending status
       - Store and return result

     - Method: `list_todos()` → list of todos
       - Return all todos from storage
       - Preserve order (by ID or creation time)

     - Method: `complete_todo(id)` → (success, message)
       - Check todo exists
       - Update status to completed
       - Return result

     - Method: `edit_todo(id, new_title)` → (success, message)
       - Check todo exists
       - Validate new title
       - Update title
       - Return result

     - Method: `delete_todo(id)` → (success, message)
       - Check todo exists
       - Remove from storage
       - Return result

**Dependencies**: `models.py`, `storage.py`, `constants.py`
**Deliverable**: Complete business logic layer

**Acceptance Criteria**:
- All CRUD operations work correctly
- Invalid IDs return appropriate errors
- Validation rules enforced
- Status changes tracked correctly

---

### Module 4: Command-Line Interface (CLI)

**Purpose**: Handle user interaction and command parsing

**Tasks**:

1. **Implement `cli.py`**:
   - `parse_command(input_string)` → (command, args)
     - Parse user input into command + arguments
     - Handle: add, list, complete, edit, delete, help, exit/quit
     - Return structured command data

   - `display_welcome()`
     - Show welcome message
     - Show available commands

   - `display_help()`
     - List all commands with usage
     - Show examples from specification

   - `display_todos(todos)`
     - Format and display todo list
     - Show ID, title, status
     - Distinguish pending vs completed (visual indicator)
     - Handle empty list case

   - `display_success(message)`
     - Show success feedback

   - `display_error(message)`
     - Show error feedback
     - Include actionable guidance

   - `prompt_user()` → user input string
     - Display prompt (e.g., "> ")
     - Read and return user input

**Dependencies**: `constants.py`
**Deliverable**: Complete CLI interface

**Acceptance Criteria**:
- Commands parsed correctly
- Clear visual distinction between pending/completed
- Helpful error messages
- Clean, readable output

---

### Module 5: Main Application Loop

**Purpose**: Coordinate CLI and business logic, manage application lifecycle

**Tasks**:

1. **Implement `main.py`**:
   - `run_app()`:
     - Initialize TodoManager
     - Display welcome message
     - Enter main loop:
       - Prompt for command
       - Parse command
       - Execute corresponding operation
       - Display result
       - Handle errors gracefully
     - Exit on quit/exit command
     - Display goodbye message

   - `main()`:
     - Entry point
     - Call `run_app()`
     - Handle unexpected errors

   - Command handlers:
     - `handle_add(manager, args)`
     - `handle_list(manager, args)`
     - `handle_complete(manager, args)`
     - `handle_edit(manager, args)`
     - `handle_delete(manager, args)`
     - `handle_help()`

**Dependencies**: `cli.py`, `todo_manager.py`
**Deliverable**: Fully functional application

**Acceptance Criteria**:
- Application starts up < 2 seconds
- All commands work end-to-end
- Graceful error handling
- Clean exit on quit/exit

---

### Module 6: Edge Case Handling & Validation

**Purpose**: Ensure robust error handling per specification

**Tasks**:

1. **Implement edge case handlers**:
   - Empty list handling → informative message
   - Invalid ID (negative, out of range) → error with guidance
   - Empty/whitespace titles → validation error
   - Long titles (>500 chars) → validation error with limit
   - Invalid commands → help suggestion
   - Application startup → welcome + help
   - Application exit → goodbye message

2. **Input sanitization**:
   - Trim whitespace from titles
   - Validate ID is integer
   - Handle malformed input gracefully

3. **Error message templates**:
   - "Todo not found. Use 'list' to see valid IDs."
   - "Title cannot be empty. Please provide a description."
   - "Title too long (max 500 characters). Current: {length}"
   - "Invalid command '{cmd}'. Type 'help' for available commands."

**Dependencies**: All modules
**Deliverable**: Robust error handling throughout

**Acceptance Criteria**:
- All 7 edge cases from specification handled
- No crashes on invalid input (100% requirement)
- Error messages actionable and helpful

---

## Task Dependencies & Sequence

### Critical Path

```
Project Setup (Module 1)
    ↓
Data Model & Storage (Module 2)
    ↓
Business Logic (Module 3)
    ↓
CLI Interface (Module 4)
    ↓
Main Application (Module 5)
    ↓
Edge Case Handling (Module 6)
```

### Parallel Development Opportunities

After Module 1 completes:
- Module 2 (Data Model) can be developed independently
- Module 4 (CLI) can be developed in parallel with Module 2

After Module 2 and Module 4 complete:
- Module 3 (Business Logic) requires Module 2
- Module 5 (Main App) requires Modules 3 and 4

Module 6 (Edge Cases) can be implemented incrementally alongside other modules.

---

## Implementation Milestones

| Milestone | Description | Deliverables | Success Criteria |
|-----------|-------------|--------------|------------------|
| **M1: Foundation** | Project setup and data model | Modules 1, 2 complete | Todo model validated, storage functional |
| **M2: Core CRUD** | Business logic implemented | Module 3 complete | add, list, complete, delete work programmatically |
| **M3: User Interface** | CLI and main loop | Modules 4, 5 complete | Full end-to-end user interaction |
| **M4: Production Ready** | Edge cases and polish | Module 6 complete | All acceptance scenarios pass |

### Milestone Validation

**M1 Validation**:
- Can create Todo objects
- TodoStorage stores and retrieves todos
- Validation catches invalid titles

**M2 Validation**:
- TodoManager CRUD operations work
- IDs assigned correctly
- Status changes tracked

**M3 Validation**:
- User can add, list, complete, edit, delete via CLI
- Help and exit commands work
- Basic error handling present

**M4 Validation**:
- All user stories (P1-P4) testable via CLI
- All edge cases handled
- Performance criteria met (< 2s startup, < 1s operations)

---

## Testing Strategy

### Manual Testing Checklist

**User Story 1 (P1): Create and View Todos**
- [ ] Can add a todo and see confirmation
- [ ] Can list multiple todos with titles and status
- [ ] Empty list shows appropriate message

**User Story 2 (P2): Mark Complete**
- [ ] Can mark todo as complete
- [ ] Completed todos visually distinguished
- [ ] Invalid ID shows error

**User Story 3 (P3): Delete Todos**
- [ ] Can delete a todo
- [ ] Deleted todo no longer in list
- [ ] Invalid ID shows error

**User Story 4 (P4): Edit Titles**
- [ ] Can edit todo title
- [ ] Updated title displayed correctly
- [ ] Empty title rejected

**Edge Cases**
- [ ] Empty list handled
- [ ] Invalid ID (negative, out of range) rejected
- [ ] Empty/whitespace title rejected
- [ ] Long title (>500 chars) rejected
- [ ] Invalid command shows help
- [ ] Startup shows welcome
- [ ] Exit shows goodbye

### Automated Testing (Optional for Phase I)

If implementing tests (encouraged for code quality):

```
tests/
├── test_models.py        # Todo model validation
├── test_storage.py       # Storage operations
├── test_todo_manager.py  # Business logic
└── test_cli.py           # Command parsing
```

Use pytest framework with fixtures for TodoStorage/TodoManager.

---

## Technical Decisions

### Command Syntax Design

**Chosen Approach**: Space-separated arguments
```
add <title>
complete <id>
edit <id> <new_title>
delete <id>
list
help
exit / quit
```

**Rationale**:
- Simple to parse
- Intuitive for users
- Matches specification examples

**Alternative Considered**: Flag-based (e.g., `--add "title"`)
- More complex to implement
- Less intuitive for simple operations

### Data Structure for Storage

**Chosen Approach**: Dictionary (id → Todo)
```python
{
    1: Todo(id=1, title="Buy groceries", status="pending"),
    2: Todo(id=2, title="Call mom", status="completed")
}
```

**Rationale**:
- O(1) lookup by ID
- Easy to check existence
- Simple to implement

**Alternative Considered**: List of Todos
- O(n) lookup
- Would require linear search for operations

### ID Generation Strategy

**Chosen Approach**: Sequential integers starting at 1
```python
_next_id = 1
# Increment on each add
```

**Rationale**:
- Simple and predictable
- User-friendly (small numbers)
- Sufficient for in-memory Phase I scope

**Alternative Considered**: UUIDs
- Overly complex for Phase I
- Not user-friendly for manual ID input

### Status Representation

**Chosen Approach**: String constants ("pending", "completed")

**Rationale**:
- Simple and readable
- Easy to display to users
- Sufficient for two states

**Alternative Considered**: Boolean (is_completed)
- Less extensible
- Less descriptive in output

---

## Directory Structure (Final)

```
phase-I/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point, main loop
│   ├── cli.py               # Command parsing, display functions
│   ├── todo_manager.py      # Business logic, CRUD operations
│   ├── models.py            # Todo class, validation
│   ├── storage.py           # In-memory storage
│   └── constants.py         # Configuration constants
├── tests/ (optional)
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_todo_manager.py
│   └── test_cli.py
├── README.md                # Project documentation
└── requirements.txt         # Dependencies (if any)
```

---

## Notes for Developers and AI Agents

### Phase I Boundaries (CRITICAL)

**ALLOWED**:
- Python standard library
- In-memory data structures (lists, dicts)
- Console I/O (print, input)
- Optional: terminal color libraries (e.g., colorama)

**PROHIBITED**:
- ❌ File I/O for persistence (NO json, pickle, csv)
- ❌ Database connections (NO sqlite, postgres)
- ❌ Web frameworks (NO flask, fastapi)
- ❌ HTTP requests/APIs
- ❌ Any Phase II+ technologies

### Code Quality Guidelines

**Simplicity First**:
- Avoid over-engineering
- No complex design patterns unless justified
- Clear, readable code over clever code

**Testability**:
- Separate business logic from I/O
- Pure functions where possible
- Dependency injection for TodoManager/Storage

**Error Handling**:
- Never crash on invalid input
- Always provide actionable error messages
- Handle edge cases explicitly

**Documentation**:
- Docstrings for classes and non-obvious functions
- Inline comments for complex logic only
- README explains how to run and use

### Development Best Practices

1. **Start with Module 1 & 2**: Get data model solid first
2. **Test as you go**: Manually test each module as completed
3. **Keep commands simple**: Match specification examples
4. **User feedback**: Every operation gives clear confirmation or error
5. **Performance**: Measure startup time, should be < 2 seconds
6. **Character limit**: Enforce 500-character validation strictly

### Common Pitfalls to Avoid

❌ **Don't add persistence**: It's tempting, but violates Phase I scope
❌ **Don't over-validate**: Keep validation to spec requirements
❌ **Don't add extra features**: Categories, priorities, due dates are out of scope
❌ **Don't use complex parsing**: Simple string split is sufficient
❌ **Don't skip error messages**: Users need helpful feedback

### Integration with Future Phases

**Design considerations for Phase II migration**:
- TodoManager interface should be clean (easy to swap storage layer)
- Business logic separate from I/O (can reuse in API)
- Validation functions reusable

**But don't over-engineer for future**:
- No database abstraction layer
- No API-style request/response objects
- No persistence hooks

---

## Success Criteria (from Specification)

- **SC-001**: Users can create, view, mark complete, delete, and edit todos ✅
- **SC-002**: Full workflow completes in < 30 seconds ✅
- **SC-003**: Operations provide feedback < 1 second ✅
- **SC-004**: 100% invalid inputs handled with clear errors ✅
- **SC-005**: Visual distinction between pending/completed ✅
- **SC-006**: Startup in < 2 seconds ✅
- **SC-007**: Data consistency maintained throughout session ✅

---

## Next Steps

After this planning document:

1. **Review & Approve**: Stakeholder/developer review of plan
2. **Generate Tasks**: Run `/sp.tasks` to create detailed task list
3. **Implementation**: Follow task list to build Phase I
4. **Testing**: Validate against acceptance criteria
5. **Documentation**: Update README with usage instructions

**Proceed to**: `/sp.tasks` when ready to begin implementation

---

**Phase I Plan Status**: ✅ Complete and ready for task generation
**Constitutional Compliance**: ✅ Verified
**Technical Feasibility**: ✅ Confirmed
