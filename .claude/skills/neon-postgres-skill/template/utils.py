"""
utils.py - Database utility functions for Neon Postgres

Helper functions for database operations, connection management,
and common query patterns.

Usage:
    from utils import get_db_connection, execute_query, fetch_one, fetch_all

    # Execute query
    result = execute_query("INSERT INTO todos (title) VALUES (%s)", ("My todo",))

    # Fetch single row
    todo = fetch_one("SELECT * FROM todos WHERE id = %s", (1,))

    # Fetch multiple rows
    todos = fetch_all("SELECT * FROM todos ORDER BY created_at DESC")
"""

import os
import sys
from contextlib import contextmanager
from typing import Optional, List, Dict, Tuple, Any

try:
    import psycopg2
    from psycopg2 import pool, sql
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("Error: psycopg2 is not installed")
    print("Install it with: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional


# =============================================================================
# CONFIGURATION
# =============================================================================

def get_database_url() -> str:
    """
    Get database URL from environment variables.

    Returns:
        str: PostgreSQL connection URL

    Raises:
        ValueError: If DATABASE_URL is not set
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        # Try to construct from individual components
        host = os.getenv("NEON_DB_HOST")
        port = os.getenv("NEON_DB_PORT", "5432")
        database = os.getenv("NEON_DB_NAME", "neondb")
        user = os.getenv("NEON_DB_USER")
        password = os.getenv("NEON_DB_PASSWORD")

        if all([host, user, password]):
            database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
        else:
            raise ValueError(
                "DATABASE_URL not found. Set DATABASE_URL in .env file or environment variables."
            )

    return database_url


# =============================================================================
# CONNECTION POOL
# =============================================================================

# Global connection pool
_connection_pool: Optional[pool.SimpleConnectionPool] = None


def init_connection_pool(
    minconn: int = 1,
    maxconn: int = 10,
    database_url: Optional[str] = None
) -> pool.SimpleConnectionPool:
    """
    Initialize connection pool.

    Args:
        minconn: Minimum number of connections
        maxconn: Maximum number of connections
        database_url: Optional database URL (uses get_database_url() if not provided)

    Returns:
        SimpleConnectionPool: Connection pool instance
    """
    global _connection_pool

    if _connection_pool is None:
        if database_url is None:
            database_url = get_database_url()

        _connection_pool = pool.SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            dsn=database_url
        )

    return _connection_pool


def get_connection_pool() -> pool.SimpleConnectionPool:
    """
    Get existing connection pool or create new one.

    Returns:
        SimpleConnectionPool: Connection pool instance
    """
    if _connection_pool is None:
        return init_connection_pool()
    return _connection_pool


def close_connection_pool():
    """Close all connections in the pool."""
    global _connection_pool
    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None


# =============================================================================
# CONNECTION MANAGEMENT
# =============================================================================

@contextmanager
def get_db_connection(use_pool: bool = True, dict_cursor: bool = True):
    """
    Context manager for database connections.

    Args:
        use_pool: Whether to use connection pool
        dict_cursor: Whether to use RealDictCursor (returns rows as dicts)

    Yields:
        Connection: Database connection

    Example:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos")
            results = cursor.fetchall()
    """
    if use_pool:
        pool_instance = get_connection_pool()
        conn = pool_instance.getconn()
    else:
        database_url = get_database_url()
        conn = psycopg2.connect(database_url)

    try:
        if dict_cursor:
            conn.cursor_factory = RealDictCursor

        yield conn
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        if use_pool:
            pool_instance.putconn(conn)
        else:
            conn.close()


# =============================================================================
# QUERY EXECUTION
# =============================================================================

def execute_query(
    query: str,
    params: Optional[Tuple] = None,
    fetch: bool = False,
    dict_cursor: bool = True
) -> Optional[List[Dict]]:
    """
    Execute a SQL query.

    Args:
        query: SQL query string
        params: Query parameters (tuple)
        fetch: Whether to fetch results (for SELECT queries)
        dict_cursor: Whether to return results as dicts

    Returns:
        List of results if fetch=True, None otherwise

    Example:
        # INSERT
        execute_query(
            "INSERT INTO todos (title) VALUES (%s)",
            ("My todo",)
        )

        # SELECT
        results = execute_query(
            "SELECT * FROM todos WHERE completed = %s",
            (False,),
            fetch=True
        )
    """
    with get_db_connection(dict_cursor=dict_cursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if fetch:
                return cursor.fetchall()

            return None


def fetch_one(
    query: str,
    params: Optional[Tuple] = None,
    dict_cursor: bool = True
) -> Optional[Dict]:
    """
    Fetch a single row.

    Args:
        query: SQL query string
        params: Query parameters (tuple)
        dict_cursor: Whether to return result as dict

    Returns:
        Single row as dict (or None if no results)

    Example:
        todo = fetch_one("SELECT * FROM todos WHERE id = %s", (1,))
        if todo:
            print(todo['title'])
    """
    with get_db_connection(dict_cursor=dict_cursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()


def fetch_all(
    query: str,
    params: Optional[Tuple] = None,
    dict_cursor: bool = True
) -> List[Dict]:
    """
    Fetch all rows.

    Args:
        query: SQL query string
        params: Query parameters (tuple)
        dict_cursor: Whether to return results as dicts

    Returns:
        List of rows as dicts

    Example:
        todos = fetch_all("SELECT * FROM todos ORDER BY created_at DESC")
        for todo in todos:
            print(todo['title'])
    """
    with get_db_connection(dict_cursor=dict_cursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


def fetch_paginated(
    query: str,
    params: Optional[Tuple] = None,
    limit: int = 50,
    offset: int = 0,
    dict_cursor: bool = True
) -> Tuple[List[Dict], int]:
    """
    Fetch paginated results with total count.

    Args:
        query: SQL query string (without LIMIT/OFFSET)
        params: Query parameters (tuple)
        limit: Number of rows to return
        offset: Number of rows to skip
        dict_cursor: Whether to return results as dicts

    Returns:
        Tuple of (results, total_count)

    Example:
        results, total = fetch_paginated(
            "SELECT * FROM todos WHERE completed = %s ORDER BY created_at DESC",
            (False,),
            limit=10,
            offset=0
        )
        print(f"Showing {len(results)} of {total} results")
    """
    with get_db_connection(dict_cursor=dict_cursor) as conn:
        with conn.cursor() as cursor:
            # Get total count
            count_query = f"SELECT COUNT(*) FROM ({query}) AS count_query"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0] if not dict_cursor else cursor.fetchone()['count']

            # Get paginated results
            paginated_query = f"{query} LIMIT %s OFFSET %s"
            paginated_params = params + (limit, offset) if params else (limit, offset)
            cursor.execute(paginated_query, paginated_params)
            results = cursor.fetchall()

            return results, total_count


# =============================================================================
# CRUD HELPERS
# =============================================================================

def insert_one(table: str, data: Dict) -> Optional[Dict]:
    """
    Insert a single row and return it.

    Args:
        table: Table name
        data: Dictionary of column: value pairs

    Returns:
        Inserted row as dict

    Example:
        todo = insert_one('todos', {
            'title': 'My todo',
            'description': 'Todo description',
            'priority': 'high'
        })
        print(f"Created todo with id: {todo['id']}")
    """
    columns = list(data.keys())
    values = list(data.values())
    placeholders = ', '.join(['%s'] * len(values))

    query = sql.SQL(
        "INSERT INTO {} ({}) VALUES ({}) RETURNING *"
    ).format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(placeholders)
    )

    return fetch_one(query.as_string(psycopg2.connect(get_database_url())), tuple(values))


def update_one(table: str, id: int, data: Dict, id_column: str = 'id') -> Optional[Dict]:
    """
    Update a single row by ID and return it.

    Args:
        table: Table name
        id: Row ID
        data: Dictionary of column: value pairs to update
        id_column: Name of ID column (default: 'id')

    Returns:
        Updated row as dict

    Example:
        todo = update_one('todos', 1, {
            'completed': True,
            'priority': 'low'
        })
        print(f"Updated todo: {todo['title']}")
    """
    set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
    values = list(data.values()) + [id]

    query = sql.SQL(
        "UPDATE {} SET {}, updated_at = CURRENT_TIMESTAMP WHERE {} = %s RETURNING *"
    ).format(
        sql.Identifier(table),
        sql.SQL(set_clause),
        sql.Identifier(id_column)
    )

    return fetch_one(query.as_string(psycopg2.connect(get_database_url())), tuple(values))


def delete_one(table: str, id: int, id_column: str = 'id') -> Optional[Dict]:
    """
    Delete a single row by ID and return it.

    Args:
        table: Table name
        id: Row ID
        id_column: Name of ID column (default: 'id')

    Returns:
        Deleted row as dict

    Example:
        todo = delete_one('todos', 1)
        print(f"Deleted todo: {todo['title']}")
    """
    query = sql.SQL(
        "DELETE FROM {} WHERE {} = %s RETURNING *"
    ).format(
        sql.Identifier(table),
        sql.Identifier(id_column)
    )

    return fetch_one(query.as_string(psycopg2.connect(get_database_url())), (id,))


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        bool: True if connection successful, False otherwise

    Example:
        if test_connection():
            print("Database connection successful")
        else:
            print("Database connection failed")
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False


def get_table_info(table_name: str) -> Dict:
    """
    Get information about a table.

    Args:
        table_name: Name of the table

    Returns:
        Dictionary with table information

    Example:
        info = get_table_info('todos')
        print(f"Table has {info['row_count']} rows")
    """
    query = """
        SELECT
            (SELECT COUNT(*) FROM {table}) as row_count,
            (SELECT COUNT(*) FROM information_schema.columns
             WHERE table_name = %s) as column_count
    """.format(table=sql.Identifier(table_name))

    result = fetch_one(query, (table_name,))

    return {
        'table_name': table_name,
        'row_count': result['row_count'] if result else 0,
        'column_count': result['column_count'] if result else 0
    }


# =============================================================================
# CLEANUP
# =============================================================================

def cleanup():
    """Close all database connections."""
    close_connection_pool()


# Register cleanup on exit
import atexit
atexit.register(cleanup)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Test connection
    if test_connection():
        print("✅ Database connection successful")

        # Example queries
        print("\nExample 1: Fetch all todos")
        todos = fetch_all("SELECT * FROM todos ORDER BY created_at DESC LIMIT 5")
        for todo in todos:
            print(f"  - {todo['title']} (completed: {todo['completed']})")

        print("\nExample 2: Fetch single todo")
        todo = fetch_one("SELECT * FROM todos WHERE id = %s", (1,))
        if todo:
            print(f"  Todo: {todo['title']}")

        print("\nExample 3: Insert new todo")
        new_todo = insert_one('todos', {
            'title': 'Test todo from utils.py',
            'description': 'This is a test',
            'priority': 'low'
        })
        if new_todo:
            print(f"  Created todo with ID: {new_todo['id']}")

            # Update it
            print("\nExample 4: Update todo")
            updated = update_one('todos', new_todo['id'], {'completed': True})
            if updated:
                print(f"  Updated todo: {updated['title']} (completed: {updated['completed']})")

            # Delete it
            print("\nExample 5: Delete todo")
            deleted = delete_one('todos', new_todo['id'])
            if deleted:
                print(f"  Deleted todo: {deleted['title']}")

        print("\nExample 6: Paginated results")
        results, total = fetch_paginated(
            "SELECT * FROM todos ORDER BY created_at DESC",
            limit=5,
            offset=0
        )
        print(f"  Showing {len(results)} of {total} total todos")

    else:
        print("❌ Database connection failed")
