# Phase II: Full-Stack Web Application - Feature Specification

## Overview

**Feature Name**: Phase II Web Application
**Short Name**: phase-ii-web-app
**Phase**: 2 of 5
**Priority**: High
**Complexity**: High
**Estimated Effort**: 150 points
**Due Date**: December 14, 2025

## Background

Phase I delivered a functional in-memory console-based todo application with complete CRUD operations. Phase II transforms this into a full-stack web application with persistent storage, introducing a modern web UI, RESTful API, and database layer while preserving all Phase I functionality.

## Goals

1. Provide a modern web-based user interface for todo management
2. Implement a RESTful API backend with FastAPI
3. Add persistent database storage with Neon DB
4. Enhance features with categories, due dates, and search
5. Enable seamless migration from Phase I data model

## Non-Goals

- Mobile native applications (web responsive only)
- Real-time collaboration features (deferred to Phase V)
- Advanced authentication (basic implementation only)
- Offline-first capabilities

## User Stories

### US1: Web-Based Todo Management (P1)
**As a** user
**I want** to manage my todos through a web browser
**So that** I can access my tasks from any device without installing software

**Acceptance Criteria**:
- Users can view all todos in a responsive web interface
- Users can create new todos with title, category, and due date
- Users can mark todos as complete/incomplete via checkbox
- Users can edit todo details inline
- Users can delete todos with confirmation
- UI displays todo count and filters by status
- All Phase I validation rules are enforced client-side and server-side

**Test Scenarios**:
1. Open web browser, navigate to application, see todo list
2. Click "Add Todo" button, fill form, submit, see new todo appear
3. Click checkbox on todo, see status change to completed
4. Click edit icon, modify title, save, see updated title
5. Click delete icon, confirm, see todo removed from list

### US2: RESTful API Backend (P1)
**As a** frontend application
**I want** to interact with todos through a REST API
**So that** I can perform CRUD operations with proper HTTP semantics

**Acceptance Criteria**:
- GET /api/todos returns all todos with pagination
- POST /api/todos creates a new todo and returns 201 Created
- GET /api/todos/{id} returns a single todo or 404
- PUT /api/todos/{id} updates a todo and returns updated resource
- DELETE /api/todos/{id} deletes a todo and returns 204 No Content
- PATCH /api/todos/{id}/complete toggles completion status
- All endpoints validate input and return appropriate error codes
- API documentation available via Swagger UI

**Test Scenarios**:
1. Send GET /api/todos, receive JSON array of todos
2. Send POST /api/todos with valid data, receive 201 with created todo
3. Send POST /api/todos with invalid data, receive 400 with error details
4. Send PUT /api/todos/999, receive 404 Not Found
5. Send DELETE /api/todos/1, receive 204, verify deletion

### US3: Database Persistence (P1)
**As a** system
**I want** to persist todos in a PostgreSQL database
**So that** data survives application restarts

**Acceptance Criteria**:
- Todos are stored in Neon DB PostgreSQL database
- Schema includes id, title, status, created_at, updated_at, due_date, category
- Database migrations managed via Alembic
- Automatic timestamps for created_at and updated_at
- Indexes on status and due_date for performance
- Connection pooling configured for scalability

**Test Scenarios**:
1. Create todo, restart server, verify todo persists
2. Update todo, check updated_at timestamp is current
3. Query todos by status, verify index is used
4. Create 1000 todos, verify query performance remains under 100ms

### US4: Enhanced Features (P2)
**As a** user
**I want** to organize and filter my todos
**So that** I can manage tasks more efficiently

**Acceptance Criteria**:
- Users can assign categories to todos (Work, Personal, Shopping, etc.)
- Users can set due dates for todos
- Users can filter todos by status, category, or due date
- Users can search todos by title text
- UI shows overdue todos in distinct color
- Dashboard displays summary statistics (total, pending, completed, overdue)

**Test Scenarios**:
1. Create todo with category "Work", filter by Work, see only Work todos
2. Create todo with due date yesterday, see it marked as overdue
3. Search for "groceries", see only matching todos
4. View dashboard, see correct counts for all categories

### US5: Data Migration from Phase I (P2)
**As a** Phase I user
**I want** to import my existing todos
**So that** I don't lose my data when upgrading

**Acceptance Criteria**:
- Migration script reads Phase I in-memory format
- All todos preserve their ID, title, status, and created timestamp
- New fields (category, due_date) default to null
- Migration validates data integrity before committing
- Migration provides summary report (total migrated, errors)

**Test Scenarios**:
1. Run migration with 10 Phase I todos, verify all 10 appear in web UI
2. Run migration twice, verify no duplicates created
3. Verify Phase I todo IDs match Phase II database IDs

## Functional Requirements

### Web Frontend (Next.js)

**FR-001**: Application uses Next.js 14+ with App Router
**FR-002**: UI components built with React 18+ and TypeScript
**FR-003**: Styling uses Tailwind CSS for responsive design
**FR-004**: Todo list displays in sortable table or card grid
**FR-005**: Create/Edit forms include title (required), category (optional), due date (optional)
**FR-006**: Client-side validation matches Phase I rules: title max 500 chars, non-empty, trimmed whitespace
**FR-007**: Loading states displayed during API calls
**FR-008**: Error messages shown via toast notifications
**FR-009**: Confirmation dialog before deleting todos
**FR-010**: Filter controls for status (all/pending/completed), category, due date range
**FR-011**: Search input with debounced text filtering
**FR-012**: Dashboard page with statistics cards
**FR-013**: Responsive layout works on mobile, tablet, desktop

### Backend API (FastAPI)

**FR-014**: API built with FastAPI 0.100+
**FR-015**: All endpoints return JSON responses
**FR-016**: Request validation uses Pydantic models
**FR-017**: CORS configured to allow frontend origin
**FR-018**: Error responses include status code, message, and request ID
**FR-019**: GET /api/todos supports query parameters: status, category, search, limit, offset
**FR-020**: POST /api/todos validates title length and trimming
**FR-021**: PUT /api/todos/{id} performs optimistic locking via version field
**FR-022**: PATCH /api/todos/{id}/complete toggles status atomically
**FR-023**: Health check endpoint at /api/health returns 200 OK
**FR-024**: API documentation auto-generated at /docs (Swagger UI)

### Database (SQLModel + Neon DB)

**FR-025**: Database uses SQLModel ORM with PostgreSQL dialect
**FR-026**: Todo table schema:
- id: Integer, Primary Key, Auto-increment
- title: String(500), Not Null
- status: Enum('pending', 'completed'), Default='pending'
- category: String(50), Nullable
- due_date: Date, Nullable
- created_at: Timestamp, Default=now()
- updated_at: Timestamp, Default=now(), OnUpdate=now()
- version: Integer, Default=1 (for optimistic locking)

**FR-027**: Database migrations managed via Alembic
**FR-028**: Connection string stored in environment variable DATABASE_URL
**FR-029**: Connection pooling with max 20 connections
**FR-030**: Indexes created on: status, category, due_date, created_at

### Validation & Error Handling

**FR-031**: Title validation: non-empty, max 500 characters, trimmed
**FR-032**: Status validation: must be 'pending' or 'completed'
**FR-033**: Category validation: max 50 characters if provided
**FR-034**: Due date validation: must be valid date format (YYYY-MM-DD), past dates allowed for historical todos
**FR-035**: API returns 400 Bad Request for validation errors
**FR-036**: API returns 404 Not Found for non-existent todo IDs
**FR-037**: API returns 409 Conflict for optimistic locking failures
**FR-038**: All database errors logged with stack traces

## Success Criteria

**SC-001**: Web UI loads in under 2 seconds on 4G network (50ms latency, 10Mbps download)
**SC-002**: All Phase I CRUD operations work in web interface
**SC-003**: API handles 100 concurrent requests without errors
**SC-004**: Database SELECT queries with filters and pagination complete in under 100ms for up to 10,000 todos
**SC-005**: Migration script successfully imports Phase I data
**SC-006**: No todos lost during migration (100% data integrity)
**SC-007**: UI is responsive on mobile (320px width) and desktop (1920px width)
**SC-008**: API documentation is complete and accurate
**SC-009**: All validation rules from Phase I are enforced
**SC-010**: Application deployed and accessible via public URL

## Integration with Phase I

### Component Mapping

| Phase I Component | Phase II Equivalent | Migration Notes |
|-------------------|---------------------|-----------------|
| `phase-I/src/models.py` (Todo class) | `backend/models/todo.py` (SQLModel) | Add database fields (id auto-increment, timestamps, category, due_date) |
| `phase-I/src/storage.py` (TodoStorage) | `backend/db/database.py` + SQLAlchemy | Replace dict storage with database queries |
| `phase-I/src/todo_manager.py` (TodoManager) | `backend/api/todos.py` (FastAPI routes) | Convert methods to REST endpoints |
| `phase-I/src/cli.py` (CLI functions) | `frontend/components/TodoList.tsx` | Replace console display with React components |
| `phase-I/src/main.py` (command loop) | `frontend/app/page.tsx` (Next.js page) | Replace CLI loop with web UI event handlers |
| `phase-I/src/constants.py` | `backend/core/constants.py` + `frontend/lib/constants.ts` | Share constants across frontend/backend |

### Business Logic Preservation

All Phase I business logic is preserved in Phase II:

1. **Validation Rules** (from `models.py::validate_title`):
   - Implemented in backend: `backend/schemas/todo.py` (Pydantic validators)
   - Implemented in frontend: `frontend/lib/validation.ts` (client-side)

2. **CRUD Operations** (from `todo_manager.py`):
   - `add_todo` → POST /api/todos
   - `list_todos` → GET /api/todos
   - `complete_todo` → PATCH /api/todos/{id}/complete
   - `edit_todo` → PUT /api/todos/{id}
   - `delete_todo` → DELETE /api/todos/{id}

3. **Error Messages** (from `constants.py`):
   - Migrated to `backend/core/messages.py`
   - Used in API error responses and frontend toast notifications

### File Structure

```
todo-app-hackathon-II/
├── phase-I/                          # Existing Phase I implementation (preserved)
│   └── src/
│       ├── models.py                 # Original Todo class and validation
│       ├── storage.py                # Original in-memory storage
│       ├── todo_manager.py           # Original business logic
│       ├── cli.py                    # Original CLI interface
│       └── main.py                   # Original command loop
│
├── phase-II/                         # New Phase II implementation
│   ├── backend/                      # FastAPI Backend
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── todos.py              # REST endpoints (maps to todo_manager.py methods)
│   │   ├── core/
│   │   │   ├── config.py             # Environment configuration
│   │   │   ├── constants.py          # Migrated from phase-I/src/constants.py
│   │   │   └── messages.py           # Error messages
│   │   ├── db/
│   │   │   ├── database.py           # Database connection and session
│   │   │   └── base.py               # SQLModel base class
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── todo.py               # SQLModel Todo (extends phase-I/src/models.py)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── todo.py               # Pydantic request/response models
│   │   ├── migrations/
│   │   │   └── versions/             # Alembic migration files
│   │   ├── main.py                   # FastAPI application entry point
│   │   └── requirements.txt          # Backend dependencies
│   │
│   ├── frontend/                     # Next.js Frontend
│   │   ├── app/
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Homepage with todo list (replaces main.py loop)
│   │   │   └── dashboard/
│   │   │       └── page.tsx          # Dashboard with statistics
│   │   ├── components/
│   │   │   ├── TodoList.tsx          # Main todo list (replaces cli.py display_todos)
│   │   │   ├── TodoItem.tsx          # Individual todo card
│   │   │   ├── TodoForm.tsx          # Create/edit form (replaces cli.py prompts)
│   │   │   ├── FilterBar.tsx         # Status/category filters
│   │   │   └── SearchBar.tsx         # Text search
│   │   ├── lib/
│   │   │   ├── api.ts                # API client functions
│   │   │   ├── constants.ts          # Frontend constants (from phase-I constants.py)
│   │   │   └── validation.ts         # Client-side validation (from models.py)
│   │   ├── types/
│   │   │   └── todo.ts               # TypeScript interfaces
│   │   ├── package.json              # Frontend dependencies
│   │   └── next.config.js            # Next.js configuration
│   │
│   └── scripts/
│       └── migrate_from_phase_i.py   # Data migration script
│
└── specs/
    └── 002-phase-ii-web-app/
        └── spec.md                   # This specification
```

## User Flow Examples

### Phase I (Console) vs Phase II (Web)

#### Example 1: Creating a Todo

**Phase I Console**:
```
> add Buy groceries
[SUCCESS] Todo created with ID 1: "Buy groceries" (pending)
```

**Phase II Web**:
1. User clicks "Add Todo" button
2. Modal opens with form fields:
   - Title: "Buy groceries"
   - Category: "Shopping"
   - Due Date: "2025-12-20"
3. User clicks "Create"
4. Toast notification: "Todo created successfully"
5. New todo appears in list with badge "Shopping" and due date

**API Request** (Phase II):
```http
POST /api/todos
Content-Type: application/json

{
  "title": "Buy groceries",
  "category": "Shopping",
  "due_date": "2025-12-20"
}
```

**API Response**:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "title": "Buy groceries",
  "status": "pending",
  "category": "Shopping",
  "due_date": "2025-12-20",
  "created_at": "2025-12-31T10:00:00Z",
  "updated_at": "2025-12-31T10:00:00Z"
}
```

#### Example 2: Listing Todos

**Phase I Console**:
```
> list
============================================================
  YOUR TODOS
============================================================

  1. [ ] Buy groceries
  2. [X] Read documentation

============================================================
  Total: 2 todo(s)
============================================================
```

**Phase II Web**:
- User navigates to homepage
- Todo list displays as cards:
  - Card 1: "Buy groceries" | Badge: Shopping | Due: Dec 20 | ☐ Pending
  - Card 2: "Read documentation" | Badge: Work | ☑ Completed
- Filter bar shows: "All (2) | Pending (1) | Completed (1)"
- Search bar available at top

**API Request**:
```http
GET /api/todos?limit=20&offset=0
```

**API Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "status": "pending",
      "category": "Shopping",
      "due_date": "2025-12-20",
      "created_at": "2025-12-31T10:00:00Z",
      "updated_at": "2025-12-31T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Read documentation",
      "status": "completed",
      "category": "Work",
      "due_date": null,
      "created_at": "2025-12-30T09:00:00Z",
      "updated_at": "2025-12-31T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 20,
  "offset": 0
}
```

#### Example 3: Marking Todo as Complete

**Phase I Console**:
```
> complete 1
[SUCCESS] Todo 1 marked as completed
```

**Phase II Web**:
1. User clicks checkbox next to "Buy groceries"
2. Checkbox animates to checked state
3. Todo card background changes to light green
4. Status badge updates to "Completed"

**API Request**:
```http
PATCH /api/todos/1/complete
```

**API Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "title": "Buy groceries",
  "status": "completed",
  "category": "Shopping",
  "due_date": "2025-12-20",
  "created_at": "2025-12-31T10:00:00Z",
  "updated_at": "2025-12-31T12:30:00Z"
}
```

#### Example 4: Editing a Todo

**Phase I Console**:
```
> edit 1 Buy milk and eggs
[SUCCESS] Todo 1 updated
```

**Phase II Web**:
1. User clicks edit icon on todo card
2. Inline form appears with current values:
   - Title: "Buy groceries" → changes to "Buy milk and eggs"
   - Category: "Shopping" (unchanged)
   - Due Date: "2025-12-20" (unchanged)
3. User clicks "Save"
4. Toast notification: "Todo updated successfully"
5. Card updates with new title

**API Request**:
```http
PUT /api/todos/1
Content-Type: application/json

{
  "title": "Buy milk and eggs",
  "category": "Shopping",
  "due_date": "2025-12-20"
}
```

**API Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "title": "Buy milk and eggs",
  "status": "completed",
  "category": "Shopping",
  "due_date": "2025-12-20",
  "created_at": "2025-12-31T10:00:00Z",
  "updated_at": "2025-12-31T13:00:00Z"
}
```

#### Example 5: Deleting a Todo

**Phase I Console**:
```
> delete 1
[SUCCESS] Todo 1 deleted
```

**Phase II Web**:
1. User clicks delete icon (trash can) on todo card
2. Confirmation dialog appears: "Delete 'Buy milk and eggs'? This cannot be undone."
3. User clicks "Confirm"
4. Todo card animates and fades out
5. Toast notification: "Todo deleted successfully"

**API Request**:
```http
DELETE /api/todos/1
```

**API Response**:
```http
HTTP/1.1 204 No Content
```

## Technical Constraints

1. **Technology Stack** (from Hackathon-II-Todo-App.md):
   - Frontend: Next.js 14+, React 18+, TypeScript, Tailwind CSS
   - Backend: FastAPI 0.100+, Python 3.11+
   - ORM: SQLModel 0.0.14+
   - Database: Neon DB (PostgreSQL 15+)
   - Migrations: Alembic

2. **Performance**:
   - API response time < 200ms for simple queries
   - Page load time < 2 seconds
   - Support up to 10,000 todos per user

3. **Security**:
   - All API inputs validated
   - SQL injection prevention via ORM
   - CORS configured for production domain only
   - Environment variables for secrets

4. **Compatibility**:
   - Browser support: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
   - Mobile responsive: 320px minimum width

## Out of Scope

- User authentication (placeholder implementation only)
- Multi-user support and data isolation
- Real-time collaboration features
- Email notifications for due dates
- File attachments on todos
- Recurring todos
- Subtasks and nested todos
- Export to external formats (CSV, JSON)
- Third-party integrations (calendar sync, etc.)

## Dependencies

- Phase I implementation must be complete and validated
- Neon DB account created and connection string available
- Deployment environment configured (Vercel for frontend, Railway/Render for backend)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database connection failures | High | Medium | Implement retry logic with exponential backoff |
| Data migration errors | High | Low | Validate Phase I data before migration, provide rollback |
| API rate limiting issues | Medium | Low | Implement client-side caching and request debouncing |
| Browser compatibility issues | Medium | Medium | Test on all target browsers, use polyfills |
| Slow query performance | Medium | Medium | Create database indexes, implement pagination |

## Open Questions

None at this time. All requirements are clearly defined based on Phase I implementation and Hackathon-II-Todo-App.md specifications.

---

**Document Version**: 1.0
**Last Updated**: 2025-12-31
**Author**: Claude Sonnet 4.5
**Status**: Ready for Planning
