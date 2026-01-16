# Phase II Backend - FastAPI Todo API

RESTful API backend for the Todo application built with FastAPI, SQLModel, and PostgreSQL (Neon DB).

## Tech Stack

- **Framework**: FastAPI 0.100+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Database**: Neon DB (PostgreSQL 15+)
- **Migrations**: Alembic 1.12+
- **Testing**: pytest

## Setup Instructions

### 1. Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon DB recommended)

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 5. Initialize Database

Run Alembic migrations:

```bash
alembic upgrade head
```

### 6. Run Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 7. API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Todos

#### `GET /api/todos`
List all todos with pagination and filtering.

**Query Parameters:**
- `limit` (int, default: 20) - Number of todos to return
- `offset` (int, default: 0) - Number of todos to skip
- `status` (string, optional) - Filter by status: "pending" | "completed"
- `category` (string, optional) - Filter by category name
- `search` (string, optional) - Case-insensitive search in title

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "status": "pending",
      "category": "Personal",
      "due_date": "2025-12-31",
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z",
      "version": 1
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### `POST /api/todos`
Create a new todo.

**Request Body:**
```json
{
  "title": "Buy groceries",
  "category": "Personal",
  "due_date": "2025-12-31"
}
```

**Response:** `201 Created`

#### `GET /api/todos/{id}`
Get a single todo by ID.

**Response:** `200 OK` | `404 Not Found`

#### `PUT /api/todos/{id}`
Update a todo (with optimistic locking).

**Request Body:**
```json
{
  "title": "Buy organic groceries",
  "category": "Personal",
  "due_date": "2025-12-31",
  "version": 1
}
```

**Response:** `200 OK` | `404 Not Found` | `409 Conflict` (version mismatch)

#### `DELETE /api/todos/{id}`
Delete a todo.

**Response:** `204 No Content` | `404 Not Found`

#### `PATCH /api/todos/{id}/status`
Toggle todo completion status.

**Request Body:**
```json
{
  "status": "completed",
  "version": 1
}
```

**Response:** `200 OK` | `404 Not Found` | `409 Conflict`

#### `GET /api/todos/stats`
Get todo statistics.

**Response:** `200 OK`
```json
{
  "total": 10,
  "pending": 5,
  "completed": 4,
  "overdue": 1
}
```

### Health

#### `GET /health`
Health check endpoint.

**Response:** `200 OK`
```json
{
  "status": "healthy"
}
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## Project Structure

```
backend/
├── api/              # API routes
├── core/             # Configuration and constants
├── db/               # Database setup
├── models/           # SQLModel models
├── schemas/          # Pydantic schemas
├── migrations/       # Alembic migrations
├── tests/            # Test files
├── main.py           # FastAPI app entry point
└── requirements.txt  # Python dependencies
```

## Development

### Adding a New Endpoint

1. Create Pydantic schemas in `schemas/`
2. Define SQLModel model in `models/`
3. Create API route in `api/`
4. Register route in `main.py`
5. Write tests in `tests/`

### Creating a Migration

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `ENVIRONMENT`: development | staging | production
