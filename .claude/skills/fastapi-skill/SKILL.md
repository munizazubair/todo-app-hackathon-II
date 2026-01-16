---
name: fastapi-skill
description: Scaffolds and manages FastAPI 2+ backend applications. Generates project structure, creates routers and endpoints, configures databases, and applies production-grade patterns. Use when creating FastAPI backends, adding API routes, setting up database models, or configuring CORS for frontend integration.
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# FastAPISkill - Backend Development

Expert guidance for FastAPI 2+ backend development.

---

## Overview

FastAPISkill provides comprehensive support for building production-grade FastAPI backends with:

- **Project Scaffolding**: Complete FastAPI project structure
- **Router & Endpoint Generation**: CRUD operations and custom endpoints
- **Database Configuration**: SQLModel, SQLAlchemy, Tortoise ORM support
- **Model Generation**: Pydantic schemas and database models
- **CORS Setup**: Frontend integration with Next.js
- **Environment Management**: Secure configuration with .env files
- **Production Patterns**: Validation, error handling, API documentation

---

## Core Capabilities

### 1. Project Creation

Generate complete FastAPI project structure:

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   ├── config.py        # Settings
│   │   └── security.py      # Authentication
│   ├── api/
│   │   └── v1/endpoints/    # API routes
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   └── db/                  # Database config
├── tests/
├── .env.example
└── requirements.txt
```

### 2. Router Management

Create routers with CRUD operations:
- GET `/api/resource/` - List all
- POST `/api/resource/` - Create new
- GET `/api/resource/{id}` - Get single
- PUT `/api/resource/{id}` - Update
- DELETE `/api/resource/{id}` - Delete

### 3. Database Integration

Support for multiple ORMs and databases:
- **ORMs**: SQLModel, SQLAlchemy, Tortoise
- **Databases**: PostgreSQL, MySQL, SQLite
- **Migrations**: Alembic integration
- **Connection**: Pooling and session management

### 4. Model Generation

Automatic generation of:
- **SQLModel schemas**: Database models with type hints
- **Pydantic models**: Request/response validation
- **Timestamps**: created_at, updated_at
- **Relationships**: Foreign keys and joins

### 5. CORS Configuration

Seamless frontend integration:
- Configure allowed origins
- Set credentials policy
- Define allowed methods and headers
- Production-ready settings

---

## Quick Start

### Create Project

```python
# Use template files from template/ directory
# Or follow examples in examples.md
```

### Add Router

```python
# Create router file: app/api/v1/endpoints/todos.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/todos", tags=["todos"])

@router.get("/")
async def list_todos():
    return {"items": [], "total": 0}
```

### Configure Database

```python
# app/db/session.py
from sqlmodel import create_engine, Session

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

---

## Technology Stack

- **Framework**: FastAPI 0.100+
- **Python**: 3.11+
- **ORM**: SQLModel 0.0.14+ (or SQLAlchemy/Tortoise)
- **Validation**: Pydantic 2.0+
- **Server**: Uvicorn
- **Migrations**: Alembic
- **Testing**: Pytest

---

## Phase II Integration

This skill is specifically designed for Phase II backend:

### Todo API Requirements

```python
# Model: app/models/todo.py
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=500)
    status: str = Field(default="pending")
    category: Optional[str] = Field(max_length=50)
    due_date: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Router: app/api/v1/endpoints/todos.py

```python
@router.get("/", response_model=TodoListResponse)
async def list_todos(
    status: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    # Implementation
    pass

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    # Implementation
    pass
```

---

## Best Practices

### 1. Type Safety

Use Pydantic for validation:
```python
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    category: Optional[str] = Field(max_length=50)
```

### 2. Error Handling

Proper HTTP exceptions:
```python
from fastapi import HTTPException

if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
```

### 3. Dependencies

Use dependency injection:
```python
from fastapi import Depends

@router.get("/")
async def list_todos(db: Session = Depends(get_db)):
    pass
```

### 4. Documentation

Auto-generated OpenAPI docs at `/docs`

---

## Scripts

### create_project.py

Scaffolds a new FastAPI project:
```bash
python scripts/create_project.py --name todo_backend --output ./phase-II/backend
```

### validate_setup.py

Validates FastAPI project structure:
```bash
python scripts/validate_setup.py ./phase-II/backend
```

---

## Templates

Ready-to-use code templates in `template/`:
- `core.py` - Core FastAPI setup
- `utils.py` - Utility functions

See `examples.md` for complete implementations.

---

## When to Use

This skill activates when you:
- Create FastAPI backends
- Add API endpoints
- Configure databases
- Set up authentication
- Implement CORS
- Generate API documentation

---

**Version**: 1.0.0
**Format**: Claude Code Skill
**Framework**: FastAPI 2+
**Updated**: 2025-12-31
