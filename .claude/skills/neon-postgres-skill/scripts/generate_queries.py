#!/usr/bin/env python3
"""
generate_queries.py - Generate example SQL queries for Neon Postgres

This script generates example SQL queries for common CRUD operations
based on the database schema.

Usage:
    python generate_queries.py
    python generate_queries.py --output queries.sql
    python generate_queries.py --table todos
    python generate_queries.py --format markdown
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

try:
    import psycopg2
except ImportError:
    print("⚠️  Warning: psycopg2 is not installed")
    print("Install it with: pip install psycopg2-binary")
    print("Generating queries without database connection...")
    psycopg2 = None

try:
    from dotenv import load_dotenv
except ImportError:
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


def get_table_schema(table_name: str = "todos") -> Dict:
    """Get or generate table schema"""
    # Default schema for todos table
    default_schema = {
        'table_name': table_name,
        'columns': [
            {'name': 'id', 'type': 'SERIAL', 'nullable': False, 'primary_key': True},
            {'name': 'title', 'type': 'VARCHAR(255)', 'nullable': False},
            {'name': 'description', 'type': 'TEXT', 'nullable': True},
            {'name': 'completed', 'type': 'BOOLEAN', 'nullable': False, 'default': 'FALSE'},
            {'name': 'priority', 'type': 'VARCHAR(20)', 'nullable': True},
            {'name': 'created_at', 'type': 'TIMESTAMP', 'nullable': False, 'default': 'CURRENT_TIMESTAMP'},
            {'name': 'updated_at', 'type': 'TIMESTAMP', 'nullable': False, 'default': 'CURRENT_TIMESTAMP'},
        ]
    }

    # Try to get actual schema from database
    if psycopg2 and load_dotenv:
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")

        if database_url:
            try:
                conn = psycopg2.connect(database_url)
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
                conn.close()

                if columns:
                    return {'table_name': table_name, 'columns': columns}

            except Exception:
                pass  # Fall back to default schema

    return default_schema


def generate_insert_queries(schema: Dict) -> List[str]:
    """Generate INSERT queries"""
    table_name = schema['table_name']
    queries = []

    # Get non-auto columns
    columns = [col for col in schema['columns']
               if col['name'] != 'id' and
               not (col.get('default') and 'CURRENT_TIMESTAMP' in str(col.get('default')))]

    column_names = [col['name'] for col in columns]

    # Single insert with positional parameters
    queries.append(f"""-- Insert single {table_name[:-1] if table_name.endswith('s') else table_name}
INSERT INTO {table_name} ({', '.join(column_names)})
VALUES ({', '.join(f'${i+1}' for i in range(len(column_names)))})
RETURNING *;
""")

    # Insert with example data
    if table_name == 'todos':
        queries.append(f"""-- Insert with example data
INSERT INTO {table_name} (title, description, completed, priority)
VALUES ('Complete project documentation', 'Write comprehensive docs for Phase II', false, 'high')
RETURNING *;
""")

        # Batch insert
        queries.append(f"""-- Batch insert multiple {table_name}
INSERT INTO {table_name} (title, description, completed, priority)
VALUES
    ('Setup database', 'Configure Neon Postgres', true, 'high'),
    ('Create API endpoints', 'Build REST API with FastAPI', false, 'high'),
    ('Design UI components', 'Create reusable React components', false, 'medium'),
    ('Write tests', 'Add unit and integration tests', false, 'medium'),
    ('Deploy application', 'Deploy to production', false, 'low')
RETURNING *;
""")

    # Upsert (INSERT ... ON CONFLICT)
    queries.append(f"""-- Upsert (insert or update on conflict)
INSERT INTO {table_name} (id, {', '.join(column_names)})
VALUES ($1, {', '.join(f'${i+2}' for i in range(len(column_names)))})
ON CONFLICT (id) DO UPDATE
SET {', '.join(f'{col} = EXCLUDED.{col}' for col in column_names)}
RETURNING *;
""")

    return queries


def generate_select_queries(schema: Dict) -> List[str]:
    """Generate SELECT queries"""
    table_name = schema['table_name']
    queries = []

    # Select all
    queries.append(f"""-- Select all {table_name}
SELECT * FROM {table_name}
ORDER BY created_at DESC;
""")

    # Select with limit and offset (pagination)
    queries.append(f"""-- Select with pagination
SELECT * FROM {table_name}
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;
""")

    # Select by ID
    queries.append(f"""-- Select by ID
SELECT * FROM {table_name}
WHERE id = $1;
""")

    # Table-specific queries
    if table_name == 'todos':
        # Select active todos
        queries.append(f"""-- Select active (incomplete) todos
SELECT * FROM {table_name}
WHERE completed = false
ORDER BY created_at DESC;
""")

        # Select by priority
        queries.append(f"""-- Select by priority
SELECT * FROM {table_name}
WHERE priority = $1
ORDER BY created_at DESC;
""")

        # Select with multiple filters
        queries.append(f"""-- Select with multiple filters
SELECT * FROM {table_name}
WHERE completed = $1
  AND priority = $2
ORDER BY created_at DESC;
""")

        # Full-text search
        queries.append(f"""-- Search todos (case-insensitive)
SELECT * FROM {table_name}
WHERE title ILIKE $1 OR description ILIKE $1
ORDER BY created_at DESC;
""")

        # Count queries
        queries.append(f"""-- Count total todos
SELECT COUNT(*) as total FROM {table_name};
""")

        # Aggregation by priority
        queries.append(f"""-- Count todos by priority and status
SELECT
    priority,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed_count,
    COUNT(*) FILTER (WHERE completed = false) as active_count
FROM {table_name}
GROUP BY priority
ORDER BY
    CASE priority
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
        ELSE 4
    END;
""")

    return queries


def generate_update_queries(schema: Dict) -> List[str]:
    """Generate UPDATE queries"""
    table_name = schema['table_name']
    queries = []

    # Update single field
    queries.append(f"""-- Update single field by ID
UPDATE {table_name}
SET completed = $1, updated_at = CURRENT_TIMESTAMP
WHERE id = $2
RETURNING *;
""")

    # Update multiple fields
    queries.append(f"""-- Update multiple fields by ID
UPDATE {table_name}
SET title = $1,
    description = $2,
    priority = $3,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $4
RETURNING *;
""")

    # Conditional update
    if table_name == 'todos':
        queries.append(f"""-- Mark all high priority todos as completed
UPDATE {table_name}
SET completed = true, updated_at = CURRENT_TIMESTAMP
WHERE priority = 'high' AND completed = false
RETURNING *;
""")

        # Partial update (only provided fields)
        queries.append(f"""-- Partial update (COALESCE for optional fields)
UPDATE {table_name}
SET title = COALESCE($1, title),
    description = COALESCE($2, description),
    completed = COALESCE($3, completed),
    priority = COALESCE($4, priority),
    updated_at = CURRENT_TIMESTAMP
WHERE id = $5
RETURNING *;
""")

    return queries


def generate_delete_queries(schema: Dict) -> List[str]:
    """Generate DELETE queries"""
    table_name = schema['table_name']
    queries = []

    # Delete by ID
    queries.append(f"""-- Delete by ID
DELETE FROM {table_name}
WHERE id = $1
RETURNING *;
""")

    # Conditional delete
    if table_name == 'todos':
        queries.append(f"""-- Delete completed todos
DELETE FROM {table_name}
WHERE completed = true
RETURNING *;
""")

        queries.append(f"""-- Delete old todos (older than 30 days)
DELETE FROM {table_name}
WHERE created_at < NOW() - INTERVAL '30 days'
RETURNING *;
""")

    # Delete all (with caution)
    queries.append(f"""-- Delete all {table_name} (CAUTION: destructive!)
-- Uncomment to use:
-- DELETE FROM {table_name};
""")

    return queries


def format_as_sql(queries: Dict[str, List[str]]) -> str:
    """Format queries as SQL file"""
    output = []
    output.append("-- Generated SQL Queries")
    output.append(f"-- Generated at: {datetime.now().isoformat()}")
    output.append("-- Neon Postgres Skill")
    output.append("")
    output.append("-- " + "=" * 70)
    output.append("")

    for category, query_list in queries.items():
        output.append(f"-- {category.upper()}")
        output.append("-- " + "-" * 70)
        output.append("")
        for query in query_list:
            output.append(query)
        output.append("")

    return "\n".join(output)


def format_as_markdown(queries: Dict[str, List[str]]) -> str:
    """Format queries as Markdown file"""
    output = []
    output.append("# Generated SQL Queries")
    output.append("")
    output.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    output.append("---")
    output.append("")

    for category, query_list in queries.items():
        output.append(f"## {category.title()}")
        output.append("")
        for i, query in enumerate(query_list, 1):
            # Extract comment as title
            lines = query.strip().split('\n')
            title = lines[0].replace('--', '').strip() if lines else f"Query {i}"

            output.append(f"### {i}. {title}")
            output.append("")
            output.append("```sql")

            # Add query without the first comment line
            query_lines = [line for line in lines[1:] if line.strip()]
            output.append('\n'.join(query_lines))

            output.append("```")
            output.append("")

    return "\n".join(output)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate example SQL queries for Neon Postgres"
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (default: print to stdout)'
    )
    parser.add_argument(
        '--table',
        type=str,
        default='todos',
        help='Table name to generate queries for (default: todos)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['sql', 'markdown'],
        default='sql',
        help='Output format (default: sql)'
    )

    args = parser.parse_args()

    print_header("📝 Generating SQL Queries")

    # Get table schema
    print_info(f"Generating queries for table: {args.table}")
    schema = get_table_schema(args.table)

    # Generate queries by category
    queries = {
        'insert': generate_insert_queries(schema),
        'select': generate_select_queries(schema),
        'update': generate_update_queries(schema),
        'delete': generate_delete_queries(schema),
    }

    # Print summary
    total_queries = sum(len(q) for q in queries.values())
    print_success(f"Generated {len(queries['insert'])} INSERT queries")
    print_success(f"Generated {len(queries['select'])} SELECT queries")
    print_success(f"Generated {len(queries['update'])} UPDATE queries")
    print_success(f"Generated {len(queries['delete'])} DELETE queries")
    print_info(f"Total: {total_queries} queries")

    # Format output
    if args.format == 'sql':
        output = format_as_sql(queries)
    else:
        output = format_as_markdown(queries)

    # Write to file or stdout
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print_success(f"Queries written to: {args.output}")
        except Exception as e:
            print_error(f"Failed to write file: {e}")
            sys.exit(1)
    else:
        print("\n" + "=" * 70)
        print(output)
        print("=" * 70)

    print("\n✨ Next steps:")
    print("  1. Review generated queries")
    print("  2. Integrate queries into your application")
    print("  3. Test queries with your database")
    print("  4. Customize queries for your specific use case")


if __name__ == "__main__":
    main()
