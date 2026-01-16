#!/usr/bin/env python3
"""
create_db.py - Create Neon Postgres database schema

This script connects to Neon Postgres using credentials from environment
variables and creates the database schema from a template file.

Usage:
    python create_db.py
    python create_db.py --schema-file custom_schema.sql
    python create_db.py --drop-existing
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    import psycopg2
    from psycopg2 import sql, errors
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

    # Check for DATABASE_URL_DIRECT (for migrations)
    database_url_direct = os.getenv("DATABASE_URL_DIRECT")
    if database_url_direct:
        print_warning("Using DATABASE_URL_DIRECT (direct connection)")
        return database_url_direct

    # Construct from individual components
    host = os.getenv("NEON_DB_HOST")
    port = os.getenv("NEON_DB_PORT", "5432")
    database = os.getenv("NEON_DB_NAME", "neondb")
    user = os.getenv("NEON_DB_USER")
    password = os.getenv("NEON_DB_PASSWORD")

    if all([host, user, password]):
        return f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"

    return None


def get_default_schema_path() -> Path:
    """Get default schema file path"""
    # Look for schema.sql in common locations
    locations = [
        Path(__file__).parent.parent / "template" / "schema.sql",
        Path.cwd() / "database" / "schema.sql",
        Path.cwd() / "schema.sql",
    ]

    for location in locations:
        if location.exists():
            return location

    # Return default location even if it doesn't exist
    return Path(__file__).parent.parent / "template" / "schema.sql"


def connect_to_database(database_url: str):
    """Connect to Neon Postgres database"""
    try:
        conn = psycopg2.connect(database_url)
        conn.autocommit = False
        return conn
    except psycopg2.OperationalError as e:
        print_error(f"Failed to connect to database: {e}")
        print_info("Check your connection string and ensure:")
        print("  1. DATABASE_URL is set in .env file")
        print("  2. Neon project is active (not suspended)")
        print("  3. Connection string includes ?sslmode=require")
        sys.exit(1)


def read_schema_file(schema_path: Path) -> str:
    """Read SQL schema from file"""
    if not schema_path.exists():
        print_error(f"Schema file not found: {schema_path}")
        print_info("Create a schema.sql file or specify path with --schema-file")
        sys.exit(1)

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print_error(f"Failed to read schema file: {e}")
        sys.exit(1)


def drop_existing_tables(conn):
    """Drop existing tables (use with caution!)"""
    print_warning("Dropping existing tables...")

    try:
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)

        tables = cursor.fetchall()

        if not tables:
            print_info("No existing tables to drop")
            return

        # Drop each table
        for (table_name,) in tables:
            cursor.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(
                sql.Identifier(table_name)
            ))
            print_success(f"Dropped table: {table_name}")

        conn.commit()
        cursor.close()

    except Exception as e:
        conn.rollback()
        print_error(f"Failed to drop tables: {e}")
        sys.exit(1)


def execute_schema(conn, schema_sql: str):
    """Execute schema SQL"""
    try:
        cursor = conn.cursor()

        # Split schema into individual statements
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]

        for statement in statements:
            try:
                cursor.execute(statement)

                # Check if statement creates a table, index, or trigger
                statement_lower = statement.lower()
                if 'create table' in statement_lower:
                    # Extract table name
                    parts = statement_lower.split('create table')[1].split('(')[0].strip()
                    table_name = parts.replace('if not exists', '').strip()
                    print_success(f"Created table: {table_name}")
                elif 'create index' in statement_lower:
                    # Extract index name
                    parts = statement_lower.split('create index')[1].split('on')[0].strip()
                    index_name = parts.replace('if not exists', '').strip()
                    print_success(f"Created index: {index_name}")
                elif 'create trigger' in statement_lower:
                    # Extract trigger name
                    parts = statement_lower.split('create trigger')[1].split('before')[0].strip()
                    trigger_name = parts.strip()
                    print_success(f"Created trigger: {trigger_name}")
                elif 'create function' in statement_lower or 'create or replace function' in statement_lower:
                    # Extract function name
                    if 'create or replace function' in statement_lower:
                        parts = statement_lower.split('create or replace function')[1].split('(')[0].strip()
                    else:
                        parts = statement_lower.split('create function')[1].split('(')[0].strip()
                    function_name = parts.strip()
                    print_success(f"Created function: {function_name}")

            except errors.DuplicateTable:
                print_warning(f"Table already exists (skipped)")
            except errors.DuplicateObject:
                print_warning(f"Object already exists (skipped)")
            except Exception as e:
                print_error(f"Failed to execute statement: {e}")
                print_info(f"Statement: {statement[:100]}...")
                conn.rollback()
                raise

        conn.commit()
        cursor.close()

    except Exception as e:
        conn.rollback()
        print_error(f"Failed to execute schema: {e}")
        sys.exit(1)


def get_database_info(conn):
    """Get database information"""
    try:
        cursor = conn.cursor()

        # Get PostgreSQL version
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        pg_version = version.split()[1] if 'PostgreSQL' in version else 'Unknown'

        # Get connection info
        cursor.execute("SELECT current_database(), current_user")
        db_name, db_user = cursor.fetchone()

        # Get table count
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]

        # Get table names
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        cursor.close()

        return {
            'pg_version': pg_version,
            'database': db_name,
            'user': db_user,
            'table_count': table_count,
            'tables': tables
        }

    except Exception as e:
        print_warning(f"Could not retrieve database info: {e}")
        return None


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Create Neon Postgres database schema"
    )
    parser.add_argument(
        '--schema-file',
        type=Path,
        help='Path to schema SQL file (default: auto-detect)'
    )
    parser.add_argument(
        '--drop-existing',
        action='store_true',
        help='Drop existing tables before creating (CAUTION: destructive!)'
    )

    args = parser.parse_args()

    print_header("🔧 Creating Neon Postgres Database Schema")

    # Get database URL
    database_url = get_database_url()
    if not database_url:
        print_error("DATABASE_URL not found in environment")
        print_info("Set DATABASE_URL in .env file or environment variables")
        print("\nExample .env file:")
        print("DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require")
        sys.exit(1)

    # Get schema file path
    schema_path = args.schema_file or get_default_schema_path()
    print_info(f"Using schema file: {schema_path}")

    # Connect to database
    print_info("Connecting to Neon Postgres...")
    conn = connect_to_database(database_url)
    print_success("Connected to Neon Postgres successfully")

    try:
        # Drop existing tables if requested
        if args.drop_existing:
            response = input(f"{Colors.YELLOW}⚠️  Drop all existing tables? This is destructive! (yes/no): {Colors.END}")
            if response.lower() == 'yes':
                drop_existing_tables(conn)
            else:
                print_info("Skipping table drop")

        # Read schema file
        print_info("Reading schema file...")
        schema_sql = read_schema_file(schema_path)

        # Execute schema
        print_info("Executing schema...")
        execute_schema(conn, schema_sql)

        print_header("🎉 Database Schema Created Successfully!")

        # Get and display database info
        db_info = get_database_info(conn)
        if db_info:
            print("\nDatabase Information:")
            print(f"  PostgreSQL Version: {db_info['pg_version']}")
            print(f"  Database: {db_info['database']}")
            print(f"  User: {db_info['user']}")
            print(f"  Total Tables: {db_info['table_count']}")
            if db_info['tables']:
                print(f"  Tables: {', '.join(db_info['tables'])}")

    finally:
        conn.close()

    print("\n✨ Next steps:")
    print("  1. Run validation: python .claude/skills/neon-postgres-skill/scripts/validate_connection.py")
    print("  2. Generate queries: python .claude/skills/neon-postgres-skill/scripts/generate_queries.py")
    print("  3. Integrate with your app (Next.js or FastAPI)")


if __name__ == "__main__":
    main()
