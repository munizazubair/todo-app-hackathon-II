---
description: "Phase I Implementation Tasks - In-Memory Python Console Todo App"
created: 2025-12-31
feature: "Phase I - Console Todo App"
---

# Tasks: Phase I - In-Memory Python Console Todo Application

**Input**: Design documents from `.specify/phase-I/` and `specs/001-phase-i-console-app/`
**Prerequisites**: plan.md (complete), specification.md (complete), spec.md (complete)

**Tests**: Tests are OPTIONAL for Phase I. Manual testing checklist provided in plan.md. Tasks below focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **Checkbox**: All tasks start with `- [ ]` for tracking
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Phase I uses single project structure:
- **Source code**: `phase-I/src/`
- **Optional tests**: `phase-I/tests/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project structure and configuration per plan.md

- [X] T001 Create phase-I directory structure (phase-I/src/, phase-I/tests/)
- [X] T002 Create empty Python module files in phase-I/src/__init__.py
- [X] T003 [P] Create constants.py with MAX_TITLE_LENGTH=500, STATUS_PENDING, STATUS_COMPLETED in phase-I/src/constants.py
- [X] T004 [P] Create README.md with project description, run instructions, available commands in phase-I/README.md
- [X] T005 [P] Create requirements.txt (empty or minimal CLI helpers) in phase-I/requirements.txt

**Checkpoint**: ✅ Project structure ready for implementation

---

## Phase 2: Foundational (Data Model & Storage Layer)

**Purpose**: Core data structures that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Implement Todo class with attributes (id, title, status, created) in phase-I/src/models.py
- [X] T007 [P] Implement validate_title() function (empty check, whitespace check, 500-char limit) in phase-I/src/models.py
- [X] T008 [P] Add Todo.__str__() and to_dict() methods for display formatting in phase-I/src/models.py
- [X] T009 [P] Implement TodoStorage class with _todos dict and _next_id counter in phase-I/src/storage.py
- [X] T010 [P] Implement TodoStorage.get_next_id() method in phase-I/src/storage.py
- [X] T011 [P] Implement TodoStorage.add(todo) method in phase-I/src/storage.py
- [X] T012 [P] Implement TodoStorage.get(id) method in phase-I/src/storage.py
- [X] T013 [P] Implement TodoStorage.get_all() method returning list in phase-I/src/storage.py
- [X] T014 [P] Implement TodoStorage.delete(id) method in phase-I/src/storage.py
- [X] T015 [P] Implement TodoStorage.exists(id) method in phase-I/src/storage.py

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todos and view their current list

**Independent Test**: Launch console app, add one or more todos via command, display list to verify todos are stored and shown correctly

**Acceptance Scenarios**:
1. Add todo with title → confirmation displayed
2. List multiple todos → all displayed with titles and status
3. List when empty → message indicating no todos exist

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement TodoManager class with storage attribute in phase-I/src/todo_manager.py
- [X] T017 [P] [US1] Implement TodoManager.__init__(storage) in phase-I/src/todo_manager.py
- [X] T018 [US1] Implement TodoManager.add_todo(title) returning (success, message, todo_id) in phase-I/src/todo_manager.py
- [X] T019 [US1] Implement TodoManager.list_todos() returning list of todos in phase-I/src/todo_manager.py
- [X] T020 [P] [US1] Implement parse_command(input_string) returning (command, args) in phase-I/src/cli.py
- [X] T021 [P] [US1] Implement display_welcome() showing welcome and available commands in phase-I/src/cli.py
- [X] T022 [P] [US1] Implement display_todos(todos) with formatting and empty list handling in phase-I/src/cli.py
- [X] T023 [P] [US1] Implement display_success(message) in phase-I/src/cli.py
- [X] T024 [P] [US1] Implement display_error(message) in phase-I/src/cli.py
- [X] T025 [P] [US1] Implement prompt_user() returning user input string in phase-I/src/cli.py
- [X] T026 [US1] Implement handle_add(manager, args) command handler in phase-I/src/main.py
- [X] T027 [US1] Implement handle_list(manager, args) command handler in phase-I/src/main.py
- [X] T028 [US1] Implement run_app() main loop with TodoManager initialization in phase-I/src/main.py
- [X] T029 [US1] Implement main() entry point with error handling in phase-I/src/main.py
- [X] T030 [US1] Add empty title validation error handling in add command in phase-I/src/main.py
- [X] T031 [US1] Add title length (>500 chars) validation error handling in add command in phase-I/src/main.py
- [X] T032 [US1] Add empty list message handling in list command in phase-I/src/main.py

**Checkpoint**: ✅ User Story 1 complete - can add and view todos independently

---

## Phase 4: User Story 2 - Mark Todos as Complete (Priority: P2)

**Goal**: Enable users to mark todos as complete and distinguish completed from pending

**Independent Test**: Create several todos, mark specific ones as complete via command, verify status changes correctly when listing

**Acceptance Scenarios**:
1. Mark specific todo as complete → status changes to completed
2. List todos → clearly distinguish completed vs pending visually
3. Mark non-existent todo → appropriate error message

### Implementation for User Story 2

- [X] T033 [US2] Implement TodoManager.complete_todo(id) returning (success, message) in phase-I/src/todo_manager.py
- [X] T034 [US2] Update display_todos() to visually distinguish pending vs completed (e.g., checkboxes, colors) in phase-I/src/cli.py
- [X] T035 [US2] Implement handle_complete(manager, args) command handler in phase-I/src/main.py
- [X] T036 [US2] Add parse_command() support for complete command in phase-I/src/cli.py
- [X] T037 [US2] Add invalid ID error handling in complete command in phase-I/src/main.py
- [X] T038 [US2] Add non-existent todo error handling in complete command in phase-I/src/main.py

**Checkpoint**: ✅ User Stories 1 AND 2 both work independently

---

## Phase 5: User Story 3 - Delete Todos (Priority: P3)

**Goal**: Enable users to delete todos that are no longer needed

**Independent Test**: Create todos, delete specific ones via command, verify they no longer appear in list

**Acceptance Scenarios**:
1. Delete specific todo → todo removed from list
2. Delete non-existent todo → appropriate error message
3. Delete all todos → list shows message indicating no todos exist

### Implementation for User Story 3

- [X] T039 [US3] Implement TodoManager.delete_todo(id) returning (success, message) in phase-I/src/todo_manager.py
- [X] T040 [US3] Implement handle_delete(manager, args) command handler in phase-I/src/main.py
- [X] T041 [US3] Add parse_command() support for delete command in phase-I/src/cli.py
- [X] T042 [US3] Add invalid ID error handling in delete command in phase-I/src/main.py
- [X] T043 [US3] Add non-existent todo error handling in delete command in phase-I/src/main.py

**Checkpoint**: ✅ User Stories 1, 2, AND 3 all work independently

---

## Phase 6: User Story 4 - Edit Todo Titles (Priority: P4)

**Goal**: Enable users to edit todo titles to correct mistakes or update descriptions

**Independent Test**: Create a todo, edit its title via command, verify updated title appears when listing

**Acceptance Scenarios**:
1. Edit todo title → title updated
2. Edit non-existent todo → appropriate error message
3. Edit with empty title → error message, original title unchanged

### Implementation for User Story 4

- [X] T044 [US4] Implement TodoManager.edit_todo(id, new_title) returning (success, message) in phase-I/src/todo_manager.py
- [X] T045 [US4] Implement handle_edit(manager, args) command handler in phase-I/src/main.py
- [X] T046 [US4] Add parse_command() support for edit command in phase-I/src/cli.py
- [X] T047 [US4] Add invalid ID error handling in edit command in phase-I/src/main.py
- [X] T048 [US4] Add empty title validation error handling in edit command in phase-I/src/main.py
- [X] T049 [US4] Add title length (>500 chars) validation error handling in edit command in phase-I/src/main.py

**Checkpoint**: ✅ All 4 user stories complete and independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, help system, and application lifecycle improvements

- [X] T050 [P] Implement display_help() listing all commands with usage examples in phase-I/src/cli.py
- [X] T051 [P] Implement handle_help() command handler in phase-I/src/main.py
- [X] T052 [P] Add parse_command() support for help command in phase-I/src/cli.py
- [X] T053 [P] Implement handle_exit() with goodbye message in phase-I/src/main.py
- [X] T054 [P] Add parse_command() support for exit and quit commands in phase-I/src/cli.py
- [X] T055 Add invalid command error handling with help suggestion in phase-I/src/main.py
- [X] T056 [P] Add welcome message display on startup in phase-I/src/main.py
- [X] T057 [P] Add goodbye message display on exit in phase-I/src/main.py
- [X] T058 Add graceful error handling for unexpected exceptions in main() in phase-I/src/main.py
- [X] T059 [P] Update README.md with complete command reference and examples in phase-I/README.md
- [X] T060 [P] Add startup time optimization (ensure < 2 seconds) in phase-I/src/main.py
- [X] T061 Validate all 7 edge cases from specification are handled:
  - [X] T061a Edge case: Invalid command handling (displays error + help suggestion)
  - [X] T061b Edge case: Invalid todo ID handling (negative, out of range)
  - [X] T061c Edge case: Empty title rejection
  - [X] T061d Edge case: Long title rejection (>500 characters)
  - [X] T061e Edge case: Application startup (welcome message + help)
  - [X] T061f Edge case: Application exit (quit/exit command + goodbye message)
  - [X] T061g Edge case: Empty list handling (appropriate message)
- [X] T062 Run manual testing checklist from plan.md (all user stories P1-P4)
- [X] T063 [P] Code quality review and validation:
  - [X] T063a Verify clear, descriptive naming for functions, variables, classes (NFR-002)
  - [X] T063b Verify documentation added for non-obvious logic (NFR-003)
  - [X] T063c Verify no over-engineering or premature abstraction (NFR-004)
  - [X] T063d Verify Python best practices followed (NFR-001)
- [X] T064 [P] Performance validation:
  - [X] T064a Verify all user operations provide feedback within 1 second (NFR-006)
  - [X] T064b Test with 50 todos to ensure no performance degradation (NFR-007)
  - [X] T064c Verify application startup time is under 2 seconds (NFR-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 display but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- TodoManager methods before CLI display functions
- CLI functions before command handlers in main
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005 can all run in parallel

**Phase 2 (Foundational)**: T006, T007, T008 (models.py) can run parallel to T009-T015 (storage.py)

**Phase 3 (US1)**:
- T016, T017 (TodoManager init) parallel
- T020-T025 (all CLI functions) can run in parallel
- T018, T019 must complete before T026, T027

**Phase 4 (US2)**: T034, T036 can run parallel to T033

**Phase 5 (US3)**: T041 can run parallel to T039

**Phase 6 (US4)**: T046 can run parallel to T044

**Phase 7 (Polish)**: T050, T051, T052, T053, T054, T056, T057, T059, T060, T063, T064 can all run in parallel

**Cross-Story Parallelization**: After Phase 2 completes, US1, US2, US3, US4 can be developed in parallel by different developers

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch these in parallel:

# TodoManager methods (phase-I/src/todo_manager.py):
Task T016: "Implement TodoManager class with storage attribute"
Task T017: "Implement TodoManager.__init__(storage)"

# CLI functions (phase-I/src/cli.py):
Task T020: "Implement parse_command(input_string)"
Task T021: "Implement display_welcome()"
Task T022: "Implement display_todos(todos)"
Task T023: "Implement display_success(message)"
Task T024: "Implement display_error(message)"
Task T025: "Implement prompt_user()"
```

---

## Parallel Example: Foundational Phase

```bash
# After Setup completes, launch models and storage in parallel:

# Models (phase-I/src/models.py):
Task T006: "Implement Todo class with attributes"
Task T007: "Implement validate_title() function"
Task T008: "Add Todo.__str__() and to_dict() methods"

# Storage (phase-I/src/storage.py):
Task T009: "Implement TodoStorage class with _todos dict and _next_id"
Task T010: "Implement TodoStorage.get_next_id()"
Task T011: "Implement TodoStorage.add(todo)"
Task T012: "Implement TodoStorage.get(id)"
Task T013: "Implement TodoStorage.get_all()"
Task T014: "Implement TodoStorage.delete(id)"
Task T015: "Implement TodoStorage.exists(id)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T015) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T016-T032)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can add todos
   - Can list todos
   - Empty list handled
   - Invalid input rejected
5. Demo/review if ready

**Estimated Tasks for MVP**: 32 tasks (Setup + Foundation + US1)

### Incremental Delivery

1. **Setup + Foundational** (T001-T015) → Foundation ready ✅
2. **Add User Story 1** (T016-T032) → Test independently → Demo (MVP!) 🎯
3. **Add User Story 2** (T033-T038) → Test independently → Demo
4. **Add User Story 3** (T039-T043) → Test independently → Demo
5. **Add User Story 4** (T044-T049) → Test independently → Demo
6. **Polish** (T050-T062) → Final validation → Production ready 🚀

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

- **Developer A**: User Story 1 (T016-T032)
- **Developer B**: User Story 2 (T033-T038)
- **Developer C**: User Story 3 (T039-T043)
- **Developer D**: User Story 4 (T044-T049)

Then team converges on Polish phase together.

---

## Task Summary

- **Total Tasks**: 64 (with 17 validation subtasks)
- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 10 tasks
- **Phase 3 (US1 - Create/View)**: 17 tasks 🎯 MVP
- **Phase 4 (US2 - Complete)**: 6 tasks
- **Phase 5 (US3 - Delete)**: 5 tasks
- **Phase 6 (US4 - Edit)**: 6 tasks
- **Phase 7 (Polish)**: 15 tasks (includes enhanced validation)
  - T050-T060: Implementation tasks (11 tasks)
  - T061: Edge case validation with 7 explicit subtasks (T061a-T061g)
  - T062: Manual testing checklist
  - T063: Code quality review with 4 validation subtasks (T063a-T063d)
  - T064: Performance validation with 3 validation subtasks (T064a-T064c)

**Parallel Opportunities**: 34 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 = 32 tasks

**Independent User Stories**: US1, US2, US3, US4 can all be tested independently

---

## Constitutional Compliance

Per `.specify/memory/constitution.md`:

✅ **Phase Discipline (§2)**: All tasks confined to Phase I scope only
✅ **Output Directory (§2.4)**: All code outputs to `phase-I/` directory
✅ **Technology Stack (§2.2)**: Python only, no databases, no web interfaces
✅ **Phase Prohibitions (§2.2)**: NO persistence, NO GUI, NO web interfaces
✅ **SpecKitPlus Workflow (§3)**: Following Specification → Planning → Tasks → Implementation
✅ **No Phase II+ Features (§2.1)**: Strictly in-memory, console-only

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story**: Independently completable and testable
- **Commit strategy**: Commit after each task or logical group
- **Checkpoints**: Stop at any checkpoint to validate story independently
- **Validation**: Use manual testing checklist from plan.md
- **Character limit**: Strictly enforce 500-character validation
- **Error handling**: Never crash on invalid input - always provide helpful feedback
- **Performance**: Ensure startup < 2 seconds, operations < 1 second

---

**Phase I Tasks Status**: ✅ Complete and ready for implementation
**Next Step**: Begin implementation with Phase 1 (Setup) using `/sp.implement`
