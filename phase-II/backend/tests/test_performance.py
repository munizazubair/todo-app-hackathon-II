"""Performance tests for database queries (US3)."""

import pytest
import time
from datetime import date, timedelta
from sqlmodel import Session, select
from models.todo import Todo, TodoStatus


class TestDatabasePerformance:
    """Test database query performance with large datasets."""

    @pytest.fixture(autouse=True)
    def setup_large_dataset(self, engine):
        """Create 1000 todos for performance testing."""
        with Session(engine) as session:
            todos = []
            base_date = date.today()

            for i in range(1000):
                todo = Todo(
                    title=f"Performance test todo {i}",
                    category=f"Category {i % 10}",  # 10 different categories
                    due_date=base_date + timedelta(days=i % 30),  # Spread over 30 days
                    status=TodoStatus.PENDING if i % 3 != 0 else TodoStatus.COMPLETED
                )
                todos.append(todo)

            session.add_all(todos)
            session.commit()

        yield

        # Cleanup after tests
        with Session(engine) as session:
            session.exec(select(Todo)).all()
            for todo in session.exec(select(Todo)).all():
                session.delete(todo)
            session.commit()

    def test_query_performance_with_filters(self, engine):
        """
        Test T094: Create 1000 todos, query with filter, assert <100ms.

        Note: SQLite in-memory is very fast, so we'll measure and verify
        the query completes reasonably quickly. In production PostgreSQL,
        the indexes should ensure queries stay under 100ms.
        """
        with Session(engine) as session:
            # Test 1: Filter by status
            start_time = time.time()
            statement = select(Todo).where(Todo.status == TodoStatus.PENDING)
            results = session.exec(statement).all()
            elapsed_ms = (time.time() - start_time) * 1000

            assert len(results) > 0
            assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms, expected <100ms"

    def test_query_performance_composite_index(self, engine):
        """
        Test composite index performance: Filter by status AND due_date.

        This query should use the composite index on (status, due_date).
        """
        target_date = date.today() + timedelta(days=15)

        with Session(engine) as session:
            start_time = time.time()
            statement = select(Todo).where(
                Todo.status == TodoStatus.PENDING,
                Todo.due_date <= target_date
            )
            results = session.exec(statement).all()
            elapsed_ms = (time.time() - start_time) * 1000

            assert len(results) > 0
            assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms, expected <100ms"

    def test_query_performance_category_filter(self, engine):
        """
        Test category index performance: Filter by category.

        This query should use the index on category column.
        """
        with Session(engine) as session:
            start_time = time.time()
            statement = select(Todo).where(Todo.category == "Category 5")
            results = session.exec(statement).all()
            elapsed_ms = (time.time() - start_time) * 1000

            # Should find roughly 100 todos (1000 / 10 categories)
            assert len(results) >= 90  # Allow some variance
            assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms, expected <100ms"

    def test_query_performance_pagination(self, engine):
        """Test pagination performance with large dataset."""
        with Session(engine) as session:
            start_time = time.time()
            statement = select(Todo).limit(20).offset(500)
            results = session.exec(statement).all()
            elapsed_ms = (time.time() - start_time) * 1000

            assert len(results) == 20
            assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms, expected <100ms"

    def test_query_performance_combined_filters(self, engine):
        """Test performance with multiple filters combined."""
        target_date = date.today() + timedelta(days=10)

        with Session(engine) as session:
            start_time = time.time()
            statement = select(Todo).where(
                Todo.status == TodoStatus.PENDING,
                Todo.category == "Category 3",
                Todo.due_date <= target_date
            )
            results = session.exec(statement).all()
            elapsed_ms = (time.time() - start_time) * 1000

            assert len(results) >= 0  # May or may not have results
            assert elapsed_ms < 100, f"Query took {elapsed_ms:.2f}ms, expected <100ms"

    def test_count_query_performance(self, engine):
        """Test count query performance."""
        with Session(engine) as session:
            start_time = time.time()
            statement = select(Todo).where(Todo.status == TodoStatus.COMPLETED)
            count = len(session.exec(statement).all())
            elapsed_ms = (time.time() - start_time) * 1000

            assert count > 0
            assert elapsed_ms < 100, f"Count query took {elapsed_ms:.2f}ms, expected <100ms"
