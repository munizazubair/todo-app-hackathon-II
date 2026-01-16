# Implementation Tasks: Phase II Full-Stack Web Application

**Branch**: `002-phase-ii-web-app` | **Date**: 2025-12-31
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Task Overview

This document breaks down the Phase II Full-Stack Web Application implementation into atomic, executable tasks organized by user story. Each task references the primary agent responsible and the skills they use.

**Total Tasks**: 157
**Estimated Effort**: 150 story points
**Parallel Opportunities**: 42 parallelizable tasks (marked with [P])

## Technology Stack

- **Frontend**: Next.js 14+, React 18+, TypeScript 5.0+, Tailwind CSS 3+, shadcn/ui
- **Backend**: FastAPI 0.100+, Python 3.11+, Pydantic, SQLModel 0.0.14+
- **Database**: Neon DB (PostgreSQL 15+), Alembic 1.12+
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)

## Skills & Agents

**Skills Available**:
- nextjs-skill - Next.js 14+ App Router scaffolding
- tailwind-css-skill - Tailwind CSS 3+ responsive design
- shadcn-skill - shadcn/ui accessible components
- fastapi-skill - FastAPI application structure
- neon-postgres-skill - Neon DB setup and migrations

**Agents**:
- Full-Stack Architecture Expert - System design, integration
- Database Expert - Schema, migrations, optimization
- Backend Expert - FastAPI, REST API, validation
- Frontend Expert - Next.js, React components, state
- UI/UX Expert - Design, accessibility, responsiveness

---

## Phase 1: Setup & Foundation

**Goal**: Initialize project structure, configure environment, and set up development tooling.

### Environment & Structure

- [X] T001 Create phase-II/ root directory and initialize git
- [X] T002 Create backend/ directory structure with api/, core/, db/, models/, schemas/, migrations/
- [X] T003 Create frontend/ directory structure with app/, components/, lib/, types/
- [X] T004 Create backend/requirements.txt with FastAPI, SQLModel, Alembic, pytest dependencies
- [X] T005 Create frontend/package.json with Next.js, React, TypeScript, Tailwind, shadcn/ui dependencies
- [X] T006 Initialize backend virtual environment and install dependencies (python -m venv .venv)
- [X] T007 Initialize frontend node_modules and install dependencies (npm install)
- [X] T008 Create .env.example files for backend (DATABASE_URL, API_PORT) and frontend (NEXT_PUBLIC_API_URL)
- [X] T009 Create .gitignore with __pycache__/, .venv/, node_modules/, .next/, .env
- [X] T010 [P] Create backend/README.md with setup instructions (Agent: Backend Expert, Skills: fastapi-skill)
- [X] T011 [P] Create frontend/README.md with setup instructions (Agent: Frontend Expert, Skills: nextjs-skill)

---

## Phase 2: Foundational Layer (Blocking Prerequisites)

**Goal**: Set up database connection, base models, and core infrastructure needed by all user stories.

**Agent**: Database Expert, Backend Expert
**Skills**: neon-postgres-skill, fastapi-skill

### Database Foundation

- [X] T012 Create backend/db/base.py with SQLModel Base class
- [X] T013 Create backend/db/database.py with get_engine(), get_session(), connection pooling config
- [X] T014 Create backend/core/config.py with Settings class (DATABASE_URL, API_HOST, API_PORT, CORS_ORIGINS)
- [X] T015 Initialize Alembic in backend/migrations/ (alembic init migrations)
- [X] T016 Configure Alembic env.py to use SQLModel metadata and DATABASE_URL from config
- [X] T017 Create backend/models/__init__.py exporting all models
- [X] T018 Create backend/schemas/__init__.py exporting all schemas

### Backend Foundation

- [X] T019 Create backend/main.py with FastAPI() app initialization
- [X] T020 Configure CORS middleware in backend/main.py using CORS_ORIGINS from config
- [X] T021 Add startup event to backend/main.py to test database connection
- [X] T022 [P] Add shutdown event to backend/main.py to dispose database engine
- [X] T023 Create backend/api/__init__.py and configure APIRouter
- [X] T024 [P] Create backend/core/messages.py migrating error messages from Phase I constants.py

### Frontend Foundation

- [X] T025 Initialize Next.js 14 with App Router in frontend/ (npx create-next-app@latest)
- [X] T026 Configure Tailwind CSS in frontend/tailwind.config.ts with custom theme colors
- [X] T027 Initialize shadcn/ui in frontend/ (npx shadcn-ui@latest init)
- [X] T028 Create frontend/app/layout.tsx with root layout, fonts, and metadata
- [X] T029 [P] Create frontend/lib/utils.ts with cn() helper for className merging
- [X] T030 Create frontend/types/todo.ts with Todo, TodoCreate, TodoUpdate TypeScript interfaces
- [X] T031 Create frontend/lib/constants.ts migrating constants from Phase I constants.py

---

## Phase 3: User Story 1 - Web-Based Todo Management (P1)

**Goal**: Implement core CRUD operations for todos via web interface

**Priority**: P1 (Highest - MVP Feature)
**User Story**: US1 from spec.md
**Agent**: Full-Stack (coordination), Database Expert, Backend Expert, Frontend Expert, UI/UX Expert
**Skills**: neon-postgres-skill, fastapi-skill, nextjs-skill, tailwind-css-skill, shadcn-skill

**Independent Test**: User can open browser, view todos, create a new todo, mark it complete, edit it, and delete it - all via web UI.

### Database Layer (US1)

- [X] T032 [US1] Create backend/models/todo.py with SQLModel Todo class (id, title, status, category, due_date, created_at, updated_at, version)
- [X] T033 [US1] Generate Alembic migration for todos table (alembic revision --autogenerate -m "create todos table")
- [X] T034 [US1] Review and apply migration (alembic upgrade head)
- [X] T035 [P] [US1] Create database indexes on status and created_at columns
- [X] T036 [P] [US1] Add updated_at trigger in migration for automatic timestamp updates

### Backend API (US1)

- [X] T037 [US1] Create backend/schemas/todo.py with TodoBase, TodoCreate, TodoUpdate, TodoInDB Pydantic models
- [X] T038 [US1] Add title validation in TodoCreate (min_length=1, max_length=500, strip whitespace)
- [X] T039 [US1] Create backend/api/todos.py with APIRouter for /api/todos
- [X] T040 [US1] Implement POST /api/todos endpoint (create todo, return 201 Created)
- [X] T041 [US1] Implement GET /api/todos endpoint (list all todos, return 200 OK)
- [X] T042 [US1] Implement GET /api/todos/{id} endpoint (get single todo, return 200 OK or 404)
- [X] T043 [US1] Implement PUT /api/todos/{id} endpoint (update todo, check version for optimistic locking, return 200 or 409)
- [X] T044 [US1] Implement DELETE /api/todos/{id} endpoint (delete todo, return 204 No Content)
- [X] T045 [US1] Implement PATCH /api/todos/{id}/complete endpoint (toggle status, return 200 OK)
- [X] T046 [US1] Register todos router in backend/main.py under /api prefix
- [X] T047 [P] [US1] Create GET /api/health endpoint returning {"status": "healthy"}
- [X] T048 [P] [US1] Add error handling middleware for validation errors (return 400 with details)
- [X] T049 [P] [US1] Add error handling middleware for 404 Not Found (return custom error format)

### Frontend API Client (US1)

- [X] T050 [P] [US1] Create frontend/lib/api.ts with base API_URL configuration
- [X] T051 [US1] Implement getTodos() in frontend/lib/api.ts (GET /api/todos)
- [X] T052 [US1] Implement createTodo(data) in frontend/lib/api.ts (POST /api/todos)
- [X] T053 [US1] Implement updateTodo(id, data) in frontend/lib/api.ts (PUT /api/todos/{id})
- [X] T054 [US1] Implement deleteTodo(id) in frontend/lib/api.ts (DELETE /api/todos/{id})
- [X] T055 [US1] Implement toggleComplete(id) in frontend/lib/api.ts (PATCH /api/todos/{id}/complete)

### Frontend UI Components (US1)

- [X] T056 [US1] Install shadcn/ui components: button, card, input, checkbox, dialog, toast (npx shadcn-ui@latest add)
- [X] T057 [US1] Create frontend/components/TodoItem.tsx with title, status checkbox, edit/delete buttons
- [X] T058 [US1] Create frontend/components/TodoList.tsx rendering array of TodoItem components
- [X] T059 [US1] Create frontend/components/TodoForm.tsx with title input and submit/cancel buttons
- [X] T060 [US1] Add client-side validation to TodoForm (title required, max 500 chars)
- [X] T061 [US1] Create frontend/components/DeleteConfirmDialog.tsx using shadcn dialog component
- [X] T062 [US1] Create frontend/app/page.tsx with TodoList and "Add Todo" button
- [X] T063 [US1] Implement create todo flow: button → dialog → TodoForm → API call → refresh list
- [X] T064 [US1] Implement toggle complete: checkbox click → API call → update local state
- [X] T065 [US1] Implement edit todo: edit button → inline form → API call → update display
- [X] T066 [US1] Implement delete todo: delete button → confirm dialog → API call → remove from list
- [X] T067 [P] [US1] Add loading spinner during API calls using shadcn skeleton components
- [X] T068 [P] [US1] Add error toast notifications for API failures using shadcn toast component
- [X] T069 [P] [US1] Add success toast notifications for create/update/delete operations

### Testing (US1)

- [X] T070 [P] [US1] Create backend/tests/test_todos_api.py with pytest fixtures for test database
- [X] T071 [P] [US1] Write backend integration tests for all 6 todo API endpoints
- [X] T072 [P] [US1] Write frontend component tests for TodoForm, TodoItem, TodoList using Jest + RTL
- [X] T071a [P] [US1] Write backend integration test for health check endpoint (verify 200 OK with status "healthy")
- [X] T073 [P] [US1] Verify manual E2E test: Create → View → Edit → Complete → Delete todo via browser

---

## Phase 4: User Story 2 - RESTful API Backend (P1)

**Goal**: Enhance API with pagination, filtering, query parameters, and Swagger documentation

**Priority**: P1
**User Story**: US2 from spec.md
**Agent**: Backend Expert, Full-Stack Architecture Expert
**Skills**: fastapi-skill

**Independent Test**: API supports pagination (limit/offset), returns proper HTTP status codes, and has complete Swagger UI documentation at /docs.

### API Enhancement (US2)

- [X] T074 [US2] Add query parameters to GET /api/todos: limit (default 20), offset (default 0)
- [X] T075 [US2] Implement pagination logic in GET /api/todos (query.limit().offset())
- [X] T076 [US2] Update GET /api/todos response to include total count and pagination metadata
- [X] T077 [P] [US2] Add request_id to error responses using middleware (uuid4())
- [X] T078 [P] [US2] Configure Swagger UI with title, description, version at /docs endpoint
- [X] T079 [P] [US2] Add OpenAPI tags to endpoints for better Swagger organization ("Todos", "Health")
- [X] T080 [P] [US2] Add example request/response bodies to Pydantic schemas for Swagger

### Testing (US2)

- [X] T081 [P] [US2] Write tests for pagination (verify limit/offset work correctly)
- [X] T082 [P] [US2] Write tests for error responses (verify 400, 404, 409 formats)
- [X] T083 [P] [US2] Verify Swagger UI loads, documents all endpoints with examples, and validates API contract completeness

---

## Phase 5: User Story 3 - Database Persistence (P1)

**Goal**: Add database schema enhancements, indexes, and connection pooling optimization

**Priority**: P1
**User Story**: US3 from spec.md
**Agent**: Database Expert
**Skills**: neon-postgres-skill

**Independent Test**: Todos persist across server restarts, timestamps update automatically, and queries on 1000+ todos complete under 100ms.

### Database Enhancement (US3)

- [X] T084 [US3] Create Alembic migration to add category column (VARCHAR(50), nullable)
- [X] T085 [US3] Create Alembic migration to add due_date column (DATE, nullable)
- [X] T086 [US3] Create composite index on (status, due_date) for filtered queries
- [X] T087 [US3] Create index on category column for category filtering
- [X] T088 [US3] Update backend/db/database.py with connection pool settings (pool_size=5, max_overflow=10)
- [X] T089 [P] [US3] Add pool_pre_ping=True to engine for connection health checks
- [X] T090 [P] [US3] Update backend/models/todo.py with category and due_date fields
- [X] T091 [P] [US3] Update backend/schemas/todo.py with category and due_date fields

### Testing (US3)

- [X] T092 [P] [US3] Write test: Create todo, stop server, restart, verify todo still exists
- [X] T093 [P] [US3] Write test: Update todo, verify updated_at timestamp changed
- [X] T094 [P] [US3] Write performance test: Create 1000 todos, query with filter, assert <100ms
- [X] T095 [P] [US3] Run EXPLAIN ANALYZE on filtered query to verify index usage

---

## Phase 6: User Story 4 - Enhanced Features (P2)

**Goal**: Add categories, due dates, search, filtering, and dashboard statistics

**Priority**: P2
**User Story**: US4 from spec.md
**Agent**: Frontend Expert, Backend Expert, UI/UX Expert
**Skills**: nextjs-skill, fastapi-skill, tailwind-css-skill, shadcn-skill

**Independent Test**: User can assign categories, set due dates, filter by status/category, search by title, and view dashboard with statistics.

### Backend API Enhancement (US4)

- [X] T096 [US4] Add query parameter to GET /api/todos: status (filter by pending/completed)
- [X] T097 [US4] Add query parameter to GET /api/todos: category (filter by category name)
- [X] T098 [US4] Add query parameter to GET /api/todos: search (case-insensitive title search using LIKE)
- [X] T099 [US4] Implement filtering logic in GET /api/todos (combine status, category, search filters)
- [X] T100 [US4] Create GET /api/todos/stats endpoint returning {total, pending, completed, overdue}
- [X] T101 [P] [US4] Add validation for category (max 50 chars) in TodoCreate/TodoUpdate schemas
- [X] T102 [P] [US4] Add validation for due_date (YYYY-MM-DD format) in TodoCreate/TodoUpdate schemas

### Frontend UI Enhancement (US4)

- [X] T103 [US4] Update frontend/components/TodoForm.tsx with category input (text field)
- [X] T104 [US4] Update frontend/components/TodoForm.tsx with due_date input (date picker)
- [X] T105 [US4] Create frontend/components/FilterBar.tsx with status dropdown (All/Pending/Completed)
- [X] T106 [US4] Add category filter to FilterBar (text input or dropdown)
- [X] T107 [US4] Create frontend/components/SearchBar.tsx with debounced search input (300ms delay)
- [X] T108 [US4] Update frontend/app/page.tsx to pass filter state to getTodos() API call
- [X] T109 [US4] Add overdue highlighting in TodoItem.tsx (red text/border if due_date < today && !completed)
- [X] T110 [US4] Create frontend/app/dashboard/page.tsx with statistics cards (total, pending, completed, overdue)
- [X] T111 [US4] Create frontend/components/StatCard.tsx for displaying individual statistics
- [X] T112 [US4] Fetch statistics from GET /api/todos/stats in dashboard page
- [X] T113 [P] [US4] Add navigation link to dashboard in frontend/app/layout.tsx nav bar

### Testing (US4)

- [X] T114 [P] [US4] Write backend tests for status/category/search filtering
- [X] T115 [P] [US4] Write backend test for stats endpoint (verify counts)
- [X] T116 [P] [US4] Write frontend tests for FilterBar, SearchBar components
- [X] T117 [P] [US4] Verify manual E2E test: Filter by category, search by title, view dashboard stats

---

## Phase 7: User Story 5 - Data Migration from Phase I (P2)

**Goal**: Create migration script to import Phase I todos into Phase II database

**Priority**: P2
**User Story**: US5 from spec.md
**Agent**: Backend Expert, Database Expert
**Skills**: fastapi-skill, neon-postgres-skill

**Independent Test**: Migration script successfully imports 10 Phase I todos, preserves IDs/titles/status, sets category/due_date to null, and reports summary.

### Migration Script (US5)

- [X] T118 [US5] Create phase-II/scripts/migrate_from_phase_i.py script file
- [X] T119 [US5] Implement read_phase_i_todos() to parse Phase I in-memory format (JSON or pickle)
- [X] T120 [US5] Implement validate_todo_data() to check data integrity before insertion
- [X] T121 [US5] Implement insert_todos_to_db() using SQLModel to insert todos
- [X] T122 [US5] Add duplicate detection (check if ID already exists, skip if duplicate)
- [X] T123 [US5] Generate migration summary report (total migrated, duplicates skipped, errors)
- [X] T124 [P] [US5] Add command-line argument parsing (--source, --dry-run flags)
- [X] T125 [P] [US5] Add logging to migration script (INFO for progress, ERROR for failures)

### Testing (US5)

- [X] T126 [P] [US5] Create test data with 10 Phase I todos in JSON format
- [X] T127 [P] [US5] Run migration script with --dry-run, verify it reports correctly without inserting
- [X] T128 [P] [US5] Run migration script, verify all 10 todos appear in web UI
- [X] T129 [P] [US5] Run migration twice, verify no duplicates created
- [X] T130 [P] [US5] Verify Phase I IDs match Phase II database IDs

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Add final touches, improve UX, and ensure production readiness

**Agent**: Frontend Expert, UI/UX Expert, Full-Stack Architecture Expert
**Skills**: nextjs-skill, tailwind-css-skill, shadcn-skill

### Responsive Design

- [ ] T131 [P] Test UI on mobile (320px width) - adjust TodoList to stack vertically
- [ ] T132 [P] Test UI on tablet (768px width) - use responsive Tailwind breakpoints (md:)
- [ ] T133 [P] Test UI on desktop (1920px width) - ensure max-width container for readability
- [ ] T134 [P] Add touch-friendly button sizes on mobile (min height 44px for accessibility)

### Accessibility

- [ ] T135 [P] Add ARIA labels to all interactive elements (buttons, inputs, checkboxes)
- [ ] T136 [P] Ensure keyboard navigation works (Tab, Enter, Escape)
- [ ] T137 [P] Add focus indicators to all focusable elements (ring-2 ring-blue-500)
- [ ] T138 [P] Test with screen reader (verify labels are descriptive)

### Performance Optimization

- [ ] T139 [P] Add React.memo() to TodoItem component to prevent unnecessary re-renders
- [ ] T140 [P] Use useMemo() for filtered/sorted todo lists
- [ ] T141 [P] Add useCallback() to event handlers to prevent function recreation
- [ ] T142 [P] Optimize images (if any) with Next.js Image component

### Error Handling & Logging

- [ ] T143 [P] Add structured logging to backend using Python logging module
- [ ] T144 [P] Log all database errors with stack traces
- [ ] T145 [P] Add request logging middleware (log method, path, status, duration)
- [ ] T146 [P] Create custom error page frontend/app/error.tsx for unhandled errors

### Documentation

- [ ] T147 [P] Update backend/README.md with API endpoint documentation
- [ ] T148 [P] Update frontend/README.md with component usage examples
- [ ] T149 [P] Create phase-II/README.md with project overview and setup instructions
- [ ] T150 [P] Add inline code comments for complex business logic

### Deployment Preparation

- [ ] T151 Create Dockerfile for backend with Python 3.11 base image
- [ ] T152 Create Dockerfile for frontend with Node 18 base image
- [ ] T153 Create docker-compose.yml for local development (backend + frontend + postgres)
- [ ] T154 Create deployment README with instructions for Vercel (frontend) and Railway (backend)
- [ ] T155 [P] Add health check endpoint verification in deployment docs
- [ ] T156 [P] Document environment variables needed for production

---

## Task Dependencies & Execution Order

### Critical Path (Must Complete Sequentially)

1. **Setup** (T001-T011) → Foundation for all work
2. **Foundation** (T012-T031) → Blocking prerequisites
3. **US1 Database** (T032-T036) → Required before backend API
4. **US1 Backend API** (T037-T049) → Required before frontend
5. **US1 Frontend** (T050-T073) → Core functionality
6. **US2 API Enhancement** (T074-T083) → Extends US1 backend
7. **US3 Database Enhancement** (T084-T095) → Extends US1 database
8. **US4 Enhanced Features** (T096-T117) → Requires US1+US2+US3 complete
9. **US5 Migration** (T118-T130) → Requires US1+US3 database complete
10. **Polish** (T131-T156) → Final touches after all features

### Parallel Execution Opportunities

**Within US1** (can run simultaneously after dependencies met):
- T070-T073 (Testing) - parallel after T069
- T047-T049 (Health/Error handling) - parallel after T046

**Within US2** (all parallel after US1 complete):
- T077-T080 (Documentation)
- T081-T083 (Testing)

**Within US3** (parallel groups):
- T089-T091 (Schema updates) - parallel after T088

**Within US4** (parallel groups):
- T101-T102 (Validation) - parallel after T100
- T114-T117 (Testing) - parallel after T113

**Polish Phase** (most tasks parallel):
- T131-T156 can mostly run in parallel after all user stories complete

### MVP Scope (Minimum Viable Product)

For fastest time-to-value, implement in this order:

**Sprint 1**: Setup + Foundation + US1 (T001-T073)
- Delivers working web UI with full CRUD operations
- Users can create, view, edit, complete, delete todos

**Sprint 2**: US2 + US3 (T074-T095)
- Adds pagination, better API, database persistence

**Sprint 3**: US4 (T096-T117)
- Adds search, filtering, categories, dashboard

**Sprint 4**: US5 + Polish (T118-T156)
- Migration + production readiness

---

## Validation Checklist

Before marking Phase II complete, verify:

- [ ] All 5 user stories have independent test scenarios verified
- [ ] Web UI loads in <2 seconds on average network (SC-001)
- [ ] All Phase I CRUD operations work in web interface (SC-002)
- [ ] API handles 100 concurrent requests without errors (SC-003)
- [ ] Database queries complete in <100ms for 10,000 todos (SC-004)
- [ ] Migration script successfully imports Phase I data (SC-005)
- [ ] No todos lost during migration (SC-006)
- [ ] UI responsive on mobile (320px) and desktop (1920px) (SC-007)
- [ ] API documentation complete and accurate at /docs (SC-008)
- [ ] All Phase I validation rules enforced (SC-009)
- [ ] Application deployed and accessible via public URL (SC-010)

---

**Tasks File Version**: 1.0
**Last Updated**: 2025-12-31
**Generated By**: Claude Sonnet 4.5
**Status**: Ready for Implementation
