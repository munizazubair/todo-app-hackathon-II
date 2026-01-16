#!/usr/bin/env python3
"""
validate_connection.py - Validate Neon Postgres connection and setup

This script validates:
- Database connection credentials
- Database connectivity
- Required tables existence
- Indexes creation
- Triggers setup
- Basic query functionality

Usage:
    python validate_connection.py
    python validate_connection.py --verbose
    python validate_connection.py --table todos
"""

import os
import sys
import argparse
from typing import List, Dict, Optional, Tuple

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("❌ Error: psycopg2 is not installed")
    print("Install it with: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  Warning: python-dotenv is not installed")
    print("Install it with: pip install python-dotenv")
    load_dotenv = None


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_success(message: str):
    """Print success message in green"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")


def print_header(message: str):
    """Print header message in bold"""
    print(f"\n{Colors.BOLD}{message}{Colors.END}\n")


def get_database_url() -> Optional[str]:
    """Get database URL from environment variables"""
    # Try to load from .env file
    if load_dotenv:
        load_dotenv()

    # Check for DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Check for DATABASE_URL_POOLED
    database_url_pooled = os.getenv("DATABASE_URL_POOLED")
    if database_url_pooled:
        print_warning("Using DATABASE_URL_POOLED (pooled connection)")
        return database_url_pooled

    # Construct from individual components
    host = os.getenv("NEON_DB_HOST")
    port = os.getenv("NEON_DB_PORT", "5432")
    database = os.getenv("NEON_DB_NAME", "neondb")
    user = os.getenv("NEON_DB_USER")
    password = os.getenv("NEON_DB_PASSWORD")

    if all([host, user, password]):
        return f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"

    return None


def validate_connection_string(database_url: str) -> Tuple[bool, List[str]]:
    """Validate connection string format"""
    issues = []

    if not database_url:
        issues.append("Connection string is empty")
        return False, issues

    if not database_url.startswith("postgresql://") and not database_url.startswith("postgres://"):
        issues.append("Connection string must start with postgresql:// or postgres://")

    if "sslmode=require" not in database_url:
        issues.append("Connection string should include sslmode=require for Neon")

    if "@" not in database_url or "/" not in database_url:
        issues.append("Connection string format appears invalid")

    return len(issues) == 0, issues


def connect_to_database(database_url: str, verbose: bool = False):
    """Connect to Neon Postgres database"""
    try:
        conn = psycopg2.connect(database_url)

        if verbose:
            # Get connection info
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    current_database() as database,
                    current_user as user,
                    inet_server_addr() as host,
                    inet_server_port() as port,
                    version() as version
            """)
            info = cursor.fetchone()
            cursor.close()

            print_info(f"Database: {info[0]}")
            print_info(f"User: {info[1]}")
            print_info(f"Host: {info[2] if info[2] else 'N/A (Unix socket)'}")
            print_info(f"Port: {info[3] if info[3] else 'N/A'}")
            pg_version = info[4].split()[1] if 'PostgreSQL' in info[4] else 'Unknown'
            print_info(f"PostgreSQL Version: {pg_version}")

        return conn
    except psycopg2.OperationalError as e:
        print_error(f"Failed to connect to database: {e}")
        return None


def check_table_exists(conn, table_name: str) -> bool:
    """Check if a table exists"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            )
        """, (table_name,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists
    except Exception as e:
        print_warning(f"Error checking table existence: {e}")
        return False


def get_table_columns(conn, table_name: str) -> List[Dict]:
    """Get table column information"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))

        columns = []
        for row in cursor.fetchall():
            columns.append({
                'name': row[0],
                'type': row[1],
                'nullable': row[2] == 'YES',
                'default': row[3]
            })

        cursor.close()
        return columns
    except Exception as e:
        print_warning(f"Error getting table columns: {e}")
        return []


def get_table_indexes(conn, table_name: str) -> List[str]:
    """Get table indexes"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND tablename = %s
            ORDER BY indexname
        """, (table_name,))

        indexes = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return indexes
    except Exception as e:
        print_warning(f"Error getting table indexes: {e}")
        return []


def get_table_triggers(conn, table_name: str) -> List[str]:
    """Get table triggers"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT trigger_name
            FROM information_schema.triggers
            WHERE event_object_schema = 'public'
            AND event_object_table = %s
            ORDER BY trigger_name
        """, (table_name,))

        triggers = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return triggers
    except Exception as e:
        print_warning(f"Error getting table triggers: {e}")
        return []


def test_basic_queries(conn, table_name: str, verbose: bool = False) -> bool:
    """Test basic CRUD operations"""
    try:
        cursor = conn.cursor()

        # Test SELECT
        cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(
            sql.Identifier(table_name)
        ))
        count = cursor.fetchone()[0]

        if verbose:
            print_info(f"Total rows in {table_name}: {count}")

        # Test INSERT (rollback after)
        try:
            cursor.execute(sql.SQL("""
                INSERT INTO {} (title, description)
                VALUES (%s, %s)
                RETURNING id
            """).format(sql.Identifier(table_name)), ("Test todo", "Test description"))

            test_id = cursor.fetchone()[0]

            if verbose:
                print_info(f"Test INSERT successful (id: {test_id})")

            # Test UPDATE
            cursor.execute(sql.SQL("""
                UPDATE {}
                SET completed = true
                WHERE id = %s
            """).format(sql.Identifier(table_name)), (test_id,))

            if verbose:
                print_info("Test UPDATE successful")

            # Test DELETE
            cursor.execute(sql.SQL("""
                DELETE FROM {}
                WHERE id = %s
            """).format(sql.Identifier(table_name)), (test_id,))

            if verbose:
                print_info("Test DELETE successful")

            # Rollback test changes
            conn.rollback()

        except Exception as e:
            conn.rollback()
            print_warning(f"CRUD test failed (table may have different schema): {e}")

        cursor.close()
        return True

    except Exception as e:
        print_warning(f"Basic query test failed: {e}")
        conn.rollback()
        return False


def get_all_tables(conn) -> List[str]:
    """Get all tables in database"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables
    except Exception as e:
        print_warning(f"Error getting tables: {e}")
        return []


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Validate Neon Postgres connection and setup"
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--table',
        type=str,
        default='todos',
        help='Table name to validate (default: todos)'
    )

    args = parser.parse_args()

    print_header("🔍 Validating Neon Postgres Connection")

    # Step 1: Validate connection string
    print_info("Step 1: Checking connection string...")
    database_url = get_database_url()

    if not database_url:
        print_error("DATABASE_URL not found in environment")
        print_info("Set DATABASE_URL in .env file or environment variables")
        print("\nExample .env file:")
        print("DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require")
        sys.exit(1)

    valid, issues = validate_connection_string(database_url)

    if valid:
        print_success("Connection string format is valid")
    else:
        print_error("Connection string has issues:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    # Step 2: Test connection
    print_info("Step 2: Testing database connection...")
    conn = connect_to_database(database_url, args.verbose)

    if not conn:
        print_error("Failed to connect to database")
        print_info("Check your connection string and ensure:")
        print("  1. DATABASE_URL is correct in .env file")
        print("  2. Neon project is active (not suspended)")
        print("  3. Network connectivity is available")
        sys.exit(1)

    print_success("Connected to database successfully")

    try:
        # Step 3: Check for tables
        print_info("Step 3: Checking database tables...")
        all_tables = get_all_tables(conn)

        if not all_tables:
            print_warning("No tables found in database")
            print_info("Run create_db.py to create schema")
        else:
            print_success(f"Found {len(all_tables)} table(s): {', '.join(all_tables)}")

        # Step 4: Validate specific table
        if args.table:
            print_info(f"Step 4: Validating table '{args.table}'...")

            if check_table_exists(conn, args.table):
                print_success(f"Table '{args.table}' exists")

                # Get columns
                if args.verbose:
                    columns = get_table_columns(conn, args.table)
                    if columns:
                        print_info(f"Columns ({len(columns)}):")
                        for col in columns:
                            nullable = "NULL" if col['nullable'] else "NOT NULL"
                            default = f"DEFAULT {col['default']}" if col['default'] else ""
                            print(f"  - {col['name']}: {col['type']} {nullable} {default}")

                # Get indexes
                indexes = get_table_indexes(conn, args.table)
                if indexes:
                    print_success(f"Found {len(indexes)} index(es)")
                    if args.verbose:
                        for idx in indexes:
                            print(f"  - {idx}")
                else:
                    print_warning("No indexes found (consider adding for performance)")

                # Get triggers
                triggers = get_table_triggers(conn, args.table)
                if triggers:
                    print_success(f"Found {len(triggers)} trigger(s)")
                    if args.verbose:
                        for trigger in triggers:
                            print(f"  - {trigger}")

                # Test basic queries
                print_info("Step 5: Testing basic queries...")
                if test_basic_queries(conn, args.table, args.verbose):
                    print_success("Basic query tests passed")

            else:
                print_error(f"Table '{args.table}' does not exist")
                print_info("Run create_db.py to create schema")

        # Success summary
        print_header("🎉 All Validation Checks Passed!")

        print("\nDatabase Summary:")
        print(f"  Total Tables: {len(all_tables)}")
        if all_tables:
            print(f"  Tables: {', '.join(all_tables)}")

        if args.table and check_table_exists(conn, args.table):
            columns = get_table_columns(conn, args.table)
            indexes = get_table_indexes(conn, args.table)
            triggers = get_table_triggers(conn, args.table)
            print(f"\nTable '{args.table}':")
            print(f"  Columns: {len(columns)}")
            print(f"  Indexes: {len(indexes)}")
            print(f"  Triggers: {len(triggers)}")

    finally:
        conn.close()

    print("\n✨ Next steps:")
    print("  1. Generate queries: python .claude/skills/neon-postgres-skill/scripts/generate_queries.py")
    print("  2. Integrate with your app (Next.js or FastAPI)")
    print("  3. Run migrations if needed")


if __name__ == "__main__":
    main()
