#!/usr/bin/env python3
"""
Migration script to import Phase I todos into Phase II database.

This script reads todos from Phase I JSON format and inserts them
into the Phase II PostgreSQL database using SQLModel.
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlmodel import Session, select
from models.todo import Todo, TodoStatus
from db.database import engine


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_phase_i_todos(source_path: str) -> List[Dict]:
    """
    Read Phase I todos from JSON file.

    Args:
        source_path: Path to JSON file containing Phase I todos

    Returns:
        List of todo dictionaries

    Raises:
        FileNotFoundError: If source file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    logger.info(f"Reading Phase I todos from: {source_path}")

    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    with open(path, 'r') as f:
        todos = json.load(f)

    logger.info(f"Loaded {len(todos)} todos from file")
    return todos


def validate_todo_data(todo_dict: Dict) -> Tuple[bool, str]:
    """
    Validate Phase I todo data before insertion.

    Checks:
    - Required fields (id, title, status) are present
    - Title is not empty
    - Title length <= 500 characters
    - Status is valid (pending or completed)
    - ID is a positive integer

    Args:
        todo_dict: Dictionary containing todo data

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = ['id', 'title', 'status']
    for field in required_fields:
        if field not in todo_dict:
            return False, f"Missing required field: {field}"

    # Validate ID
    try:
        todo_id = int(todo_dict['id'])
        if todo_id <= 0:
            return False, f"Invalid ID: {todo_id} (must be positive)"
    except (ValueError, TypeError):
        return False, f"Invalid ID: {todo_dict['id']} (must be integer)"

    # Validate title
    title = todo_dict['title']
    if not title or not title.strip():
        return False, "Title cannot be empty"

    if len(title) > 500:
        return False, f"Title too long: {len(title)} characters (max 500)"

    # Validate status
    valid_statuses = ['pending', 'completed']
    status = todo_dict['status'].lower()
    if status not in valid_statuses:
        return False, f"Invalid status: {status} (must be 'pending' or 'completed')"

    return True, ""


def insert_todos_to_db(
    todos: List[Dict],
    session: Session,
    skip_duplicates: bool = True
) -> Tuple[int, int, int, List[str]]:
    """
    Insert todos into Phase II database.

    Args:
        todos: List of todo dictionaries from Phase I
        session: Database session
        skip_duplicates: If True, skip todos with existing IDs

    Returns:
        Tuple of (migrated_count, duplicate_count, error_count, error_messages)
    """
    migrated = 0
    duplicates = 0
    errors = 0
    error_messages = []

    for todo_dict in todos:
        try:
            # Validate data
            is_valid, error_msg = validate_todo_data(todo_dict)
            if not is_valid:
                errors += 1
                error_messages.append(f"ID {todo_dict.get('id', '?')}: {error_msg}")
                logger.error(f"Validation failed for todo {todo_dict.get('id', '?')}: {error_msg}")
                continue

            todo_id = int(todo_dict['id'])

            # Check for duplicates
            existing_todo = session.get(Todo, todo_id)
            if existing_todo:
                if skip_duplicates:
                    duplicates += 1
                    logger.info(f"Skipping duplicate ID: {todo_id}")
                    continue
                else:
                    errors += 1
                    error_messages.append(f"ID {todo_id}: Duplicate ID (use --force to overwrite)")
                    logger.error(f"Duplicate ID found: {todo_id}")
                    continue

            # Map Phase I status to Phase II status enum
            status_str = todo_dict['status'].lower()
            status = TodoStatus.PENDING if status_str == 'pending' else TodoStatus.COMPLETED

            # Parse created timestamp if available
            created_at = datetime.utcnow()
            if 'created' in todo_dict:
                try:
                    created_at = datetime.fromisoformat(todo_dict['created'])
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse created timestamp for ID {todo_id}, using current time")

            # Create Phase II todo
            # Note: Phase I doesn't have category/due_date, so they default to None
            new_todo = Todo(
                id=todo_id,
                title=todo_dict['title'].strip(),
                status=status,
                category=None,  # Phase I didn't have categories
                due_date=None,  # Phase I didn't have due dates
                created_at=created_at,
                updated_at=created_at,
                version=1
            )

            session.add(new_todo)
            migrated += 1
            logger.info(f"Migrated todo ID {todo_id}: {todo_dict['title'][:50]}")

        except Exception as e:
            errors += 1
            error_messages.append(f"ID {todo_dict.get('id', '?')}: {str(e)}")
            logger.error(f"Error migrating todo {todo_dict.get('id', '?')}: {e}")

    return migrated, duplicates, errors, error_messages


def generate_migration_report(
    migrated: int,
    duplicates: int,
    errors: int,
    error_messages: List[str],
    dry_run: bool = False
) -> str:
    """
    Generate migration summary report.

    Args:
        migrated: Number of todos successfully migrated
        duplicates: Number of duplicate IDs skipped
        errors: Number of errors encountered
        error_messages: List of error messages
        dry_run: Whether this was a dry run

    Returns:
        Formatted report string
    """
    report = []
    report.append("=" * 60)
    if dry_run:
        report.append("MIGRATION DRY RUN REPORT")
    else:
        report.append("MIGRATION REPORT")
    report.append("=" * 60)
    report.append(f"Total todos processed: {migrated + duplicates + errors}")
    report.append(f"Successfully migrated: {migrated}")
    report.append(f"Duplicates skipped: {duplicates}")
    report.append(f"Errors: {errors}")

    if error_messages:
        report.append("")
        report.append("Error Details:")
        for msg in error_messages[:10]:  # Show first 10 errors
            report.append(f"  - {msg}")
        if len(error_messages) > 10:
            report.append(f"  ... and {len(error_messages) - 10} more errors")

    if dry_run:
        report.append("")
        report.append("NOTE: This was a dry run. No changes were made to the database.")

    report.append("=" * 60)
    return "\n".join(report)


def main():
    """Main migration script entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate Phase I todos to Phase II database"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to Phase I todos JSON file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test migration without inserting into database"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Read Phase I todos
        todos = read_phase_i_todos(args.source)

        if not todos:
            logger.warning("No todos found in source file")
            return 0

        # Create database session
        with Session(engine) as session:
            # Migrate todos
            if args.dry_run:
                logger.info("DRY RUN MODE - No database changes will be made")
                # Validate all todos but don't insert
                migrated = 0
                duplicates = 0
                errors = 0
                error_messages = []

                for todo_dict in todos:
                    is_valid, error_msg = validate_todo_data(todo_dict)
                    if not is_valid:
                        errors += 1
                        error_messages.append(f"ID {todo_dict.get('id', '?')}: {error_msg}")
                    else:
                        todo_id = int(todo_dict['id'])
                        existing = session.get(Todo, todo_id)
                        if existing:
                            duplicates += 1
                        else:
                            migrated += 1
            else:
                migrated, duplicates, errors, error_messages = insert_todos_to_db(
                    todos, session, skip_duplicates=True
                )
                session.commit()
                logger.info("Database changes committed")

            # Generate and print report
            report = generate_migration_report(
                migrated, duplicates, errors, error_messages, args.dry_run
            )
            print(report)

            # Return appropriate exit code
            if errors > 0:
                return 1
            return 0

    except FileNotFoundError as e:
        logger.error(str(e))
        return 1
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON file: {e}")
        return 1
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
