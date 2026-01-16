# FastAPISkill Examples

Practical examples and walkthroughs for FastAPI backend development.

---

## Example 1: Complete Phase II Backend Setup

### Step-by-Step Walkthrough

```bash
# 1. Create project directory
mkdir -p phase-II/backend
cd phase-II/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Create project structure
mkdir -p app/{core,api/v1/endpoints,models,schemas,db}
mkdir -p tests alembic

# 4. Create __init__.py files
touch app/__init__.py
touch app/core/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/db/__init__.py

# 5. Install dependencies
pip install fastapi uvicorn sqlmodel pydantic-settings python-dotenv alembic psycopg2-binary

# 6. Create requirements.txt
pip freeze > requirements.txt

# 7. Copy templates from .claude/skills/fastapi-skill/template/

# 8. Configure environment
cat > .env << 'EOF'
APP_NAME=Todo API
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
CORS_ORIGINS=["http://localhost:3000"]
EOF

# 9. Run server
uvicorn app.main:app --reload
```

---

## Example 2: Creating Todo Model and Schema

### Database Model (SQLModel)

```python
# app/models/todo.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Todo(SQLModel, table=True):
    """Todo database model for Phase II."""
    __tablename__ = "todos"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required fields
    title: str = Field(max_length=500, description="Todo title")
    status: str = Field(default="pending", description="pending or completed")

    # Optional fields
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = Field(default=None, description="YYYY-MM-DD format")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Pydantic Schemas

```python
# app/schemas/todo.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    """Base todo schema."""
    title: str = Field(min_length=1, max_length=500)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = None

class TodoCreate(TodoBase):
    """Schema for creating a todo."""
    pass

class TodoUpdate(BaseModel):
    """Schema for updating a todo."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[str] = None
    status: Optional[str] = None

class TodoResponse(TodoBase):
    """Schema for todo response."""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## Example 3: Complete Todo Router

```python
# app/api/v1/endpoints/todos.py
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlmodel import Session, select, func
from typing import Optional
from datetime import datetime

from app.db.session import get_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/")
async def list_todos(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """
    List todos with optional filters and pagination.

    - **status**: pending or completed
    - **category**: Filter by category
    - **search**: Search in title
    - **limit**: Max items to return (1-1000)
    - **offset**: Number of items to skip
    """
    # Build query
    query = select(Todo)

    if status:
        query = query.where(Todo.status == status)
    if category:
        query = query.where(Todo.category == category)
    if search:
        query = query.where(Todo.title.contains(search))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Get paginated results
    todos = session.exec(query.offset(offset).limit(limit)).all()

    return {
        "items": todos,
        "total": total,
        "limit": limit,
        "offset": offset,
    }

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
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

    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
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

## Example 4: Database Setup with Alembic

### Initialize Database

```python
# app/db/session.py
from sqlmodel import create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

def get_session():
    """Dependency for database sessions."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create all tables."""
    from app.models.todo import Todo  # Import all models
    SQLModel.metadata.create_all(engine)
```

### Alembic Configuration

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini - set sqlalchemy.url
# Or use env.py to read from settings

# Create migration
alembic revision --autogenerate -m "Create todos table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Example 5: Testing the API

### Using FastAPI TestClient

```python
# tests/test_todos.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_todo():
    response = client.post("/api/todos/", json={
        "title": "Test Todo",
        "category": "Testing",
        "due_date": "2025-12-31"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["status"] == "pending"
    return data["id"]

def test_list_todos():
    response = client.get("/api/todos/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_get_todo():
    # Create a todo first
    create_response = client.post("/api/todos/", json={"title": "Get Test"})
    todo_id = create_response.json()["id"]

    # Get the todo
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Test"

def test_update_todo():
    # Create
    create_response = client.post("/api/todos/", json={"title": "Update Test"})
    todo_id = create_response.json()["id"]

    # Update
    response = client.put(f"/api/todos/{todo_id}", json={
        "title": "Updated Title",
        "status": "completed"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["status"] == "completed"

def test_delete_todo():
    # Create
    create_response = client.post("/api/todos/", json={"title": "Delete Test"})
    todo_id = create_response.json()["id"]

    # Delete
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404
```

---

## Example 6: Using Scripts

### Validate Setup

```bash
python .claude/skills/fastapi-skill/scripts/validate_setup.py phase-II/backend

# Output:
# Checking project structure... ✓
# Checking required files... ✓
# Checking dependencies... ✓
# Checking database config... ✓
```

### Create Project

```bash
python .claude/skills/fastapi-skill/scripts/create_project.py \
  --name todo_backend \
  --output ./phase-II/backend \
  --database postgresql

# Creates complete project structure
```

---

## Example 7: Running the Server

### Development

```bash
# With auto-reload
uvicorn app.main:app --reload --port 8000

# Access docs at:
# http://localhost:8000/docs
```

### Production

```bash
# With multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

**Skill**: FastAPISkill
**Version**: 1.0.0
**Updated**: 2025-12-31
