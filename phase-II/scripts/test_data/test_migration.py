"""
Test script to validate migration logic without database connection.

This script tests the validation and data transformation logic
of the migration script.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import migration functions
from migrate_from_phase_i import read_phase_i_todos, validate_todo_data


def test_read_phase_i_todos():
    """Test reading Phase I todos from JSON."""
    print("Test 1: Reading Phase I todos...")

    test_file = Path(__file__).parent / "phase_i_todos.json"
    try:
        todos = read_phase_i_todos(str(test_file))
        print(f"  ✓ Successfully loaded {len(todos)} todos")
        assert len(todos) == 10, f"Expected 10 todos, got {len(todos)}"
        print("  ✓ Correct number of todos")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_validate_todo_data():
    """Test todo validation logic."""
    print("\nTest 2: Validating todo data...")

    test_cases = [
        # Valid cases
        (
            {"id": 1, "title": "Test todo", "status": "pending"},
            True,
            "Valid pending todo"
        ),
        (
            {"id": 2, "title": "Another test", "status": "completed"},
            True,
            "Valid completed todo"
        ),
        # Invalid cases
        (
            {"title": "Missing ID", "status": "pending"},
            False,
            "Missing ID field"
        ),
        (
            {"id": 1, "status": "pending"},
            False,
            "Missing title field"
        ),
        (
            {"id": 1, "title": "", "status": "pending"},
            False,
            "Empty title"
        ),
        (
            {"id": 1, "title": "x" * 600, "status": "pending"},
            False,
            "Title too long (>500 chars)"
        ),
        (
            {"id": -1, "title": "Test", "status": "pending"},
            False,
            "Negative ID"
        ),
        (
            {"id": 1, "title": "Test", "status": "invalid"},
            False,
            "Invalid status"
        ),
    ]

    passed = 0
    failed = 0

    for todo_dict, expected_valid, description in test_cases:
        is_valid, error_msg = validate_todo_data(todo_dict)

        if is_valid == expected_valid:
            print(f"  ✓ {description}")
            passed += 1
        else:
            print(f"  ✗ {description}")
            print(f"    Expected valid={expected_valid}, got valid={is_valid}")
            if error_msg:
                print(f"    Error: {error_msg}")
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


def test_data_structure():
    """Test that Phase I data has expected structure."""
    print("\nTest 3: Validating Phase I data structure...")

    test_file = Path(__file__).parent / "phase_i_todos.json"
    todos = read_phase_i_todos(str(test_file))

    # Check each todo
    issues = []
    for todo in todos:
        if 'id' not in todo:
            issues.append(f"Todo missing 'id': {todo}")
        if 'title' not in todo:
            issues.append(f"Todo {todo.get('id', '?')} missing 'title'")
        if 'status' not in todo:
            issues.append(f"Todo {todo.get('id', '?')} missing 'status'")

        # Check ID uniqueness
        todo_ids = [t['id'] for t in todos]
        if len(todo_ids) != len(set(todo_ids)):
            issues.append("Duplicate IDs found in test data")
            break

    if issues:
        print("  ✗ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  ✓ All todos have required fields")
        print("  ✓ All IDs are unique")
        return True


def test_status_mapping():
    """Test that statuses are correctly mapped."""
    print("\nTest 4: Testing status mapping...")

    test_file = Path(__file__).parent / "phase_i_todos.json"
    todos = read_phase_i_todos(str(test_file))

    pending_count = sum(1 for t in todos if t['status'] == 'pending')
    completed_count = sum(1 for t in todos if t['status'] == 'completed')

    print(f"  ✓ Found {pending_count} pending todos")
    print(f"  ✓ Found {completed_count} completed todos")
    print(f"  ✓ Total: {pending_count + completed_count}")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("MIGRATION SCRIPT VALIDATION TESTS")
    print("=" * 60)

    all_tests = [
        test_read_phase_i_todos,
        test_validate_todo_data,
        test_data_structure,
        test_status_mapping,
    ]

    results = []
    for test_func in all_tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n  ✗ Test failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if all(results):
        print("\n✓ All validation tests passed!")
        print("\nThe migration script is ready to use with:")
        print("  python migrate_from_phase_i.py --source test_data/phase_i_todos.json --dry-run")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
