"""
Constants and configuration for the Todo application.

This module defines all constant values used throughout the application,
including validation limits, status values, and command names.
"""

# Title validation
MAX_TITLE_LENGTH = 500

# Todo status values
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"

# Command names
CMD_ADD = "add"
CMD_LIST = "list"
CMD_COMPLETE = "complete"
CMD_EDIT = "edit"
CMD_DELETE = "delete"
CMD_HELP = "help"
CMD_EXIT = "exit"
CMD_QUIT = "quit"

# Display symbols
SYMBOL_PENDING = "[ ]"
SYMBOL_COMPLETED = "[X]"

# Messages
MSG_WELCOME = "Welcome to Todo App - Phase I"
MSG_GOODBYE = "Goodbye! Your todos were stored in memory only."
MSG_EMPTY_LIST = "No todos yet. Use 'add <title>' to create your first todo!"
MSG_INVALID_COMMAND = "Invalid command. Type 'help' for available commands."
