# FastAPISkill Reference Guide

Complete reference documentation for FastAPI backend development.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Core Components](#core-components)
3. [Database Models](#database-models)
4. [Pydantic Schemas](#pydantic-schemas)
5. [API Endpoints](#api-endpoints)
6. [Configuration](#configuration)
7. [CORS Setup](#cors-setup)
8. [Best Practices](#best-practices)

---

## Project Structure

Standard FastAPI project layout:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings with pydantic-settings
│   │   └── security.py         # Authentication utilities
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (DB sessions)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           └── todos.py    # Router modules
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py             # SQLModel models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── todo.py             # Pydantic schemas
│   └── db/
│       ├── __init__.py
│       ├── base.py             # Model imports for Alembic
│       └── session.py          # Database engine & sessions
├── alembic/                    # Database migrations
│   └── versions/
├── tests/
│   └── test_todos.py
├── .env.example
├── .env
├── requirements.txt
├── alembic.ini
└── README.md
```

---

## Core Components

### main.py

FastAPI application entry point:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import todos

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Todo API", "version": settings.version}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### config.py

Configuration with Pydantic Settings:

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Application
    app_name: str = Field(default="Todo API", env="APP_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    debug: bool = Field(default=False, env="DEBUG")

    # Database
    database_url: str = Field(env="DATABASE_URL")

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        env="CORS_ORIGINS"
    )

    # Authentication (optional)
    secret_key: str = Field(default="", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## Database Models

### SQLModel Todo Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Todo(SQLModel, table=True):
    """Todo database model."""
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=500)
    status: str = Field(default="pending")
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Database Session

```python
from sqlmodel import create_engine, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Session dependency
def get_session():
    with Session(engine) as session:
        yield session
```

---

## Pydantic Schemas

### Request/Response Schemas

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base schema
class TodoBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = None

# Create schema
class TodoCreate(TodoBase):
    pass

# Update schema
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = None
    status: Optional[str] = None

# Response schema
class TodoResponse(TodoBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# List response
class TodoListResponse(BaseModel):
    items: list[TodoResponse]
    total: int
    limit: int
    offset: int
```

---

## API Endpoints

### Complete CRUD Router

```python
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=TodoListResponse)
async def list_todos(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    """List todos with optional filtering."""
    query = select(Todo)

    if status:
        query = query.where(Todo.status == status)
    if category:
        query = query.where(Todo.category == category)
    if search:
        query = query.where(Todo.title.contains(search))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Get paginated results
    query = query.offset(skip).limit(limit)
    todos = session.exec(query).all()

    return TodoListResponse(
        items=todos,
        total=total,
        limit=limit,
        offset=skip,
    )

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
):
    """Create a new todo."""
    db_todo = Todo(**todo.model_dump())
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """Get a single todo by ID."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session),
):
    """Update a todo."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update fields
    for key, value in todo_update.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)

    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """Delete a todo."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return

@router.patch("/{todo_id}/complete", response_model=TodoResponse)
async def toggle_complete(
    todo_id: int,
    session: Session = Depends(get_session),
):
    """Toggle todo completion status."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.status = "completed" if todo.status == "pending" else "pending"
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
```

---

## Configuration

### requirements.txt

```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlmodel>=0.0.14
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0
```

### .env.example

```bash
# Application
APP_NAME=Todo API
VERSION=1.0.0
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Authentication (optional)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

---

## CORS Setup

### Basic CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Production CORS

```python
# In config.py
cors_origins: list[str] = Field(
    default=["https://yourdomain.com"],
    env="CORS_ORIGINS"
)

# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
```

---

## Best Practices

### 1. Use Dependencies

```python
from fastapi import Depends

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token
    return user

@router.get("/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
```

### 2. Error Handling

```python
from fastapi import HTTPException

try:
    result = await some_operation()
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error")
```

### 3. Response Models

Always use response models:
```python
@router.get("/", response_model=list[TodoResponse])
async def list_todos():
    return todos
```

### 4. Status Codes

Use appropriate HTTP status codes:
```python
from fastapi import status

@router.post("/", status_code=status.HTTP_201_CREATED)
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
```

---

## Alembic Migrations

### Initialize Alembic

```bash
alembic init alembic
```

### Create Migration

```bash
alembic revision --autogenerate -m "Create todos table"
```

### Apply Migration

```bash
alembic upgrade head
```

---

## Testing

### Test Example

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/api/todos/", json={
        "title": "Test Todo",
        "category": "Testing"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
```

---

**Skill**: FastAPISkill
**Version**: 1.0.0
**Updated**: 2025-12-31
