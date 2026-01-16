# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `002-phase-ii-web-app` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-phase-ii-web-app/spec.md`

## Summary

Phase II transforms the Phase I in-memory console Todo application into a full-stack web application with persistent storage. The implementation adds a modern web UI (Next.js + React + TypeScript + Tailwind CSS), RESTful API backend (FastAPI + Python), and database layer (Neon PostgreSQL + SQLModel), while preserving all Phase I business logic and validation rules.

**Technical approach**: Three-tier architecture with clear separation between presentation (Next.js frontend), application (FastAPI backend), and data (PostgreSQL database) layers. Migration path from Phase I preserves data integrity and IDs.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Next.js 14+, React 18+, FastAPI 0.100+, SQLModel 0.0.14+, Neon DB (PostgreSQL 15+), Alembic 1.12+
**Storage**: Neon DB (serverless PostgreSQL with connection pooling)
**Testing**: pytest (backend), Jest + React Testing Library (frontend), manual E2E testing
**Target Platform**: Web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), Linux/macOS/Windows server
**Project Type**: Web application (frontend + backend + database)
**Performance Goals**:
- Web UI loads in <2 seconds on 4G network (50ms latency, 10Mbps download)
- API response time <200ms for simple queries (single SELECT)
- Database queries <100ms for up to 10,000 todos (SELECT with filters and pagination)
**Constraints**:
- Browser support: minimum 320px width for mobile
- Must preserve all Phase I validation rules and business logic
- Connection pooling: max 20 concurrent database connections
- No user authentication (placeholder only)
- No real-time features (deferred to Phase V)
**Scale/Scope**:
- Target: 10,000 todos per user
- 5 user stories (US1-US5)
- 157 atomic tasks across 8 implementation phases
- 150 story points estimated effort

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Phase Discipline** (Section 2.1-2.2): PASS
- This is Phase II only; no Phase III+ features included
- Does not violate phase isolation
- Output directory: `/phase-II/` (backend/, frontend/, scripts/)
- Phase I preserved under `/phase-I/` (no modifications)

✅ **Technology Stack** (Section 2.2 - Phase II): PASS
- Frontend: Next.js 14+, React 18+, TypeScript 5.0+, Tailwind CSS 3+ ✓
- Backend: FastAPI 0.100+, Python 3.11+ ✓
- ORM: SQLModel 0.0.14+ ✓
- Database: Neon DB (PostgreSQL 15+) ✓
- Migrations: Alembic 1.12+ ✓
- All technologies match approved Phase II stack

✅ **Output Directory Discipline** (Section 2.4): PASS
- Implementation outputs → `/phase-II/backend/` and `/phase-II/frontend/`
- Planning artifacts → `/specs/002-phase-ii-web-app/`
- No mixing of phase-specific code across directories

✅ **Security** (Section 4): PASS
- All API inputs validated via Pydantic
- SQL injection prevention via SQLModel ORM
- Environment variables for DATABASE_URL and secrets
- CORS configured for production domain only
- No hardcoded credentials in code

✅ **Documentation Standards** (Section 5): PASS
- PHR will be created for each major implementation step
- ADRs suggested for architecturally significant decisions
- README files for backend and frontend setup
- Inline comments for complex business logic
- API documentation via Swagger UI at /docs

**Verdict**: ✅ ALL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-ii-web-app/
├── spec.md                   # Feature specification (complete)
├── plan.md                   # This file
├── tasks.md                  # Task breakdown (complete, 156 tasks)
└── [No research.md needed - Phase I implementation provides all context]
```

### Source Code (repository root)

```text
phase-II/
├── backend/                      # FastAPI Backend
│   ├── api/
│   │   ├── __init__.py
│   │   └── todos.py              # REST endpoints for todos
│   ├── core/
│   │   ├── config.py             # Settings (DATABASE_URL, CORS, etc.)
│   │   ├── constants.py          # Migrated from Phase I
│   │   └── messages.py           # Error messages
│   ├── db/
│   │   ├── database.py           # Engine, session, connection pooling
│   │   └── base.py               # SQLModel Base class
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py               # SQLModel Todo (with DB fields)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── todo.py               # Pydantic models (create, update, response)
│   ├── migrations/
│   │   └── versions/             # Alembic migration files
│   ├── tests/
│   │   ├── test_todos_api.py     # API integration tests
│   │   └── conftest.py           # pytest fixtures
│   ├── main.py                   # FastAPI app entry point
│   ├── requirements.txt          # Backend dependencies
│   └── README.md                 # Backend setup instructions
│
├── frontend/                     # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Homepage with todo list
│   │   └── dashboard/
│   │       └── page.tsx          # Statistics dashboard
│   ├── components/
│   │   ├── TodoList.tsx          # List of todos
│   │   ├── TodoItem.tsx          # Individual todo card
│   │   ├── TodoForm.tsx          # Create/edit form
│   │   ├── FilterBar.tsx         # Status/category filters
│   │   ├── SearchBar.tsx         # Search input
│   │   ├── StatCard.tsx          # Dashboard statistics card
│   │   └── DeleteConfirmDialog.tsx  # Confirmation dialog
│   ├── lib/
│   │   ├── api.ts                # API client functions
│   │   ├── constants.ts          # Frontend constants
│   │   ├── validation.ts         # Client-side validation
│   │   └── utils.ts              # cn() helper for className
│   ├── types/
│   │   └── todo.ts               # TypeScript interfaces
│   ├── tests/
│   │   └── components/           # Jest + RTL component tests
│   ├── package.json              # Frontend dependencies
│   ├── next.config.js            # Next.js configuration
│   ├── tailwind.config.ts        # Tailwind configuration
│   └── README.md                 # Frontend setup instructions
│
├── scripts/
│   └── migrate_from_phase_i.py   # Data migration script
│
├── Dockerfile.backend            # Backend container
├── Dockerfile.frontend           # Frontend container
├── docker-compose.yml            # Local development setup
└── README.md                     # Project overview
```

**Structure Decision**: Web application structure (Option 2 from template) with separate backend/ and frontend/ directories. This provides clear separation of concerns, independent deployment, and follows industry best practices for full-stack applications.

## Complexity Tracking

> **No constitutional violations** - all gates passed without exceptions.

## Skills & Agents Architecture (Phase II)

This section documents the development framework used during implementation. Skills and agents are **development-time tools** that assist in creating the application—they are not runtime features.

### Required Skills

The following skills provide reusable development capabilities for Phase II:

1. **nextjs-skill**
   - **Purpose**: Next.js 14+ App Router scaffolding, page templates, routing patterns
   - **Provides**: Component templates, layout structures, server/client component patterns
   - **Used for**: Frontend application structure, routing, SSR/CSR decisions

2. **tailwind-css-skill**
   - **Purpose**: Tailwind CSS 3+ configuration, responsive design patterns, utility conventions
   - **Provides**: Responsive breakpoint strategies, utility class patterns, design token setup
   - **Used for**: UI styling, responsive layouts, design consistency

3. **shadcn-skill**
   - **Purpose**: shadcn/ui component integration, accessible UI patterns
   - **Provides**: Pre-built accessible components, Radix UI integration patterns
   - **Used for**: Reusable UI components (buttons, forms, dialogs, toasts)

4. **fastapi-skill**
   - **Purpose**: FastAPI application structure, endpoint templates, Pydantic schemas
   - **Provides**: REST API patterns, validation schemas, dependency injection patterns
   - **Used for**: Backend API structure, endpoint implementation, request/response handling

5. **neon-postgres-skill**
   - **Purpose**: Neon DB setup, schema templates, connection configuration, migration patterns
   - **Provides**: Database schema templates, SQLModel patterns, Alembic migration templates
   - **Used for**: Database schema design, migrations, connection pooling

**Standard Skill Structure**:
```
.claude/skills/<skill-name>/
  ├── SKILL.md           # Skill metadata and capabilities
  ├── reference.md       # Technical reference documentation
  ├── examples.md        # Usage examples and walkthroughs
  ├── scripts/           # Automation scripts
  └── template/          # Code templates and boilerplates
```

### Agent Responsibilities

The following agents guide Phase II implementation:

1. **Frontend Expert Agent**
   - **Uses Skills**: tailwind-css-skill, shadcn-skill, nextjs-skill
   - **Responsibilities**:
     - UI component development and layout design
     - Responsive design implementation
     - Client-side state management
     - Accessibility compliance (WCAG AA)
   - **Outputs**: React components, Next.js pages, styling solutions

2. **Backend Expert Agent**
   - **Uses Skills**: fastapi-skill
   - **Responsibilities**:
     - REST API endpoint implementation
     - Request/response validation with Pydantic
     - Business logic layer design
     - Error handling and logging
   - **Outputs**: FastAPI routes, Pydantic schemas, service layer code

3. **Database Expert Agent**
   - **Uses Skills**: neon-postgres-skill
   - **Responsibilities**:
     - Database schema design and normalization
     - Migration script creation and execution
     - Query optimization and indexing
     - Connection pooling configuration
   - **Outputs**: SQLModel models, Alembic migrations, schema definitions

4. **UI/UX Expert Agent**
   - **Uses Skills**: tailwind-css-skill, shadcn-skill
   - **Responsibilities**:
     - User experience design and usability
     - Visual hierarchy and design consistency
     - Accessibility and WCAG compliance
     - Responsive design patterns
   - **Outputs**: Design decisions, accessibility guidelines, UX patterns

5. **Full-Stack Architecture Expert Agent**
   - **Coordinates All Skills**
   - **Responsibilities**:
     - System architecture and integration design
     - Cross-layer consistency (frontend ↔ backend ↔ database)
     - Phase I → Phase II logic preservation
     - Constitutional compliance and phase discipline
   - **Outputs**: Architectural decisions, integration patterns, ADRs when needed

### Use of Skills and Agents in Phase II

**Development Workflow**:
1. Full-Stack Architecture Expert designs overall system structure
2. Database Expert creates schema using neon-postgres-skill templates
3. Backend Expert implements API using fastapi-skill patterns
4. Frontend Expert builds UI using nextjs-skill, tailwind-css-skill, shadcn-skill
5. UI/UX Expert reviews for accessibility and usability
6. Full-Stack Architecture Expert validates integration and consistency

**Benefits**:
- **Consistency**: Standardized patterns across frontend, backend, and database layers
- **Maintainability**: Well-documented, reusable components reduce technical debt
- **Scalability**: Modular architecture supports future phases (III, IV, V) without rewrites

**Clarification**:
- Skills and agents are **development-time tools**, not runtime features
- The deployed Phase II application consists of Next.js frontend, FastAPI backend, and Neon PostgreSQL database
- Skills and agents do not add dependencies, increase bundle size, or affect application performance

## Phase 0: Research

**Status**: ✅ NOT NEEDED - This is an evolution of Phase I with well-defined requirements.

All necessary context is available:
- Phase I implementation exists and provides business logic reference
- Technology stack is defined in `Hackathon-II-Todo-App.md`
- Component mapping from Phase I to Phase II is documented in spec.md
- No technical unknowns requiring investigation

**Skip to Phase 1**.

## Phase 1: Design

### Data Model

**Entity: Todo**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier |
| title | String(500) | NOT NULL, min_length=1 | Todo title/description |
| status | Enum | 'pending' or 'completed', default='pending' | Current status |
| category | String(50) | Nullable | Optional category (Work, Personal, Shopping, etc.) |
| due_date | Date | Nullable | Optional due date (YYYY-MM-DD format) |
| created_at | Timestamp | Default=now(), NOT NULL | Creation timestamp |
| updated_at | Timestamp | Default=now(), OnUpdate=now() | Last update timestamp |
| version | Integer | Default=1 | Optimistic locking version |

**Indexes**:
- Primary: `id`
- Single: `status`, `category`, `created_at`
- Composite: `(status, due_date)` for filtered queries

**Relationships**: None (single-table design for Phase II)

**Migration Strategy**:
- Phase I → Phase II: Preserve `id`, `title`, `status`, `created_at`
- New fields: `category`, `due_date`, `updated_at`, `version` default to NULL or default values

### API Contracts

**Base URL**: `http://localhost:8000/api`

#### 1. List Todos
```http
GET /api/todos
Query Parameters:
  - status: string (optional) - Filter by 'pending' or 'completed'
  - category: string (optional) - Filter by category name
  - search: string (optional) - Case-insensitive title search
  - limit: integer (optional, default=20) - Pagination limit
  - offset: integer (optional, default=0) - Pagination offset

Response 200 OK:
{
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "status": "pending",
      "category": "Shopping",
      "due_date": "2025-12-20",
      "created_at": "2025-12-31T10:00:00Z",
      "updated_at": "2025-12-31T10:00:00Z",
      "version": 1
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### 2. Create Todo
```http
POST /api/todos
Content-Type: application/json

Request Body:
{
  "title": "Buy groceries",
  "category": "Shopping",  // optional
  "due_date": "2025-12-20"  // optional
}

Response 201 Created:
{
  "id": 1,
  "title": "Buy groceries",
  "status": "pending",
  "category": "Shopping",
  "due_date": "2025-12-20",
  "created_at": "2025-12-31T10:00:00Z",
  "updated_at": "2025-12-31T10:00:00Z",
  "version": 1
}

Response 400 Bad Request:
{
  "status_code": 400,
  "message": "Validation error",
  "detail": [{"field": "title", "error": "Title is required"}],
  "request_id": "uuid-here"
}
```

#### 3. Get Single Todo
```http
GET /api/todos/{id}

Response 200 OK:
{ /* Todo object */ }

Response 404 Not Found:
{
  "status_code": 404,
  "message": "Todo not found",
  "detail": "Todo with ID 123 does not exist",
  "request_id": "uuid-here"
}
```

#### 4. Update Todo
```http
PUT /api/todos/{id}
Content-Type: application/json

Request Body:
{
  "title": "Buy milk and eggs",
  "category": "Shopping",
  "due_date": "2025-12-20",
  "version": 1  // for optimistic locking
}

Response 200 OK:
{ /* Updated todo object with version incremented */ }

Response 409 Conflict:
{
  "status_code": 409,
  "message": "Conflict: Todo was modified by another process",
  "detail": "Expected version 1 but found version 2. Please refresh and retry.",
  "request_id": "uuid-here"
}
```

**Optimistic Locking Resolution Strategy**:
- On 409 Conflict, client MUST:
  1. Fetch latest version of todo (GET /api/todos/{id})
  2. Display conflict message to user with latest data
  3. Allow user to review changes and retry update
  4. Include updated version number in retry request

#### 5. Delete Todo
```http
DELETE /api/todos/{id}

Response 204 No Content
(no body)

Response 404 Not Found:
{ /* Error object */ }
```

#### 6. Toggle Complete
```http
PATCH /api/todos/{id}/complete

Response 200 OK:
{ /* Todo object with toggled status */ }
```

#### 7. Get Statistics
```http
GET /api/todos/stats

Response 200 OK:
{
  "total": 100,
  "pending": 45,
  "completed": 55,
  "overdue": 12  // pending todos with due_date < today
}
```

#### 8. Health Check
```http
GET /api/health

Response 200 OK:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-31T10:00:00Z"
}
```

**Error Response Format (All Endpoints)**:
```json
{
  "status_code": 400|404|409|500,
  "message": "Human-readable error message",
  "detail": "Detailed explanation or validation errors",
  "request_id": "uuid-v4-here"
}
```

### Frontend Page Structure

**Page: Homepage** (`/`)
- Components: TodoList, TodoItem, TodoForm, FilterBar, SearchBar, DeleteConfirmDialog
- State: todos (array), filters (status, category, search), loading, error
- API Calls: getTodos(), createTodo(), updateTodo(), deleteTodo(), toggleComplete()

**Page: Dashboard** (`/dashboard`)
- Components: StatCard (×4: total, pending, completed, overdue)
- State: stats (object)
- API Calls: getStats()

**Shared Layout** (`layout.tsx`)
- Navigation: Home, Dashboard
- Global toast notifications
- Metadata and fonts

## Implementation Approach

### Phase Breakdown

**Phase 1: Setup & Foundation** (T001-T011)
- Initialize project structure (backend/ and frontend/ directories)
- Set up dependencies and virtual environments
- Create configuration files (.env.example, .gitignore)
- Write initial README files

**Phase 2: Foundational Layer** (T012-T031)
- Database connection and session management
- Alembic initialization
- FastAPI app setup with CORS middleware
- Next.js initialization with Tailwind CSS and shadcn/ui
- Base TypeScript types and constants migration

**Phase 3: User Story 1 - Web-Based Todo Management** (T032-T073)
- Database: Create Todo model and migration
- Backend: Implement all 6 REST endpoints (GET, POST, PUT, DELETE, PATCH, GET/{id})
- Frontend: Build UI components (TodoList, TodoItem, TodoForm, DeleteConfirmDialog)
- Frontend: Implement CRUD flows with API integration
- Testing: Backend API tests, frontend component tests, manual E2E

**Phase 4: User Story 2 - RESTful API Backend** (T074-T083)
- Add pagination to GET /api/todos
- Enhance error responses with request_id
- Configure Swagger UI documentation
- Add API tests for pagination and error formats

**Phase 5: User Story 3 - Database Persistence** (T084-T095)
- Add category and due_date columns via migration
- Create indexes for performance
- Configure connection pooling (pool_size=5, max_overflow=10)
- Performance testing (1000 todos, <100ms query time)

**Phase 6: User Story 4 - Enhanced Features** (T096-T117)
- Backend: Add filtering (status, category, search) and stats endpoint
- Frontend: Add FilterBar, SearchBar, category/due_date inputs to TodoForm
- Frontend: Dashboard page with statistics
- Frontend: Overdue highlighting in TodoItem
- Testing: Filter/search/stats functionality

**Phase 7: User Story 5 - Data Migration** (T118-T130)
- Create migration script (migrate_from_phase_i.py)
- Implement read, validate, insert logic
- Add duplicate detection and error handling
- Test migration with Phase I data

**Phase 8: Polish & Cross-Cutting Concerns** (T131-T156)
- Responsive design testing (320px, 768px, 1920px)
- Accessibility (ARIA labels, keyboard navigation, screen reader)
- Performance optimization (React.memo, useMemo, useCallback)
- Error handling and logging
- Documentation updates
- Deployment preparation (Dockerfiles, docker-compose.yml)

### Critical Dependencies

1. **Database → Backend → Frontend** (sequential)
   - Database schema must exist before backend endpoints can be implemented
   - Backend API must be functional before frontend can integrate

2. **Foundation → Features** (blocking)
   - Phase 2 (Foundational Layer) blocks all user story implementations
   - Cannot implement US2-US5 until US1 is complete

3. **US1+US3 → US5** (prerequisite)
   - Data migration requires database schema (US3) and basic API (US1)

4. **All Features → Polish** (prerequisite)
   - Polish phase (Phase 8) runs after all 5 user stories complete

### Parallel Execution Opportunities

- **Setup tasks** (T010-T011): Backend README and Frontend README can be written in parallel
- **Within US1**: Testing tasks (T070-T073) can run in parallel after implementation
- **Within US2**: All tasks (T074-T083) can run in parallel after US1
- **Polish Phase**: Most tasks (T131-T156) can run in parallel

See `tasks.md` for detailed task dependency graph and [P] parallelization markers.

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database connection failures in production | High | Medium | Implement retry logic with exponential backoff; use pool_pre_ping=True for health checks |
| Phase I data migration errors | High | Low | Validate all data before insertion; provide dry-run mode; support rollback |
| Version conflict during concurrent updates | Medium | Low | Implement optimistic locking with clear user messaging; guide user to refresh and retry |
| Slow query performance with 10k+ todos | Medium | Medium | Create composite indexes on (status, due_date); implement pagination; limit query complexity |
| Browser compatibility issues (Safari, older browsers) | Medium | Low | Test on all target browsers; use Next.js for automatic polyfills; provide fallbacks |
| CORS issues between frontend and backend | Low | Medium | Configure CORS middleware early; test cross-origin requests in development |

## Success Metrics

- ✅ All 5 user stories pass independent test scenarios
- ✅ Web UI loads in <2 seconds on 4G network (50ms latency, 10Mbps)
- ✅ All Phase I CRUD operations work in web interface
- ✅ API handles 100 concurrent requests without errors
- ✅ Database SELECT queries with filters and pagination complete in <100ms for 10,000 todos
- ✅ Migration script successfully imports Phase I data with 100% integrity
- ✅ UI is responsive on mobile (320px), tablet (768px), and desktop (1920px)
- ✅ API documentation is complete and accurate at /docs
- ✅ All Phase I validation rules enforced (max 500 chars, non-empty, trimmed)
- ✅ Application deployed and accessible via public URL

## Architectural Decisions

### ADR Candidates (Require Documentation if Chosen)

1. **Next.js App Router vs Pages Router**
   - Decision: Use App Router (Next.js 14+)
   - Rationale: Modern routing, server components, better performance
   - Impact: Long-term maintainability, aligns with Next.js future

2. **SQLModel vs SQLAlchemy vs Raw SQL**
   - Decision: Use SQLModel
   - Rationale: Type safety, Pydantic integration, simpler than SQLAlchemy
   - Impact: Developer experience, type checking, FastAPI compatibility

3. **Optimistic Locking vs Database Transactions**
   - Decision: Use optimistic locking (version field)
   - Rationale: Better performance for low-conflict scenarios, simpler than pessimistic locking
   - Impact: Requires client-side retry logic on 409 Conflict

4. **Neon DB Connection Pooling Configuration**
   - Decision: pool_size=5, max_overflow=10, pool_pre_ping=True
   - Rationale: Balance between connection reuse and resource consumption
   - Impact: Performance under concurrent load, connection reliability

**Note**: Create ADRs for these decisions if they become contentious or require detailed tradeoff analysis during implementation.

## Timeline

**Total Estimated Effort**: 150 story points

- Phase 1 (Setup): 5 points
- Phase 2 (Foundation): 10 points
- Phase 3 (US1): 50 points (MVP core)
- Phase 4 (US2): 15 points
- Phase 5 (US3): 20 points
- Phase 6 (US4): 25 points
- Phase 7 (US5): 15 points
- Phase 8 (Polish): 10 points

**MVP Delivery** (Phases 1-3): 65 points
**Full Feature Set** (Phases 1-7): 140 points
**Production Ready** (All Phases): 150 points

**Ready for `/sp.implement` command** to begin task execution.

---

**Plan Version**: 1.0
**Last Updated**: 2025-12-31
**Author**: Claude Sonnet 4.5
**Status**: Complete - Ready for Implementation
