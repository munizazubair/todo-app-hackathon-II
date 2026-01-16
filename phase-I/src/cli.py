"""
Command-line interface functions.

This module handles command parsing, user input/output, and display formatting.
"""

from typing import List, Tuple
from .models import Todo
from .constants import (
    CMD_ADD, CMD_LIST, CMD_COMPLETE, CMD_EDIT, CMD_DELETE,
    CMD_HELP, CMD_EXIT, CMD_QUIT,
    MSG_WELCOME, MSG_EMPTY_LIST, SYMBOL_PENDING, SYMBOL_COMPLETED,
    STATUS_COMPLETED
)


def parse_command(input_string: str) -> Tuple[str, str]:
    """
    Parse user input into command and arguments.

    Args:
        input_string: Raw user input

    Returns:
        Tuple of (command, args)
        - command: The command name (lowercase)
        - args: Remaining text after the command
    """
    input_string = input_string.strip()
    if not input_string:
        return "", ""

    parts = input_string.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    return command, args


def display_welcome() -> None:
    """Display welcome message and available commands."""
    print("\n" + "=" * 60)
    print(f"  {MSG_WELCOME}")
    print("=" * 60)
    print("\nType 'help' to see available commands.")
    print("Type 'exit' or 'quit' to leave the application.\n")


def display_help() -> None:
    """Display help message listing all available commands."""
    print("\n" + "=" * 60)
    print("  AVAILABLE COMMANDS")
    print("=" * 60)
    print()
    print(f"  {CMD_ADD} <title>          Create a new todo")
    print(f"    Example: add Buy groceries")
    print()
    print(f"  {CMD_LIST}                 Display all todos")
    print(f"    Example: list")
    print()
    print(f"  {CMD_COMPLETE} <id>        Mark todo as completed")
    print(f"    Example: complete 1")
    print()
    print(f"  {CMD_EDIT} <id> <title>    Update todo title")
    print(f"    Example: edit 1 Buy milk instead")
    print()
    print(f"  {CMD_DELETE} <id>          Remove a todo")
    print(f"    Example: delete 1")
    print()
    print(f"  {CMD_HELP}                 Show this help message")
    print(f"    Example: help")
    print()
    print(f"  {CMD_EXIT} / {CMD_QUIT}          Exit the application")
    print(f"    Example: exit")
    print()
    print("=" * 60 + "\n")


def display_todos(todos: List[Todo]) -> None:
    """
    Display all todos with formatting.

    Shows todos with their ID, status symbol, and title.
    Handles empty list case.

    Args:
        todos: List of Todo instances to display
    """
    if not todos:
        print(f"\n{MSG_EMPTY_LIST}\n")
        return

    print("\n" + "=" * 60)
    print("  YOUR TODOS")
    print("=" * 60)
    print()

    for todo in todos:
        symbol = SYMBOL_COMPLETED if todo.status == STATUS_COMPLETED else SYMBOL_PENDING
        print(f"  {todo.id}. {symbol} {todo.title}")

    print("\n" + "=" * 60)
    print(f"  Total: {len(todos)} todo(s)")
    print("=" * 60 + "\n")


def display_success(message: str) -> None:
    """
    Display a success message.

    Args:
        message: Success message to display
    """
    print(f"[SUCCESS] {message}")


def display_error(message: str) -> None:
    """
    Display an error message.

    Args:
        message: Error message to display
    """
    print(f"[ERROR] {message}")


def prompt_user() -> str:
    """
    Prompt the user for input.

    Returns:
        User input string
    """
    try:
        return input("> ")
    except EOFError:
        # Handle Ctrl+D gracefully
        return CMD_EXIT
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print()  # New line after ^C
        return CMD_EXIT
