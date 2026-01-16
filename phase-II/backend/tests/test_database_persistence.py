"""Tests for database persistence (US3)."""

import pytest
from datetime import datetime, timedelta
from sqlmodel import Session, select, text
from models.todo import Todo, TodoStatus


class TestDatabasePersistence:
    """Test database persistence across server restarts."""

    def test_todo_persists_across_sessions(self, engine):
        """
        Test T092: Create todo, close session, reopen, verify todo still exists.

        This simulates a server restart by creating separate sessions.
        """
        todo_id = None

        # Session 1: Create a todo
        with Session(engine) as session:
            todo = Todo(
                title="Test persistence",
                category="Testing",
                status=TodoStatus.PENDING
            )
            session.add(todo)
            session.commit()
            session.refresh(todo)
            todo_id = todo.id
            assert todo_id is not None

        # Session closed (simulates server shutdown)

        # Session 2: Verify todo exists (simulates server restart)
        with Session(engine) as session:
            retrieved_todo = session.get(Todo, todo_id)
            assert retrieved_todo is not None
            assert retrieved_todo.title == "Test persistence"
            assert retrieved_todo.category == "Testing"
            assert retrieved_todo.status == TodoStatus.PENDING
            assert retrieved_todo.id == todo_id

    def test_updated_at_timestamp_changes(self, engine):
        """
        Test T093: Update todo, verify updated_at timestamp changed.
        """
        todo_id = None
        original_updated_at = None

        # Create a todo
        with Session(engine) as session:
            todo = Todo(
                title="Test timestamp update",
                status=TodoStatus.PENDING
            )
            session.add(todo)
            session.commit()
            session.refresh(todo)
            todo_id = todo.id
            original_updated_at = todo.updated_at

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.1)

        # Update the todo
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            assert todo is not None
            todo.title = "Updated title"
            todo.updated_at = datetime.utcnow()  # Manually update timestamp
            session.add(todo)
            session.commit()
            session.refresh(todo)
            new_updated_at = todo.updated_at

        # Verify timestamp changed
        assert new_updated_at > original_updated_at

    def test_created_at_timestamp_immutable(self, engine):
        """Verify that created_at timestamp doesn't change on updates."""
        todo_id = None
        original_created_at = None

        # Create a todo
        with Session(engine) as session:
            todo = Todo(
                title="Test created_at immutability",
                status=TodoStatus.PENDING
            )
            session.add(todo)
            session.commit()
            session.refresh(todo)
            todo_id = todo.id
            original_created_at = todo.created_at

        # Update the todo
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            assert todo is not None
            todo.title = "Updated title"
            todo.updated_at = datetime.utcnow()
            session.add(todo)
            session.commit()
            session.refresh(todo)

        # Verify created_at hasn't changed
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            assert todo.created_at == original_created_at

    def test_multiple_todos_persist(self, engine):
        """Verify multiple todos can be created and retrieved."""
        # Create multiple todos
        todo_ids = []
        with Session(engine) as session:
            for i in range(5):
                todo = Todo(
                    title=f"Todo {i}",
                    category=f"Category {i % 2}",
                    status=TodoStatus.PENDING if i % 2 == 0 else TodoStatus.COMPLETED
                )
                session.add(todo)
                session.commit()
                session.refresh(todo)
                todo_ids.append(todo.id)

        # Verify all todos exist
        with Session(engine) as session:
            for i, todo_id in enumerate(todo_ids):
                todo = session.get(Todo, todo_id)
                assert todo is not None
                assert todo.title == f"Todo {i}"
                assert todo.category == f"Category {i % 2}"
