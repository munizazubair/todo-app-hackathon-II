"""
Todo data model and validation logic.

This module defines the Todo entity and provides validation functions
for todo attributes.
"""

from datetime import datetime
from typing import Tuple
from .constants import MAX_TITLE_LENGTH, STATUS_PENDING, STATUS_COMPLETED


class Todo:
    """
    Represents a single todo item.

    Attributes:
        id (int): Unique identifier for the todo
        title (str): Description of the task
        status (str): Current status (pending or completed)
        created (datetime): Timestamp when the todo was created
    """

    def __init__(self, id: int, title: str, status: str = STATUS_PENDING, created: datetime = None):
        """
        Initialize a new Todo instance.

        Args:
            id: Unique identifier
            title: Task description
            status: Initial status (default: pending)
            created: Creation timestamp (default: now)
        """
        self.id = id
        self.title = title
        self.status = status
        self.created = created or datetime.now()

    def __str__(self) -> str:
        """Return string representation of the todo."""
        status_symbol = "[X]" if self.status == STATUS_COMPLETED else "[ ]"
        return f"{self.id}. {status_symbol} {self.title}"

    def to_dict(self) -> dict:
        """
        Convert todo to dictionary for display formatting.

        Returns:
            Dictionary with todo attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created": self.created.isoformat()
        }


def validate_title(title: str) -> Tuple[bool, str]:
    """
    Validate a todo title.

    Checks:
    - Title is not empty
    - Title is not only whitespace
    - Title length does not exceed MAX_TITLE_LENGTH

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid, error_message)
        - If valid: (True, "")
        - If invalid: (False, "error description")
    """
    # Check for None
    if title is None:
        return False, "Title cannot be empty. Please provide a description."

    # Check for empty or whitespace-only
    if not title or not title.strip():
        return False, "Title cannot be empty. Please provide a description."

    # Check length
    if len(title) > MAX_TITLE_LENGTH:
        return False, f"Title too long (max {MAX_TITLE_LENGTH} characters). Current: {len(title)}"

    return True, ""
