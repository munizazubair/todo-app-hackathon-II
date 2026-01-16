---
name: neon-postgres-skill
description: Scaffolds and manages Neon Postgres database. Provides schema templates, example queries, and scripts to validate and generate data.
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# Neon Postgres Skill

Comprehensive skill for scaffolding, configuring, and managing Neon Postgres databases for Next.js and FastAPI applications.

## Overview

**Neon Postgres** is a serverless Postgres database platform that provides:
- Instant database provisioning
- Automatic scaling with serverless compute
- Branching for development workflows
- Built-in connection pooling
- Pay-per-use pricing with generous free tier

This skill helps you:
- ✅ Set up Neon Postgres database connections
- ✅ Generate production-ready database schemas
- ✅ Validate database connectivity and configuration
- ✅ Create example queries and migrations
- ✅ Integrate with Next.js and FastAPI backends

## When to Use This Skill

Use this skill when you need to:
1. Set up a new Neon Postgres database for your project
2. Generate database schemas and migrations
3. Validate database connection and configuration
4. Create example SQL queries for CRUD operations
5. Integrate Neon Postgres with Next.js or FastAPI

**Activation Triggers:**
- "Neon Postgres"
- "Neon database"
- "serverless Postgres"
- "database setup"
- "PostgreSQL connection"

## Core Capabilities

### 1. Database Setup and Configuration

Create and configure Neon Postgres databases with proper connection handling:

```bash
# Create database and apply schema
python .claude/skills/neon-postgres-skill/scripts/create_db.py

# Validate connection and check tables
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
```

### 2. Schema Generation

Generate production-ready database schemas:

```sql
-- Example: Todo application schema
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_completed ON todos(completed);
CREATE INDEX idx_todos_priority ON todos(priority);
```

### 3. Query Generation

Generate example CRUD queries:

```bash
# Generate SQL queries for your schema
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py
```

### 4. Connection Validation

Validate database connectivity and configuration:

```bash
# Check connection and verify tables exist
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
```

## Quick Start

### 1. Create Neon Account and Database

1. Go to https://neon.tech
2. Sign up for a free account
3. Create a new project
4. Copy your connection string

### 2. Configure Environment Variables

Create `.env` file in your project root:

```env
# Neon Postgres Connection String
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Alternative format
NEON_DB_HOST=ep-xxx.us-east-2.aws.neon.tech
NEON_DB_NAME=neondb
NEON_DB_USER=user
NEON_DB_PASSWORD=password
NEON_DB_PORT=5432
```

### 3. Apply Schema

```bash
# Create database and apply schema
python .claude/skills/neon-postgres-skill/scripts/create_db.py

# Or manually with psql
psql $DATABASE_URL < .claude/skills/neon-postgres-skill/template/schema.sql
```

### 4. Validate Setup

```bash
# Verify connection and tables
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
```

## Integration Examples

### Next.js Integration

```typescript
// lib/db.ts
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
})

export async function query(text: string, params?: any[]) {
  const client = await pool.connect()
  try {
    const result = await client.query(text, params)
    return result
  } finally {
    client.release()
  }
}

// app/api/todos/route.ts
import { query } from '@/lib/db'

export async function GET() {
  const result = await query('SELECT * FROM todos ORDER BY created_at DESC')
  return Response.json(result.rows)
}
```

### FastAPI Integration

```python
# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models/todo.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

## Available Scripts

### create_db.py

Creates database schema from template:

```bash
python .claude/skills/neon-postgres-skill/scripts/create_db.py
```

Options:
- Reads `DATABASE_URL` from environment
- Applies schema from `template/schema.sql`
- Creates tables and indexes
- Reports success/failure

### validate_connection.py

Validates database connection and configuration:

```bash
python .claude/skills/neon-postgres-skill/scripts/validate_connection.py
```

Checks:
- ✅ Connection string validity
- ✅ Database connectivity
- ✅ Required tables exist
- ✅ Indexes are created
- ✅ Permissions are correct

### generate_queries.py

Generates example SQL queries:

```bash
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py

# Output to file
python .claude/skills/neon-postgres-skill/scripts/generate_queries.py --output queries.sql
```

Generates:
- INSERT queries with example data
- SELECT queries with filters and pagination
- UPDATE queries for common operations
- DELETE queries with conditions

## Template Files

### schema.sql

Production-ready database schema template:

```sql
-- Tables, indexes, constraints, triggers
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_completed ON todos(completed);
```

### queries.sql

Example CRUD queries:

```sql
-- Insert
INSERT INTO todos (title, description) VALUES ($1, $2) RETURNING *;

-- Select all
SELECT * FROM todos ORDER BY created_at DESC;

-- Update
UPDATE todos SET completed = $1 WHERE id = $2 RETURNING *;

-- Delete
DELETE FROM todos WHERE id = $1;
```

### env.example

Environment variable template:

```env
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

### utils.py

Helper functions for database operations:

```python
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

## Best Practices

### 1. Connection Pooling

Use connection pooling for production:

```python
# Use pg.Pool for Node.js
const pool = new Pool({ connectionString: DATABASE_URL })

# Use SQLAlchemy pooling for Python
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
```

### 2. SSL/TLS

Always use SSL for Neon connections:

```env
DATABASE_URL=postgresql://...?sslmode=require
```

### 3. Environment Variables

Never commit credentials:

```bash
# .gitignore
.env
.env.local
```

### 4. Connection String Security

Store connection strings securely:

```typescript
// Use environment variables
const connectionString = process.env.DATABASE_URL

// Never hardcode
// const connectionString = "postgresql://user:pass@host/db" ❌
```

### 5. Migrations

Use migration tools for schema changes:

```bash
# Alembic (Python)
alembic revision --autogenerate -m "Add todos table"
alembic upgrade head

# Prisma (Node.js)
npx prisma migrate dev --name add_todos_table
```

## CLI-Style Invocation

You can invoke this skill using natural language:

```
"Set up Neon Postgres for the todo app"
"Apply Neon database schema"
"Validate Neon connection"
"Generate SQL queries for todos"
```

## Technology Stack

- **Database**: Neon Postgres (Serverless PostgreSQL)
- **Python**: psycopg2, SQLAlchemy
- **Node.js**: pg, Prisma
- **SQL**: PostgreSQL 15+
- **SSL/TLS**: Required for all connections

## Next Steps

After setting up Neon Postgres:

1. ✅ Create database and apply schema
2. ✅ Validate connection
3. ✅ Integrate with FastAPI or Next.js
4. ✅ Set up migrations (Alembic/Prisma)
5. ✅ Configure connection pooling
6. ✅ Add database backups

## Resources

- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [node-postgres Documentation](https://node-postgres.com/)

---

**Skill Version**: 1.0.0
**Created**: 2025-12-31
**Project**: Hackathon II Todo Application
**Branch**: 002-phase-ii-web-app
