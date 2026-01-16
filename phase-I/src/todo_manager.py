"""
Business logic for todo management.

This module provides the core CRUD operations for todos,
coordinating between the data model and storage layer.
"""

from typing import List, Tuple
from .models import Todo, validate_title
from .storage import TodoStorage
from .constants import STATUS_PENDING, STATUS_COMPLETED


class TodoManager:
    """
    Manages todo operations and business logic.

    Coordinates between the storage layer and validates all operations.
    """

    def __init__(self, storage: TodoStorage):
        """
        Initialize the TodoManager with a storage instance.

        Args:
            storage: TodoStorage instance for data persistence
        """
        self.storage = storage

    def add_todo(self, title: str) -> Tuple[bool, str, int]:
        """
        Create a new todo with the given title.

        Args:
            title: The todo description

        Returns:
            Tuple of (success, message, todo_id)
            - success: True if created, False if validation failed
            - message: Success or error message
            - todo_id: ID of created todo (or 0 if failed)
        """
        # Validate title
        is_valid, error_msg = validate_title(title)
        if not is_valid:
            return False, error_msg, 0

        # Create todo
        todo_id = self.storage.get_next_id()
        todo = Todo(id=todo_id, title=title.strip(), status=STATUS_PENDING)
        self.storage.add(todo)

        return True, f'Todo created with ID {todo_id}: "{todo.title}" (pending)', todo_id

    def list_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List of all Todo instances
        """
        return self.storage.get_all()

    def complete_todo(self, id: int) -> Tuple[bool, str]:
        """
        Mark a todo as completed.

        Args:
            id: The todo ID to complete

        Returns:
            Tuple of (success, message)
        """
        # Check if todo exists
        todo = self.storage.get(id)
        if not todo:
            return False, f"Todo not found. Use 'list' to see valid IDs."

        # Update status
        todo.status = STATUS_COMPLETED
        return True, f"Todo {id} marked as completed"

    def edit_todo(self, id: int, new_title: str) -> Tuple[bool, str]:
        """
        Update the title of an existing todo.

        Args:
            id: The todo ID to edit
            new_title: The new title

        Returns:
            Tuple of (success, message)
        """
        # Check if todo exists
        todo = self.storage.get(id)
        if not todo:
            return False, f"Todo not found. Use 'list' to see valid IDs."

        # Validate new title
        is_valid, error_msg = validate_title(new_title)
        if not is_valid:
            return False, error_msg

        # Update title
        todo.title = new_title.strip()
        return True, f"Todo {id} updated"

    def delete_todo(self, id: int) -> Tuple[bool, str]:
        """
        Delete a todo.

        Args:
            id: The todo ID to delete

        Returns:
            Tuple of (success, message)
        """
        # Check if todo exists
        if not self.storage.exists(id):
            return False, f"Todo not found. Use 'list' to see valid IDs."

        # Delete todo
        self.storage.delete(id)
        return True, f"Todo {id} deleted"
