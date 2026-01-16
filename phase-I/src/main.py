"""
Main application entry point and command loop.

This module coordinates the CLI, TodoManager, and handles all user commands.
"""

import sys
from .cli import (
    parse_command, display_welcome, display_help, display_todos,
    display_success, display_error, prompt_user
)
from .todo_manager import TodoManager
from .storage import TodoStorage
from .constants import (
    CMD_ADD, CMD_LIST, CMD_COMPLETE, CMD_EDIT, CMD_DELETE,
    CMD_HELP, CMD_EXIT, CMD_QUIT,
    MSG_GOODBYE, MSG_INVALID_COMMAND
)


def handle_add(manager: TodoManager, args: str) -> None:
    """
    Handle the 'add' command.

    Args:
        manager: TodoManager instance
        args: Todo title from user input
    """
    if not args:
        display_error("Title cannot be empty. Usage: add <title>")
        return

    success, message, _ = manager.add_todo(args)
    if success:
        display_success(message)
    else:
        display_error(message)


def handle_list(manager: TodoManager, args: str) -> None:
    """
    Handle the 'list' command.

    Args:
        manager: TodoManager instance
        args: Not used
    """
    todos = manager.list_todos()
    display_todos(todos)


def handle_complete(manager: TodoManager, args: str) -> None:
    """
    Handle the 'complete' command.

    Args:
        manager: TodoManager instance
        args: Todo ID from user input
    """
    if not args:
        display_error("Please provide a todo ID. Usage: complete <id>")
        return

    try:
        todo_id = int(args)
    except ValueError:
        display_error(f"Invalid ID '{args}'. Please provide a number.")
        return

    success, message = manager.complete_todo(todo_id)
    if success:
        display_success(message)
    else:
        display_error(message)


def handle_edit(manager: TodoManager, args: str) -> None:
    """
    Handle the 'edit' command.

    Args:
        manager: TodoManager instance
        args: Todo ID and new title from user input
    """
    if not args:
        display_error("Please provide an ID and new title. Usage: edit <id> <new_title>")
        return

    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        display_error("Please provide both ID and new title. Usage: edit <id> <new_title>")
        return

    try:
        todo_id = int(parts[0])
    except ValueError:
        display_error(f"Invalid ID '{parts[0]}'. Please provide a number.")
        return

    new_title = parts[1]
    success, message = manager.edit_todo(todo_id, new_title)
    if success:
        display_success(message)
    else:
        display_error(message)


def handle_delete(manager: TodoManager, args: str) -> None:
    """
    Handle the 'delete' command.

    Args:
        manager: TodoManager instance
        args: Todo ID from user input
    """
    if not args:
        display_error("Please provide a todo ID. Usage: delete <id>")
        return

    try:
        todo_id = int(args)
    except ValueError:
        display_error(f"Invalid ID '{args}'. Please provide a number.")
        return

    success, message = manager.delete_todo(todo_id)
    if success:
        display_success(message)
    else:
        display_error(message)


def handle_help() -> None:
    """Handle the 'help' command."""
    display_help()


def handle_exit() -> None:
    """Handle the 'exit' or 'quit' command."""
    print(f"\n{MSG_GOODBYE}\n")


def run_app() -> None:
    """
    Run the main application loop.

    Initializes the TodoManager and processes user commands until exit.
    """
    # Initialize storage and manager
    storage = TodoStorage()
    manager = TodoManager(storage)

    # Display welcome message
    display_welcome()

    # Main command loop
    running = True
    while running:
        # Get user input
        user_input = prompt_user()

        # Parse command
        command, args = parse_command(user_input)

        # Handle commands
        if command == CMD_ADD:
            handle_add(manager, args)
        elif command == CMD_LIST:
            handle_list(manager, args)
        elif command == CMD_COMPLETE:
            handle_complete(manager, args)
        elif command == CMD_EDIT:
            handle_edit(manager, args)
        elif command == CMD_DELETE:
            handle_delete(manager, args)
        elif command == CMD_HELP:
            handle_help()
        elif command in (CMD_EXIT, CMD_QUIT):
            handle_exit()
            running = False
        elif command == "":
            # Empty input, just continue
            continue
        else:
            display_error(f"{MSG_INVALID_COMMAND}")


def main() -> int:
    """
    Application entry point with error handling.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        run_app()
        return 0
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        print("The application has encountered an error and must exit.\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
