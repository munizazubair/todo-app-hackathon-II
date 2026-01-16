"""
Error messages and constants migrated from Phase I.

These messages maintain consistency with Phase I validation rules.
"""

# Success Messages
MSG_TODO_CREATED = "Todo created successfully"
MSG_TODO_UPDATED = "Todo updated successfully"
MSG_TODO_DELETED = "Todo deleted successfully"
MSG_TODO_COMPLETED = "Todo marked as completed"
MSG_TODO_UNCOMPLETED = "Todo marked as pending"

# Error Messages - Validation
ERR_TITLE_EMPTY = "Title cannot be empty"
ERR_TITLE_TOO_LONG = "Title cannot exceed 500 characters"
ERR_TITLE_INVALID = "Title must be a non-empty string"
ERR_CATEGORY_TOO_LONG = "Category cannot exceed 50 characters"
ERR_DUE_DATE_INVALID = "Due date must be in YYYY-MM-DD format"
ERR_STATUS_INVALID = "Status must be 'pending' or 'completed'"

# Error Messages - Not Found
ERR_TODO_NOT_FOUND = "Todo with ID {id} does not exist"

# Error Messages - Conflict
ERR_VERSION_CONFLICT = "Conflict: Todo was modified by another process. Expected version {expected} but found version {actual}. Please refresh and retry."

# Error Messages - General
ERR_INTERNAL_SERVER = "An internal server error occurred"
ERR_DATABASE_ERROR = "Database error occurred"
ERR_VALIDATION_ERROR = "Validation error"

# Validation Constants (from Phase I)
MAX_TITLE_LENGTH = 500
MAX_CATEGORY_LENGTH = 50
VALID_STATUSES = ["pending", "completed"]
