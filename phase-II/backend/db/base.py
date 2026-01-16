"""
Database base configuration for SQLModel.
"""
from sqlmodel import SQLModel

# Import all models here to ensure they are registered with SQLModel
# This allows Alembic to auto-detect model changes
# Models will be imported here after they are created

__all__ = ["SQLModel"]
