# Neon Postgres Skill - Technical Reference

Complete technical reference for scaffolding, configuring, and managing Neon Postgres databases.

---

## Table of Contents

1. [Overview](#overview)
2. [Neon Postgres Fundamentals](#neon-postgres-fundamentals)
3. [Account Setup](#account-setup)
4. [Connection Configuration](#connection-configuration)
5. [Schema Design](#schema-design)
6. [Query Patterns](#query-patterns)
7. [Connection Pooling](#connection-pooling)
8. [Migrations](#migrations)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

**Neon Postgres** is a serverless PostgreSQL database platform that separates storage and compute, providing:

- **Serverless Architecture**: Automatic scaling and pay-per-use pricing
- **Instant Provisioning**: Create databases in seconds
- **Database Branching**: Create isolated database copies for development
- **Built-in Pooling**: Connection pooling included by default
- **Auto-scaling**: Compute scales to zero when idle
- **High Availability**: Built-in replication and failover

**Key Benefits:**
- ✅ No server management required
- ✅ Generous free tier (0.5 GB storage, 191 compute hours/month)
- ✅ Full PostgreSQL compatibility (v15+)
- ✅ Instant scaling without downtime
- ✅ Built-in backups and point-in-time recovery

---

## Neon Postgres Fundamentals

### Architecture

```
┌─────────────────────────────────────────┐
│          Neon Platform                  │
├─────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Compute    │    │   Storage    │  │
│  │ (Serverless) │◄───┤  (Persistent)│  │
│  │  PostgreSQL  │    │    Layer     │  │
│  └──────────────┘    └──────────────┘  │
│         ▲                                │
│         │ Connection String             │
└─────────┼────────────────────────────────┘
          │
    ┌─────▼──────┐
    │ Your App   │
    │ (Next.js/  │
    │  FastAPI)  │
    └────────────┘
```

### Key Concepts

**Project**: Top-level container for databases and branches
**Branch**: Isolated copy of your database (like Git branches)
**Compute**: Serverless PostgreSQL instance
**Storage**: Durable, replicated storage layer
**Endpoint**: Connection endpoint (compute + branch combination)

---

## Account Setup

### Step 1: Create Neon Account

1. Go to https://neon.tech
2. Click "Sign Up" (free tier available)
3. Sign up with GitHub, Google, or email
4. Verify your email

### Step 2: Create a Project

1. Click "Create Project" in the dashboard
2. Configure:
   - **Project Name**: e.g., "todo-app-hackathon"
   - **Region**: Choose closest to your users
     - US East (Ohio) - `us-east-2`
     - US West (Oregon) - `us-west-2`
     - Europe (Frankfurt) - `eu-central-1`
     - Asia Pacific (Singapore) - `ap-southeast-1`
   - **PostgreSQL Version**: 15 or 16 (recommended)
   - **Compute Size**: Start with 0.25 vCPU (free tier)

3. Click "Create Project"

### Step 3: Get Connection String

After project creation, you'll see your connection string:

```
postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Connection String Format:**
```
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
```

**Components:**
- `user`: Database username (default: same as project name)
- `password`: Auto-generated password
- `host`: Neon compute endpoint
- `port`: 5432 (PostgreSQL default)
- `database`: Database name (default: `neondb`)
- `sslmode=require`: SSL/TLS encryption required

### Step 4: Copy Connection Details

Save these details securely:

```env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Alternative: Individual components
NEON_DB_HOST=ep-xxx-xxx.us-east-2.aws.neon.tech
NEON_DB_NAME=neondb
NEON_DB_USER=username
NEON_DB_PASSWORD=password
NEON_DB_PORT=5432
NEON_SSL_MODE=require
```

---

## Connection Configuration

### Environment Variables

Create `.env` file in your project root:

```env
# Neon Postgres Connection String (recommended)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Alternative: Pooled connection (for serverless environments)
DATABASE_URL_POOLED=postgresql://user:password@ep-xxx-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require

# Direct connection (for migrations and admin tasks)
DATABASE_URL_DIRECT=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Connection Types:**

1. **Pooled Connection** (recommended for apps):
   - Uses Neon's built-in connection pooler
   - Best for serverless functions and high concurrency
   - Endpoint: `ep-xxx-pooler.region.aws.neon.tech`

2. **Direct Connection** (for migrations):
   - Direct connection to PostgreSQL
   - Best for migrations and admin tasks
   - Endpoint: `ep-xxx.region.aws.neon.tech`

### Node.js / Next.js Configuration

#### Using `pg` (node-postgres)

```typescript
// lib/db.ts
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  },
  max: 10, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

export async function query(text: string, params?: any[]) {
  const start = Date.now()
  const client = await pool.connect()

  try {
    const result = await client.query(text, params)
    const duration = Date.now() - start
    console.log('Executed query', { text, duration, rows: result.rowCount })
    return result
  } finally {
    client.release()
  }
}

export default pool
```

#### Using Prisma

```typescript
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model Todo {
  id          Int      @id @default(autoincrement())
  title       String   @db.VarChar(255)
  description String?
  completed   Boolean  @default(false)
  priority    String?  @db.VarChar(20)
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  @@index([completed])
  @@index([priority])
  @@map("todos")
}
```

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query', 'error', 'warn'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

### Python / FastAPI Configuration

#### Using psycopg2

```python
# core/database.py
import psycopg2
from psycopg2.pool import SimpleConnectionPool
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Connection pool
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)

def get_connection():
    """Get connection from pool"""
    return pool.getconn()

def release_connection(conn):
    """Return connection to pool"""
    pool.putconn(conn)

def execute_query(query: str, params: tuple = None):
    """Execute query with automatic connection management"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)
```

#### Using SQLAlchemy

```python
# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

---

## Schema Design

### Example Schema: Todo Application

```sql
-- schema.sql

-- Enable UUID extension (optional)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Todos table
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed);
CREATE INDEX IF NOT EXISTS idx_todos_priority ON todos(priority);
CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_todos_due_date ON todos(due_date) WHERE due_date IS NOT NULL;

-- Composite index for common query pattern
CREATE INDEX IF NOT EXISTS idx_todos_completed_priority ON todos(completed, priority);

-- Trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_todos_updated_at BEFORE UPDATE ON todos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE todos IS 'User todo items';
COMMENT ON COLUMN todos.priority IS 'Priority level: low, medium, high';
COMMENT ON COLUMN todos.completed IS 'Whether the todo is completed';
```

### Best Practices for Schema Design

1. **Use Appropriate Data Types**
   ```sql
   -- Good
   email VARCHAR(255)
   age INTEGER
   price NUMERIC(10, 2)
   created_at TIMESTAMP WITH TIME ZONE

   -- Avoid
   email TEXT
   age VARCHAR(10)
   price FLOAT
   ```

2. **Add Constraints**
   ```sql
   -- NOT NULL for required fields
   title VARCHAR(255) NOT NULL

   -- CHECK constraints for validation
   priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high'))
   age INTEGER CHECK (age >= 0 AND age <= 150)

   -- UNIQUE constraints
   email VARCHAR(255) UNIQUE
   ```

3. **Create Indexes Strategically**
   ```sql
   -- Index columns used in WHERE clauses
   CREATE INDEX idx_users_email ON users(email);

   -- Index foreign keys
   CREATE INDEX idx_todos_user_id ON todos(user_id);

   -- Composite indexes for multiple columns
   CREATE INDEX idx_todos_user_completed ON todos(user_id, completed);

   -- Partial indexes for specific queries
   CREATE INDEX idx_active_todos ON todos(user_id) WHERE completed = FALSE;
   ```

4. **Use Timestamps**
   ```sql
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   ```

---

## Query Patterns

### CRUD Operations

#### Create (INSERT)

```sql
-- Insert single record
INSERT INTO todos (title, description, priority)
VALUES ($1, $2, $3)
RETURNING *;

-- Insert multiple records
INSERT INTO todos (title, completed, priority)
VALUES
    ('Task 1', false, 'high'),
    ('Task 2', false, 'medium'),
    ('Task 3', true, 'low')
RETURNING *;

-- Insert with conflict handling (upsert)
INSERT INTO todos (id, title, completed)
VALUES ($1, $2, $3)
ON CONFLICT (id) DO UPDATE
SET title = EXCLUDED.title, completed = EXCLUDED.completed
RETURNING *;
```

#### Read (SELECT)

```sql
-- Select all
SELECT * FROM todos ORDER BY created_at DESC;

-- Select with filtering
SELECT * FROM todos WHERE completed = false;

-- Select with multiple conditions
SELECT * FROM todos
WHERE completed = false
  AND priority = 'high'
ORDER BY created_at DESC;

-- Select with pagination
SELECT * FROM todos
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;

-- Select with search
SELECT * FROM todos
WHERE title ILIKE $1 OR description ILIKE $1
ORDER BY created_at DESC;

-- Select with aggregation
SELECT
    priority,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed_count
FROM todos
GROUP BY priority;
```

#### Update (UPDATE)

```sql
-- Update single field
UPDATE todos
SET completed = $1, updated_at = CURRENT_TIMESTAMP
WHERE id = $2
RETURNING *;

-- Update multiple fields
UPDATE todos
SET title = $1, description = $2, priority = $3, updated_at = CURRENT_TIMESTAMP
WHERE id = $4
RETURNING *;

-- Conditional update
UPDATE todos
SET completed = true
WHERE due_date < CURRENT_TIMESTAMP
RETURNING *;
```

#### Delete (DELETE)

```sql
-- Delete by ID
DELETE FROM todos WHERE id = $1 RETURNING *;

-- Delete with condition
DELETE FROM todos WHERE completed = true;

-- Delete all (use with caution!)
DELETE FROM todos;
```

### Advanced Queries

#### Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE todos ADD COLUMN search_vector tsvector;

-- Create index
CREATE INDEX idx_todos_search ON todos USING gin(search_vector);

-- Update search vector
UPDATE todos
SET search_vector = to_tsvector('english', title || ' ' || COALESCE(description, ''));

-- Search query
SELECT * FROM todos
WHERE search_vector @@ to_tsquery('english', $1)
ORDER BY created_at DESC;
```

#### JSON Columns

```sql
-- Add JSON column for metadata
ALTER TABLE todos ADD COLUMN metadata JSONB DEFAULT '{}';

-- Query JSON data
SELECT * FROM todos WHERE metadata->>'tags' ? 'important';

-- Update JSON data
UPDATE todos
SET metadata = metadata || '{"tags": ["urgent", "important"]}'::jsonb
WHERE id = $1;
```

---

## Connection Pooling

### Why Connection Pooling?

Connection pooling reuses database connections instead of creating new ones for each request, improving:
- ✅ Performance (reduced connection overhead)
- ✅ Scalability (limited concurrent connections)
- ✅ Resource efficiency (lower memory usage)

### Neon Built-in Pooling

Neon provides built-in connection pooling via **PgBouncer**:

```env
# Pooled connection (recommended for apps)
DATABASE_URL=postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/neondb?sslmode=require

# Direct connection (for migrations)
DATABASE_URL_DIRECT=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

**Pooling Modes:**
- **Session Mode**: Default, connection assigned for session duration
- **Transaction Mode**: Connection released after transaction (use for serverless)

### Client-Side Pooling

#### Node.js (pg)

```typescript
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})
```

#### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Number of connections to keep
    max_overflow=20,     # Extra connections when pool is full
    pool_pre_ping=True,  # Verify connection before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

---

## Migrations

### Using Alembic (Python/FastAPI)

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Configure alembic.ini
sqlalchemy.url = driver://user:pass@localhost/dbname
# Replace with:
sqlalchemy.url = postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require
```

```python
# alembic/env.py
from sqlalchemy import engine_from_config
from core.database import Base
import models  # Import all models

target_metadata = Base.metadata
```

```bash
# Create migration
alembic revision --autogenerate -m "Create todos table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Using Prisma (Node.js/Next.js)

```bash
# Install Prisma
npm install prisma --save-dev
npm install @prisma/client

# Initialize Prisma
npx prisma init

# Configure .env
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require

# Create migration
npx prisma migrate dev --name init

# Apply migration
npx prisma migrate deploy

# Generate Prisma Client
npx prisma generate
```

---

## Best Practices

### 1. Security

```env
# Use environment variables
DATABASE_URL=postgresql://...

# Never commit credentials
# Add to .gitignore:
.env
.env.local
```

### 2. Connection Management

```typescript
// Always release connections
const client = await pool.connect()
try {
  const result = await client.query('SELECT * FROM todos')
  return result
} finally {
  client.release() // Important!
}
```

### 3. Error Handling

```python
try:
    result = db.execute("SELECT * FROM todos")
except psycopg2.Error as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error")
```

### 4. Query Optimization

```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE SELECT * FROM todos WHERE completed = false;

-- Add indexes for frequently queried columns
CREATE INDEX idx_todos_completed ON todos(completed);
```

### 5. Backups

Neon provides automatic backups:
- Point-in-time recovery (7-day retention on free tier)
- Branch your database for safe testing

---

## Troubleshooting

### Connection Errors

**Error**: `ECONNREFUSED` or `connection timeout`

**Solutions**:
1. Verify connection string format
2. Check SSL mode: `?sslmode=require`
3. Verify firewall/network settings
4. Check Neon project is active (not suspended)

### SSL Errors

**Error**: `SSL connection required`

**Solution**:
```typescript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
})
```

### Pool Exhaustion

**Error**: `remaining connection slots reserved`

**Solutions**:
1. Increase pool size
2. Use connection pooling endpoint
3. Ensure connections are released
4. Check for connection leaks

### Migration Failures

**Error**: Migration fails to apply

**Solutions**:
1. Use direct connection (not pooled) for migrations
2. Check migration order and dependencies
3. Rollback and reapply migration
4. Verify schema syntax

---

## Resources

- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [node-postgres Documentation](https://node-postgres.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

**Last Updated**: 2025-12-31
**PostgreSQL Version**: 15+
**Neon Platform**: Serverless Postgres
