"""Tests for todo filtering functionality (US4)."""

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session
from models.todo import Todo, TodoStatus


class TestTodoFiltering:
    """Test filtering todos by status, category, and search."""

    @pytest.fixture(autouse=True)
    def setup_test_data(self, session: Session):
        """Create sample todos for filtering tests."""
        # Create diverse todos
        todos = [
            Todo(title="Buy groceries", category="Personal", status=TodoStatus.PENDING),
            Todo(title="Finish project report", category="Work", status=TodoStatus.PENDING),
            Todo(title="Call dentist", category="Personal", status=TodoStatus.COMPLETED),
            Todo(title="Team meeting", category="Work", status=TodoStatus.COMPLETED),
            Todo(title="Gym workout", category="Health", status=TodoStatus.PENDING),
            Todo(title="Read book", category="Personal", status=TodoStatus.PENDING),
            Todo(title="Code review", category="Work", status=TodoStatus.COMPLETED),
        ]

        for todo in todos:
            session.add(todo)
        session.commit()

        yield

        # Cleanup
        for todo in session.query(Todo).all():
            session.delete(todo)
        session.commit()

    def test_filter_by_status_pending(self, client: TestClient):
        """Test T114: Filter todos by pending status."""
        response = client.get("/api/todos/?status=pending")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 4  # Should have 4 pending todos

        # Verify all returned todos are pending
        for todo in data["items"]:
            assert todo["status"] == "pending"

    def test_filter_by_status_completed(self, client: TestClient):
        """Test T114: Filter todos by completed status."""
        response = client.get("/api/todos/?status=completed")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 3  # Should have 3 completed todos

        # Verify all returned todos are completed
        for todo in data["items"]:
            assert todo["status"] == "completed"

    def test_filter_by_category(self, client: TestClient):
        """Test T114: Filter todos by category."""
        response = client.get("/api/todos/?category=Work")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 3  # Should have 3 Work todos

        # Verify all returned todos have Work category
        for todo in data["items"]:
            assert todo["category"] == "Work"

    def test_search_by_title(self, client: TestClient):
        """Test T114: Search todos by title (case-insensitive)."""
        # Search for "project" (should match "Finish project report")
        response = client.get("/api/todos/?search=project")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert "project" in data["items"][0]["title"].lower()

    def test_search_case_insensitive(self, client: TestClient):
        """Test that search is case-insensitive."""
        # Search with uppercase
        response1 = client.get("/api/todos/?search=GYM")
        assert response1.status_code == 200
        assert len(response1.json()["items"]) == 1

        # Search with lowercase
        response2 = client.get("/api/todos/?search=gym")
        assert response2.status_code == 200
        assert len(response2.json()["items"]) == 1

    def test_combined_filters(self, client: TestClient):
        """Test T114: Combine status and category filters."""
        response = client.get("/api/todos/?status=pending&category=Personal")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 2  # "Buy groceries" and "Read book"

        # Verify all match both filters
        for todo in data["items"]:
            assert todo["status"] == "pending"
            assert todo["category"] == "Personal"

    def test_combined_status_search(self, client: TestClient):
        """Test combining status filter and search."""
        response = client.get("/api/todos/?status=completed&search=Call")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Call dentist"
        assert data["items"][0]["status"] == "completed"

    def test_no_results_filter(self, client: TestClient):
        """Test filtering with no matching results."""
        response = client.get("/api/todos/?category=NonExistent")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 0
        assert data["total"] == 0

    def test_all_filters_combined(self, client: TestClient):
        """Test combining all three filters: status, category, search."""
        response = client.get("/api/todos/?status=pending&category=Work&search=project")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Finish project report"

    def test_pagination_with_filters(self, client: TestClient):
        """Test that pagination works correctly with filters."""
        response = client.get("/api/todos/?status=pending&limit=2&offset=0")
        assert response.status_code == 200

        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 4  # Total pending todos
        assert data["limit"] == 2
        assert data["offset"] == 0

    def test_empty_search_returns_all(self, client: TestClient):
        """Test that empty search query returns all todos."""
        response = client.get("/api/todos/")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 7  # All 7 todos
