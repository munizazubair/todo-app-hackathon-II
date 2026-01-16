#!/usr/bin/env python3
"""
FastAPI Project Structure Validator

Validates that a FastAPI project follows the Phase II structure requirements.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def check_exists(path: Path, item_type: str = "file") -> bool:
    """Check if a file or directory exists."""
    if item_type == "file":
        return path.is_file()
    else:
        return path.is_dir()


def validate_required_files(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that required files exist."""
    required_files = [
        "app/main.py",
        "app/__init__.py",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/api/v1/endpoints/__init__.py",
        "app/models/__init__.py",
        "app/schemas/__init__.py",
        "app/db/__init__.py",
        "app/db/session.py",
        "requirements.txt",
        ".env.example",
    ]

    passed = []
    failed = []

    for file_path in required_files:
        full_path = base_path / file_path
        if check_exists(full_path, "file"):
            passed.append(file_path)
        else:
            failed.append(file_path)

    return passed, failed


def validate_directory_structure(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that required directories exist."""
    required_dirs = [
        "app",
        "app/core",
        "app/api",
        "app/api/v1",
        "app/api/v1/endpoints",
        "app/models",
        "app/schemas",
        "app/db",
        "tests",
        "alembic",
    ]

    passed = []
    failed = []

    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if check_exists(full_path, "dir"):
            passed.append(dir_path)
        else:
            failed.append(dir_path)

    return passed, failed


def validate_dependencies(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that required dependencies are in requirements.txt."""
    req_file = base_path / "requirements.txt"

    if not req_file.exists():
        return [], ["requirements.txt not found"]

    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlmodel",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "alembic",
    ]

    content = req_file.read_text().lower()

    passed = []
    failed = []

    for package in required_packages:
        if package in content:
            passed.append(package)
        else:
            failed.append(package)

    return passed, failed


def validate_config_file(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that config.py has required settings."""
    config_file = base_path / "app" / "core" / "config.py"

    if not config_file.exists():
        return [], ["config.py not found"]

    required_settings = [
        "app_name",
        "database_url",
        "cors_origins",
    ]

    content = config_file.read_text()

    passed = []
    failed = []

    for setting in required_settings:
        if setting in content:
            passed.append(setting)
        else:
            failed.append(setting)

    return passed, failed


def validate_main_file(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that main.py has required components."""
    main_file = base_path / "app" / "main.py"

    if not main_file.exists():
        return [], ["main.py not found"]

    required_components = [
        "FastAPI",
        "CORSMiddleware",
        "app = FastAPI",
        "add_middleware",
    ]

    content = main_file.read_text()

    passed = []
    failed = []

    for component in required_components:
        if component in content:
            passed.append(component)
        else:
            failed.append(component)

    return passed, failed


def validate_env_example(base_path: Path) -> Tuple[List[str], List[str]]:
    """Validate that .env.example has required variables."""
    env_file = base_path / ".env.example"

    if not env_file.exists():
        return [], [".env.example not found"]

    required_vars = [
        "APP_NAME",
        "DATABASE_URL",
        "CORS_ORIGINS",
    ]

    content = env_file.read_text()

    passed = []
    failed = []

    for var in required_vars:
        if var in content:
            passed.append(var)
        else:
            failed.append(var)

    return passed, failed


def print_section_result(title: str, passed: List[str], failed: List[str]) -> bool:
    """Print validation results for a section."""
    total = len(passed) + len(failed)

    if failed:
        status = f"{Colors.YELLOW}⚠{Colors.ENDC}"
        status_text = f"{len(passed)}/{total}"
    else:
        status = f"{Colors.GREEN}✓{Colors.ENDC}"
        status_text = f"{len(passed)}/{total}"

    print(f"\n{status} {Colors.BOLD}{title}{Colors.ENDC} ({status_text})")

    if passed and not failed:
        print(f"  {Colors.GREEN}All checks passed!{Colors.ENDC}")
    else:
        if failed:
            print(f"\n  {Colors.RED}Missing:{Colors.ENDC}")
            for item in failed:
                print(f"    • {item}")

        if passed and len(passed) <= 5:
            print(f"\n  {Colors.GREEN}Found:{Colors.ENDC}")
            for item in passed[:5]:
                print(f"    • {item}")
            if len(passed) > 5:
                print(f"    ... and {len(passed) - 5} more")

    return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate FastAPI project structure"
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Project directory to validate (default: current directory)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Get absolute path
    base_path = Path(args.project_dir).resolve()

    if not base_path.exists():
        print(f"{Colors.RED}Error: Directory does not exist: {base_path}{Colors.ENDC}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}FastAPI Project Structure Validator{Colors.ENDC}")
    print(f"Validating: {Colors.BLUE}{base_path}{Colors.ENDC}")
    print("=" * 60)

    # Run all validations
    validations = [
        ("Directory Structure", validate_directory_structure(base_path)),
        ("Required Files", validate_required_files(base_path)),
        ("Dependencies (requirements.txt)", validate_dependencies(base_path)),
        ("Configuration (config.py)", validate_config_file(base_path)),
        ("Main Application (main.py)", validate_main_file(base_path)),
        ("Environment Variables (.env.example)", validate_env_example(base_path)),
    ]

    all_passed = True

    for title, (passed, failed) in validations:
        section_passed = print_section_result(title, passed, failed)
        if not section_passed:
            all_passed = False

    # Print summary
    print("\n" + "=" * 60)

    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All validations passed!{Colors.ENDC}")
        print(f"\nYour FastAPI project structure is correctly set up.")
        print(f"\n{Colors.BLUE}Next steps:{Colors.ENDC}")
        print(f"  1. Create virtual environment: python -m venv venv")
        print(f"  2. Activate: source venv/bin/activate  # Windows: venv\\Scripts\\activate")
        print(f"  3. Install dependencies: pip install -r requirements.txt")
        print(f"  4. Configure .env: cp .env.example .env")
        print(f"  5. Run server: uvicorn app.main:app --reload\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some validations failed{Colors.ENDC}")
        print(f"\nPlease fix the issues above and run validation again.")
        print(f"\n{Colors.BLUE}Tip:{Colors.ENDC} Use the FastAPISkill create_project.py script to generate a complete project structure.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
