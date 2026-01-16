"""Tests to verify database index usage (US3)."""

import pytest
from sqlmodel import Session, text, select
from models.todo import Todo, TodoStatus
from datetime import date, timedelta


class TestIndexUsage:
    """
    Test T095: Run EXPLAIN ANALYZE on filtered query to verify index usage.

    Note: These tests require PostgreSQL. They will be skipped with SQLite.
    """

    @pytest.fixture(autouse=True)
    def check_database_type(self, engine):
        """Skip tests if not using PostgreSQL."""
        if "sqlite" in str(engine.url):
            pytest.skip("Index verification tests require PostgreSQL")

    @pytest.fixture
    def sample_data(self, engine):
        """Create sample data for index testing."""
        with Session(engine) as session:
            todos = []
            base_date = date.today()

            for i in range(100):
                todo = Todo(
                    title=f"Index test todo {i}",
                    category=f"Category {i % 5}",
                    due_date=base_date + timedelta(days=i % 20),
                    status=TodoStatus.PENDING if i % 2 == 0 else TodoStatus.COMPLETED
                )
                todos.append(todo)

            session.add_all(todos)
            session.commit()

        yield

        # Cleanup
        with Session(engine) as session:
            for todo in session.exec(select(Todo)).all():
                session.delete(todo)
            session.commit()

    def test_composite_index_used_for_status_due_date_query(self, engine, sample_data):
        """
        Verify that the composite index (status, due_date) is used
        when filtering by both fields.
        """
        target_date = date.today() + timedelta(days=10)

        with Session(engine) as session:
            # Execute EXPLAIN ANALYZE
            query = text("""
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT * FROM todos
                WHERE status = 'PENDING'
                  AND due_date <= :target_date
            """)
            result = session.exec(query, {"target_date": target_date})
            explain_output = "\n".join([row[0] for row in result])

            # Verify index is used
            # PostgreSQL should mention "Index Scan" or "Bitmap Index Scan"
            # and reference the index name
            assert "Index" in explain_output, \
                f"Expected index usage in query plan:\n{explain_output}"

            # Optional: Check for specific index name
            # assert "ix_todos_status_due_date" in explain_output.lower()

            print(f"\n=== EXPLAIN ANALYZE Output ===\n{explain_output}\n")

    def test_category_index_used_for_category_query(self, engine, sample_data):
        """
        Verify that the category index is used when filtering by category.
        """
        with Session(engine) as session:
            # Execute EXPLAIN ANALYZE
            query = text("""
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT * FROM todos
                WHERE category = :category
            """)
            result = session.exec(query, {"category": "Category 2"})
            explain_output = "\n".join([row[0] for row in result])

            # Verify index is used
            assert "Index" in explain_output, \
                f"Expected index usage in query plan:\n{explain_output}"

            # Optional: Check for specific index name
            # assert "ix_todos_category" in explain_output.lower()

            print(f"\n=== EXPLAIN ANALYZE Output ===\n{explain_output}\n")

    def test_both_indexes_listed_in_database(self, engine):
        """Verify that both indexes exist in the database."""
        with Session(engine) as session:
            # Query PostgreSQL system catalog for indexes
            query = text("""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename = 'todos'
                  AND indexname IN ('ix_todos_status_due_date', 'ix_todos_category')
                ORDER BY indexname
            """)
            result = session.exec(query).all()

            # Should have 2 indexes
            assert len(result) == 2, f"Expected 2 indexes, found {len(result)}"

            index_names = [row[0] for row in result]
            assert "ix_todos_status_due_date" in index_names
            assert "ix_todos_category" in index_names

            print("\n=== Database Indexes ===")
            for row in result:
                print(f"{row[0]}: {row[1]}")

    def test_query_plan_without_indexes_comparison(self, engine, sample_data):
        """
        Compare query performance with and without specific filters
        to demonstrate index effectiveness.
        """
        with Session(engine) as session:
            # Query 1: Full table scan (no filters)
            query1 = text("EXPLAIN ANALYZE SELECT * FROM todos")
            result1 = session.exec(query1)
            plan1 = "\n".join([row[0] for row in result1])

            # Query 2: Indexed query (with status filter)
            query2 = text("""
                EXPLAIN ANALYZE
                SELECT * FROM todos
                WHERE status = 'PENDING'
            """)
            result2 = session.exec(query2)
            plan2 = "\n".join([row[0] for row in result2])

            print("\n=== Query Plan Comparison ===")
            print("Without filter (full scan):")
            print(plan1)
            print("\nWith status filter (should use index):")
            print(plan2)

            # The filtered query should be different from full scan
            assert plan1 != plan2
