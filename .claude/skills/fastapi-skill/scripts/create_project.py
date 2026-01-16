#!/usr/bin/env python3
"""
FastAPI Project Scaffolding Script

Creates a complete FastAPI project structure for Phase II backend.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional


def create_directory_structure(base_path: Path) -> None:
    """Create the standard FastAPI project directory structure."""
    directories = [
        "app",
        "app/core",
        "app/api",
        "app/api/v1",
        "app/api/v1/endpoints",
        "app/models",
        "app/schemas",
        "app/db",
        "tests",
        "alembic",
        "alembic/versions",
    ]

    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}/")

        # Create __init__.py files for Python packages
        if directory.startswith("app"):
            init_file = dir_path / "__init__.py"
            init_file.touch()


def create_main_file(base_path: Path, app_name: str) -> None:
    """Create the main FastAPI application file."""
    main_content = f'''"""
{app_name} - FastAPI Application

Main application entry point with CORS and router configuration.
"""

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

# CORS Configuration
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
    """Root endpoint."""
    return {{"message": "{app_name}", "version": settings.version}}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {{"status": "healthy"}}
'''

    main_file = base_path / "app" / "main.py"
    main_file.write_text(main_content)
    print(f"✓ Created app/main.py")


def create_config_file(base_path: Path, database_type: str) -> None:
    """Create the configuration file with pydantic-settings."""
    db_url_example = {
        "postgresql": "postgresql://user:password@localhost:5432/todo_db",
        "mysql": "mysql://user:password@localhost:3306/todo_db",
        "sqlite": "sqlite:///./todo.db",
    }.get(database_type, "sqlite:///./todo.db")

    config_content = f'''"""
Application Configuration

Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = Field(default="Todo API", env="APP_NAME")
    version: str = Field(default="1.0.0", env="VERSION")
    debug: bool = Field(default=False, env="DEBUG")

    # Database
    database_url: str = Field(
        default="{db_url_example}",
        env="DATABASE_URL"
    )

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
'''

    config_file = base_path / "app" / "core" / "config.py"
    config_file.write_text(config_content)
    print(f"✓ Created app/core/config.py")


def create_db_session_file(base_path: Path) -> None:
    """Create database session management file."""
    session_content = '''"""
Database Session Management

Creates SQLModel engine and provides session dependency.
"""

from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings


# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)


def get_session():
    """Database session dependency."""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)
'''

    session_file = base_path / "app" / "db" / "session.py"
    session_file.write_text(session_content)
    print(f"✓ Created app/db/session.py")


def create_requirements_file(base_path: Path) -> None:
    """Create requirements.txt with dependencies."""
    requirements = '''fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlmodel>=0.0.14
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0
pytest>=7.4.0
httpx>=0.24.0
'''

    req_file = base_path / "requirements.txt"
    req_file.write_text(requirements)
    print(f"✓ Created requirements.txt")


def create_env_example(base_path: Path, database_type: str) -> None:
    """Create .env.example file."""
    db_url_example = {
        "postgresql": "postgresql://user:password@localhost:5432/todo_db",
        "mysql": "mysql://user:password@localhost:3306/todo_db",
        "sqlite": "sqlite:///./todo.db",
    }.get(database_type, "sqlite:///./todo.db")

    env_content = f'''# Application
APP_NAME=Todo API
VERSION=1.0.0
DEBUG=False

# Database
DATABASE_URL={db_url_example}

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Authentication (optional)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
'''

    env_file = base_path / ".env.example"
    env_file.write_text(env_content)
    print(f"✓ Created .env.example")


def create_readme(base_path: Path, project_name: str) -> None:
    """Create README.md file."""
    readme_content = f'''# {project_name}

FastAPI backend for Phase II Hackathon Todo Application.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
{project_name}/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   └── config.py        # Settings
│   ├── api/
│   │   └── v1/endpoints/    # API routes
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   └── db/                  # Database config
├── tests/
├── alembic/                 # Database migrations
├── requirements.txt
└── .env.example
```

## Development

Generated with FastAPISkill for Claude Code.
'''

    readme_file = base_path / "README.md"
    readme_file.write_text(readme_content)
    print(f"✓ Created README.md")


def main():
    parser = argparse.ArgumentParser(
        description="Create a FastAPI project structure"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="todo_backend",
        help="Project name (default: todo_backend)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--database",
        type=str,
        choices=["postgresql", "mysql", "sqlite"],
        default="postgresql",
        help="Database type (default: postgresql)"
    )

    args = parser.parse_args()

    # Create base path
    base_path = Path(args.output).resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"\n🚀 Creating FastAPI project: {args.name}")
    print(f"📁 Output directory: {base_path}\n")

    # Create project structure
    create_directory_structure(base_path)
    create_main_file(base_path, args.name)
    create_config_file(base_path, args.database)
    create_db_session_file(base_path)
    create_requirements_file(base_path)
    create_env_example(base_path, args.database)
    create_readme(base_path, args.name)

    print(f"\n✅ Project created successfully!")
    print(f"\n📝 Next steps:")
    print(f"   1. cd {base_path}")
    print(f"   2. python -m venv venv")
    print(f"   3. source venv/bin/activate  # Windows: venv\\Scripts\\activate")
    print(f"   4. pip install -r requirements.txt")
    print(f"   5. cp .env.example .env")
    print(f"   6. uvicorn app.main:app --reload\n")


if __name__ == "__main__":
    main()
