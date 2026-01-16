"""User SQLModel definition for authentication."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .todo import Todo


class UserBase(SQLModel):
    """Base User model with shared fields."""
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address"
    )


class User(UserBase, table=True):
    """
    User database model.

    Represents an authenticated user in the system.
    """
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique user identifier (UUID)"
    )
    hashed_password: str = Field(
        max_length=255,
        description="Bcrypt hashed password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    # Relationship to todos
    todos: list["Todo"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    """Schema for user registration."""
    email: str = Field(
        max_length=255,
        description="User email address"
    )
    password: str = Field(
        min_length=8,
        description="Password (minimum 8 characters)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str = Field(description="User email address")
    password: str = Field(description="User password")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }


class UserResponse(SQLModel):
    """Schema for user response (excludes sensitive fields)."""
    id: UUID
    email: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class AuthResponse(SQLModel):
    """Schema for authentication response."""
    message: str
    user: UserResponse


class TokenData(SQLModel):
    """Schema for JWT token payload data."""
    user_id: UUID
    email: str
