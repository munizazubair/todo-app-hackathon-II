"""
Standalone validation script for Phase I test data.

This script validates the test data structure without requiring
database connections or backend imports.
"""

import json
from pathlib import Path
from typing import Dict, Tuple


def validate_todo_data(todo_dict: Dict) -> Tuple[bool, str]:
    """
    Validate Phase I todo data.

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


def main():
    """Validate test data file."""
    print("=" * 60)
    print("PHASE I TEST DATA VALIDATION")
    print("=" * 60)

    test_file = Path(__file__).parent / "phase_i_todos.json"

    # Load test data
    print(f"\n1. Loading test data from: {test_file.name}")
    try:
        with open(test_file, 'r') as f:
            todos = json.load(f)
        print(f"   [OK] Successfully loaded {len(todos)} todos")
    except Exception as e:
        print(f"   [FAIL] Failed to load: {e}")
        return 1

    # Validate count
    print(f"\n2. Validating todo count")
    if len(todos) == 10:
        print(f"   [OK] Correct count: 10 todos")
    else:
        print(f"   [FAIL] Expected 10 todos, found {len(todos)}")
        return 1

    # Validate each todo
    print(f"\n3. Validating individual todos")
    errors = []
    for i, todo in enumerate(todos, 1):
        is_valid, error_msg = validate_todo_data(todo)
        if not is_valid:
            errors.append(f"Todo {i}: {error_msg}")

    if errors:
        print(f"   [FAIL] Found {len(errors)} validation errors:")
        for error in errors:
            print(f"     - {error}")
        return 1
    else:
        print(f"   [OK] All todos passed validation")

    # Check for duplicate IDs
    print(f"\n4. Checking for duplicate IDs")
    todo_ids = [t['id'] for t in todos]
    if len(todo_ids) != len(set(todo_ids)):
        duplicates = [id for id in todo_ids if todo_ids.count(id) > 1]
        print(f"   [FAIL] Found duplicate IDs: {set(duplicates)}")
        return 1
    else:
        print(f"   [OK] All IDs are unique")

    # Check status distribution
    print(f"\n5. Analyzing status distribution")
    pending_count = sum(1 for t in todos if t['status'] == 'pending')
    completed_count = sum(1 for t in todos if t['status'] == 'completed')
    print(f"   - Pending: {pending_count}")
    print(f"   - Completed: {completed_count}")
    print(f"   [OK] Total: {pending_count + completed_count}")

    # Display sample data
    print(f"\n6. Sample data preview")
    for todo in todos[:3]:
        status_icon = "[X]" if todo['status'] == 'completed' else "[ ]"
        print(f"   {status_icon} ID {todo['id']}: {todo['title'][:50]}")
    if len(todos) > 3:
        print(f"   ... and {len(todos) - 3} more todos")

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print("[OK] All validations passed!")
    print("\nTest data is ready for migration.")
    print("\nTo perform migration (when database is available):")
    print("  cd phase-II")
    print("  python scripts/migrate_from_phase_i.py \\")
    print("    --source scripts/test_data/phase_i_todos.json \\")
    print("    --dry-run")
    print("\n" + "=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
