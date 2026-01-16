"""Todo SQLModel definition with all required fields."""

from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Enum as SQLEnum, Relationship
from enum import Enum
from uuid import UUID

if TYPE_CHECKING:
    from .user import User


class TodoStatus(str, Enum):
    """Valid todo statuses."""
    PENDING = "pending"
    COMPLETED = "completed"


class TodoBase(SQLModel):
    """Base Todo model with shared fields."""
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Todo title/description"
    )
    category: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Optional category"
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date (YYYY-MM-DD format)"
    )


class Todo(TodoBase, table=True):
    """
    Todo database model.

    Represents a single todo item with all metadata.
    Includes optimistic locking via version field.
    """
    __tablename__ = "todos"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier"
    )
    user_id: Optional[UUID] = Field(
        default=None,
        foreign_key="users.id",
        index=True,
        description="Owner user ID"
    )
    status: TodoStatus = Field(
        default=TodoStatus.PENDING,
        sa_column=Column(SQLEnum(TodoStatus)),
        description="Current status (pending or completed)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    version: int = Field(
        default=1,
        description="Optimistic locking version"
    )

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "category": "Personal",
                    "due_date": "2026-01-15"
                },
                {
                    "title": "Finish hackathon project",
                    "category": "Work",
                    "due_date": "2026-01-10"
                }
            ]
        }
    }


class TodoUpdate(SQLModel):
    """
    Schema for updating an existing todo.

    All fields are optional except version (required for optimistic locking).
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500
    )
    category: Optional[str] = Field(
        default=None,
        max_length=50
    )
    due_date: Optional[date] = None
    version: int = Field(
        description="Current version for optimistic locking"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and cook dinner",
                    "category": "Personal",
                    "due_date": "2026-01-16",
                    "version": 1
                }
            ]
        }
    }


class TodoStatusUpdate(SQLModel):
    """Schema for updating only the status of a todo."""
    status: TodoStatus
    version: int = Field(
        description="Current version for optimistic locking"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "completed",
                    "version": 1
                }
            ]
        }
    }
