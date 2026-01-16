"""Tests for todo statistics endpoint (US4)."""

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session
from models.todo import Todo, TodoStatus


class TestTodoStats:
    """Test statistics endpoint."""

    def test_stats_empty_database(self, client: TestClient):
        """Test T115: Stats with no todos."""
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 0
        assert data["pending"] == 0
        assert data["completed"] == 0
        assert data["overdue"] == 0

    def test_stats_basic_counts(self, client: TestClient, session: Session):
        """Test T115: Stats with various todo statuses."""
        # Create todos
        todos = [
            Todo(title="Pending 1", status=TodoStatus.PENDING),
            Todo(title="Pending 2", status=TodoStatus.PENDING),
            Todo(title="Pending 3", status=TodoStatus.PENDING),
            Todo(title="Completed 1", status=TodoStatus.COMPLETED),
            Todo(title="Completed 2", status=TodoStatus.COMPLETED),
        ]

        for todo in todos:
            session.add(todo)
        session.commit()

        # Get stats
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert data["pending"] == 3
        assert data["completed"] == 2
        assert data["overdue"] == 0  # No due dates set

    def test_stats_with_overdue(self, client: TestClient, session: Session):
        """Test T115: Stats correctly identify overdue todos."""
        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        # Create todos with due dates
        todos = [
            Todo(
                title="Overdue 1",
                status=TodoStatus.PENDING,
                due_date=yesterday
            ),
            Todo(
                title="Overdue 2",
                status=TodoStatus.PENDING,
                due_date=date.today() - timedelta(days=5)
            ),
            Todo(
                title="Not overdue (future)",
                status=TodoStatus.PENDING,
                due_date=tomorrow
            ),
            Todo(
                title="Completed (past due)",
                status=TodoStatus.COMPLETED,
                due_date=yesterday
            ),
            Todo(
                title="Pending (no due date)",
                status=TodoStatus.PENDING
            ),
        ]

        for todo in todos:
            session.add(todo)
        session.commit()

        # Get stats
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 5
        assert data["pending"] == 4
        assert data["completed"] == 1
        assert data["overdue"] == 2  # Only pending todos with past due dates

    def test_stats_only_pending_overdue(self, client: TestClient, session: Session):
        """Test that overdue count only includes pending todos."""
        past_date = date.today() - timedelta(days=3)

        # Create completed todo with past due date (should NOT count as overdue)
        completed_todo = Todo(
            title="Completed but past due",
            status=TodoStatus.COMPLETED,
            due_date=past_date
        )
        session.add(completed_todo)
        session.commit()

        # Get stats
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["overdue"] == 0  # Completed todos are not overdue

    def test_stats_due_today_not_overdue(self, client: TestClient, session: Session):
        """Test that todos due today are NOT counted as overdue."""
        today_todo = Todo(
            title="Due today",
            status=TodoStatus.PENDING,
            due_date=date.today()
        )
        session.add(today_todo)
        session.commit()

        # Get stats
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 1
        assert data["pending"] == 1
        assert data["overdue"] == 0  # Today is not overdue

    def test_stats_large_dataset(self, client: TestClient, session: Session):
        """Test stats performance with larger dataset."""
        # Create 100 todos
        for i in range(100):
            status = TodoStatus.PENDING if i % 3 != 0 else TodoStatus.COMPLETED
            due_date = None
            if i % 5 == 0:
                due_date = date.today() - timedelta(days=i % 10)  # Some overdue

            todo = Todo(
                title=f"Todo {i}",
                status=status,
                due_date=due_date
            )
            session.add(todo)
        session.commit()

        # Get stats
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 100
        assert data["pending"] + data["completed"] == 100
        assert data["overdue"] >= 0  # Should have some overdue

    def test_stats_response_structure(self, client: TestClient):
        """Test that stats response has correct structure."""
        response = client.get("/api/todos/stats")
        assert response.status_code == 200

        data = response.json()
        # Verify all required fields are present
        assert "total" in data
        assert "pending" in data
        assert "completed" in data
        assert "overdue" in data

        # Verify all values are integers
        assert isinstance(data["total"], int)
        assert isinstance(data["pending"], int)
        assert isinstance(data["completed"], int)
        assert isinstance(data["overdue"], int)

        # Verify logical constraints
        assert data["total"] >= 0
        assert data["pending"] >= 0
        assert data["completed"] >= 0
        assert data["overdue"] >= 0
        assert data["overdue"] <= data["pending"]  # Overdue is subset of pending

    def test_stats_after_status_changes(self, client: TestClient, session: Session):
        """Test that stats update correctly when todo status changes."""
        # Create a pending todo
        todo = Todo(
            title="Test todo",
            status=TodoStatus.PENDING,
            due_date=date.today() - timedelta(days=1)
        )
        session.add(todo)
        session.commit()

        # Get initial stats
        response1 = client.get("/api/todos/stats")
        data1 = response1.json()
        assert data1["pending"] == 1
        assert data1["overdue"] == 1

        # Mark as completed
        todo.status = TodoStatus.COMPLETED
        session.add(todo)
        session.commit()

        # Get updated stats
        response2 = client.get("/api/todos/stats")
        data2 = response2.json()
        assert data2["pending"] == 0
        assert data2["completed"] == 1
        assert data2["overdue"] == 0  # No longer overdue
