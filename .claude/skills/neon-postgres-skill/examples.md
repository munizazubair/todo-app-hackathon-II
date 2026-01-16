# Neon Postgres Skill - Examples

Practical walkthroughs and usage examples for scaffolding and managing Neon Postgres databases.

---

## Table of Contents

1. [Complete Setup Walkthrough](#complete-setup-walkthrough)
2. [Next.js Integration Example](#nextjs-integration-example)
3. [FastAPI Integration Example](#fastapi-integration-example)
4. [Common Query Examples](#common-query-examples)
5. [Migration Examples](#migration-examples)
6. [Advanced Use Cases](#advanced-use-cases)

---

## Complete Setup Walkthrough

### Step 1: Create Neon Account and Database

1. **Sign up for Neon**:
   - Go to https://neon.tech
   - Click "Sign Up" and create account
   - Verify email

2. **Create Project**:
   ```
   Project Name: todo-app-hackathon
   Region: US East (Ohio)
   PostgreSQL Version: 15
   Compute Size: 0.25 vCPU (free tier)
   ```

3. **Copy Connection String**:
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### Step 2: Configure Environment Variables

Create `.env` file in your project root:

```env
# Neon Postgres Connection
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Pooled connection (for serverless/Next.js)
DATABASE_URL_POOLED=postgresql://user:password@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require

# Direct connection (for migrations)
DATABASE_URL_DIRECT=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

Add to `.gitignore`:

```gitignore
.env
.env.local
.env.*.local
```

### Step 3: Copy Template Files

```bash
# Copy schema template
cp .claude/skills/neon-postgres-skill/template/schema.sql ./database/schema.sql

# Copy env example
cp .claude/skills/neon-postgres-skill/template/env.example ./.env.example

# Copy utility functions
cp .claude/skills/neon-postgres-skill/template/utils.py ./lib/db_utils.py
```

### Step 4: Apply Schema

```bash
# Using the create_db.py script
python .claude/skills/neon-postgres-skill/scripts/create_db.py

# Or manually with psql
psql $DATABASE_URL < database/schema.sql
```

Expected output:

```
🔧 Creating Neon Postgres database schema...

✅ Connected to Neon Postgres successfully
✅ Created table: todos
✅ Created index: idx_todos_completed
✅ Created index: idx_todos_priority
✅ Created trigger: update_todos_updated_at

🎉 Database schema created successfully!

Connection details:
  Host: ep-xxx.us-east-2.aws.neon.tech
  Database: neondb
  Tables: todos
```

### Step 5: Validate Setup

```bash
# Run validation script
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
```

Expected output:

```
🔍 Validating Neon Postgres connection...

✅ Connection string found
✅ Connected to database successfully
✅ Table 'todos' exists
✅ Index 'idx_todos_completed' exists
✅ Index 'idx_todos_priority' exists
✅ Trigger 'update_todos_updated_at' exists

🎉 All validation checks passed!

Database info:
  PostgreSQL version: 15.3
  Total tables: 1
  Total indexes: 2
```

### Step 6: Generate Example Queries

```bash
# Generate SQL queries
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py --output database/queries.sql
```

Expected output:

```
📝 Generating SQL queries...

✅ Generated INSERT queries (5 examples)
✅ Generated SELECT queries (8 examples)
✅ Generated UPDATE queries (4 examples)
✅ Generated DELETE queries (3 examples)

📄 Queries written to: database/queries.sql
```

---

## Next.js Integration Example

### Project Structure

```
phase-II/frontend/
├── app/
│   ├── api/
│   │   └── todos/
│   │       ├── route.ts          # GET /api/todos, POST /api/todos
│   │       └── [id]/
│   │           └── route.ts      # GET/PUT/DELETE /api/todos/:id
│   ├── components/
│   │   ├── TodoList.tsx
│   │   └── TodoForm.tsx
│   └── page.tsx
├── lib/
│   └── db.ts                     # Database client
├── .env.local
└── package.json
```

### Install Dependencies

```bash
cd phase-II/frontend

# Install pg (node-postgres)
npm install pg
npm install --save-dev @types/pg
```

### Database Client Setup

```typescript
// lib/db.ts
import { Pool, QueryResult } from 'pg'

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL environment variable is not set')
}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  },
  max: 10, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

// Test connection on startup
pool.on('connect', () => {
  console.log('✅ Connected to Neon Postgres')
})

pool.on('error', (err) => {
  console.error('❌ Unexpected error on idle client', err)
  process.exit(-1)
})

export async function query<T = any>(
  text: string,
  params?: any[]
): Promise<QueryResult<T>> {
  const start = Date.now()
  const client = await pool.connect()

  try {
    const result = await client.query<T>(text, params)
    const duration = Date.now() - start

    if (process.env.NODE_ENV === 'development') {
      console.log('Executed query', {
        text: text.substring(0, 100),
        duration,
        rows: result.rowCount
      })
    }

    return result
  } catch (error) {
    console.error('Database query error:', error)
    throw error
  } finally {
    client.release()
  }
}

export default pool
```

### API Routes

```typescript
// app/api/todos/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { query } from '@/lib/db'

export interface Todo {
  id: number
  title: string
  description: string | null
  completed: boolean
  priority: 'low' | 'medium' | 'high' | null
  created_at: Date
  updated_at: Date
}

// GET /api/todos
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const completed = searchParams.get('completed')
    const priority = searchParams.get('priority')
    const search = searchParams.get('search')
    const limit = parseInt(searchParams.get('limit') || '50')
    const offset = parseInt(searchParams.get('offset') || '0')

    let sql = 'SELECT * FROM todos WHERE 1=1'
    const params: any[] = []
    let paramIndex = 1

    if (completed !== null) {
      sql += ` AND completed = $${paramIndex++}`
      params.push(completed === 'true')
    }

    if (priority) {
      sql += ` AND priority = $${paramIndex++}`
      params.push(priority)
    }

    if (search) {
      sql += ` AND (title ILIKE $${paramIndex++} OR description ILIKE $${paramIndex++})`
      params.push(`%${search}%`, `%${search}%`)
    }

    sql += ` ORDER BY created_at DESC LIMIT $${paramIndex++} OFFSET $${paramIndex++}`
    params.push(limit, offset)

    const result = await query<Todo>(sql, params)

    return NextResponse.json({
      success: true,
      data: result.rows,
      count: result.rowCount
    })
  } catch (error) {
    console.error('GET /api/todos error:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch todos' },
      { status: 500 }
    )
  }
}

// POST /api/todos
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { title, description, priority } = body

    if (!title || title.trim().length === 0) {
      return NextResponse.json(
        { success: false, error: 'Title is required' },
        { status: 400 }
      )
    }

    const result = await query<Todo>(
      `INSERT INTO todos (title, description, priority)
       VALUES ($1, $2, $3)
       RETURNING *`,
      [title, description || null, priority || null]
    )

    return NextResponse.json({
      success: true,
      data: result.rows[0]
    }, { status: 201 })
  } catch (error) {
    console.error('POST /api/todos error:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to create todo' },
      { status: 500 }
    )
  }
}
```

```typescript
// app/api/todos/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { query } from '@/lib/db'
import { Todo } from '../route'

// GET /api/todos/:id
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const result = await query<Todo>(
      'SELECT * FROM todos WHERE id = $1',
      [params.id]
    )

    if (result.rowCount === 0) {
      return NextResponse.json(
        { success: false, error: 'Todo not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: result.rows[0]
    })
  } catch (error) {
    console.error('GET /api/todos/:id error:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch todo' },
      { status: 500 }
    )
  }
}

// PUT /api/todos/:id
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json()
    const { title, description, completed, priority } = body

    const result = await query<Todo>(
      `UPDATE todos
       SET title = COALESCE($1, title),
           description = COALESCE($2, description),
           completed = COALESCE($3, completed),
           priority = COALESCE($4, priority),
           updated_at = CURRENT_TIMESTAMP
       WHERE id = $5
       RETURNING *`,
      [title, description, completed, priority, params.id]
    )

    if (result.rowCount === 0) {
      return NextResponse.json(
        { success: false, error: 'Todo not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: result.rows[0]
    })
  } catch (error) {
    console.error('PUT /api/todos/:id error:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to update todo' },
      { status: 500 }
    )
  }
}

// DELETE /api/todos/:id
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const result = await query<Todo>(
      'DELETE FROM todos WHERE id = $1 RETURNING *',
      [params.id]
    )

    if (result.rowCount === 0) {
      return NextResponse.json(
        { success: false, error: 'Todo not found' },
        { status: 404 }
      )
    }

    return NextResponse.json({
      success: true,
      data: result.rows[0]
    })
  } catch (error) {
    console.error('DELETE /api/todos/:id error:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to delete todo' },
      { status: 500 }
    )
  }
}
```

### Environment Configuration

```env
# .env.local
DATABASE_URL=postgresql://user:password@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
```

---

## FastAPI Integration Example

### Project Structure

```
phase-II/backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── database.py           # Database connection
│   ├── models/
│   │   └── todo.py               # SQLAlchemy models
│   ├── schemas/
│   │   └── todo.py               # Pydantic schemas
│   └── routers/
│       └── todos.py              # Todo endpoints
├── .env
└── requirements.txt
```

### Install Dependencies

```bash
cd phase-II/backend

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### Database Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True  # Set to False in production
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Models

```python
# app/models/todo.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    priority = Column(String(20), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
```

### Schemas

```python
# app/schemas/todo.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")

class TodoResponse(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Router

```python
# app/routers/todos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all todos with optional filtering"""
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if priority:
        query = query.filter(Todo.priority == priority)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Todo.title.ilike(search_pattern)) |
            (Todo.description.ilike(search_pattern))
        )

    todos = query.order_by(Todo.created_at.desc()).limit(limit).offset(offset).all()
    return todos

@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return db_todo
```

### Main Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import todos
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="Todo application API with Neon Postgres",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Todo API with Neon Postgres"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Environment Configuration

```env
# .env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Run Application

```bash
# Run FastAPI server
uvicorn app.main:app --reload --port 8000
```

---

## Common Query Examples

### 1. Get All Todos

```sql
SELECT * FROM todos ORDER BY created_at DESC;
```

### 2. Get Active Todos

```sql
SELECT * FROM todos WHERE completed = false ORDER BY created_at DESC;
```

### 3. Get High Priority Todos

```sql
SELECT * FROM todos
WHERE completed = false AND priority = 'high'
ORDER BY created_at DESC;
```

### 4. Search Todos

```sql
SELECT * FROM todos
WHERE title ILIKE '%meeting%' OR description ILIKE '%meeting%'
ORDER BY created_at DESC;
```

### 5. Get Todos with Pagination

```sql
SELECT * FROM todos
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;
```

### 6. Get Todo Statistics

```sql
SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed,
    COUNT(*) FILTER (WHERE completed = false) as active,
    COUNT(*) FILTER (WHERE priority = 'high') as high_priority
FROM todos;
```

### 7. Get Todos Grouped by Priority

```sql
SELECT
    priority,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed,
    COUNT(*) FILTER (WHERE completed = false) as active
FROM todos
GROUP BY priority
ORDER BY
    CASE priority
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
        ELSE 4
    END;
```

---

## Migration Examples

### Using Alembic (Python)

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini
sqlalchemy.url = postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require

# Create migration
alembic revision --autogenerate -m "Add tags column to todos"

# Apply migration
alembic upgrade head
```

Example migration:

```python
# alembic/versions/xxx_add_tags_column.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('todos', sa.Column('tags', sa.JSON, nullable=True))
    op.create_index('idx_todos_tags', 'todos', ['tags'], postgresql_using='gin')

def downgrade():
    op.drop_index('idx_todos_tags')
    op.drop_column('todos', 'tags')
```

### Using Prisma (Node.js)

```bash
# Create migration
npx prisma migrate dev --name add_tags_column

# Apply migration
npx prisma migrate deploy
```

Example schema change:

```prisma
model Todo {
  id          Int      @id @default(autoincrement())
  title       String   @db.VarChar(255)
  description String?
  completed   Boolean  @default(false)
  priority    String?  @db.VarChar(20)
  tags        Json?    // New column
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  @@index([completed])
  @@index([priority])
  @@map("todos")
}
```

---

## Advanced Use Cases

### Full-Text Search

```sql
-- Add search vector column
ALTER TABLE todos ADD COLUMN search_vector tsvector;

-- Create GIN index
CREATE INDEX idx_todos_search ON todos USING gin(search_vector);

-- Update search vector
UPDATE todos
SET search_vector = to_tsvector('english', title || ' ' || COALESCE(description, ''));

-- Create trigger for automatic updates
CREATE OR REPLACE FUNCTION todos_search_trigger() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', NEW.title || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE ON todos
FOR EACH ROW EXECUTE FUNCTION todos_search_trigger();

-- Search query
SELECT * FROM todos
WHERE search_vector @@ to_tsquery('english', 'meeting & urgent')
ORDER BY ts_rank(search_vector, to_tsquery('english', 'meeting & urgent')) DESC;
```

### JSON Metadata

```sql
-- Add metadata column
ALTER TABLE todos ADD COLUMN metadata JSONB DEFAULT '{}';

-- Create GIN index
CREATE INDEX idx_todos_metadata ON todos USING gin(metadata);

-- Insert with metadata
INSERT INTO todos (title, metadata)
VALUES ('Important task', '{"tags": ["urgent", "important"], "estimate": 2}');

-- Query by JSON field
SELECT * FROM todos WHERE metadata->>'tags' ? 'urgent';

-- Update JSON field
UPDATE todos
SET metadata = metadata || '{"status": "in_progress"}'::jsonb
WHERE id = 1;
```

---

**Last Updated**: 2025-12-31
**PostgreSQL Version**: 15+
**Neon Platform**: Serverless Postgres
