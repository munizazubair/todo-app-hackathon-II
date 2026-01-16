"""
In-memory storage for todos.

This module provides the storage layer for managing todos in memory.
All data is lost when the application terminates.
"""

from typing import Dict, List, Optional
from .models import Todo


class TodoStorage:
    """
    In-memory storage for Todo items.

    Uses a dictionary for O(1) lookup by ID and maintains a counter
    for sequential ID generation.
    """

    def __init__(self):
        """Initialize empty storage with ID counter starting at 1."""
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1

    def get_next_id(self) -> int:
        """
        Get the next available ID and increment the counter.

        Returns:
            The next sequential ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, todo: Todo) -> None:
        """
        Add a todo to storage.

        Args:
            todo: The Todo instance to store
        """
        self._todos[todo.id] = todo

    def get(self, id: int) -> Optional[Todo]:
        """
        Retrieve a todo by ID.

        Args:
            id: The todo ID to look up

        Returns:
            The Todo instance if found, None otherwise
        """
        return self._todos.get(id)

    def get_all(self) -> List[Todo]:
        """
        Retrieve all todos.

        Returns:
            List of all Todo instances, ordered by ID
        """
        return [self._todos[id] for id in sorted(self._todos.keys())]

    def delete(self, id: int) -> bool:
        """
        Remove a todo from storage.

        Args:
            id: The todo ID to delete

        Returns:
            True if todo was deleted, False if ID not found
        """
        if id in self._todos:
            del self._todos[id]
            return True
        return False

    def exists(self, id: int) -> bool:
        """
        Check if a todo with the given ID exists.

        Args:
            id: The todo ID to check

        Returns:
            True if todo exists, False otherwise
        """
        return id in self._todos

    def count(self) -> int:
        """
        Get the total number of todos in storage.

        Returns:
            Count of todos
        """
        return len(self._todos)
