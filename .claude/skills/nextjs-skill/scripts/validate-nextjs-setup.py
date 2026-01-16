#!/usr/bin/env python3
"""
Validate Next.js project setup for Phase II.

This script checks that the Next.js frontend meets all Phase II requirements
from specs/002-phase-ii-web-app/spec.md.

Usage:
    python scripts/validate-nextjs-setup.py [frontend_dir]

    If frontend_dir is not provided, defaults to 'phase-II/frontend'.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple


class Color:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def check_required_files(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check for required configuration files."""
    errors = []
    warnings = []

    required_files = {
        'package.json': 'Node.js package configuration',
        'next.config.js': 'Next.js configuration (FR-001)',
        'tsconfig.json': 'TypeScript configuration (FR-002)',
        'tailwind.config.ts': 'Tailwind CSS configuration (FR-003)',
        '.env.local': 'Environment variables (optional, can be .env.example)',
    }

    for file, description in required_files.items():
        file_path = base_dir / file
        if not file_path.exists():
            if file == '.env.local':
                # Check for .env.example as alternative
                if not (base_dir / '.env.example').exists():
                    warnings.append(f"Missing {file} ({description})")
            else:
                errors.append(f"Missing {file} ({description})")

    return errors, warnings


def check_directory_structure(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check for required directories from spec.md file structure."""
    errors = []
    warnings = []

    required_dirs = {
        'app': 'Next.js App Router directory (FR-001)',
        'components': 'React components directory',
        'lib': 'Utility functions directory',
        'types': 'TypeScript type definitions',
        'public': 'Static assets directory',
    }

    for dir_name, description in required_dirs.items():
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            errors.append(f"Missing directory '{dir_name}' ({description})")
        elif not dir_path.is_dir():
            errors.append(f"'{dir_name}' exists but is not a directory")

    return errors, warnings


def check_component_files(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check for required component files from spec.md."""
    errors = []
    warnings = []

    components_dir = base_dir / 'components'
    if not components_dir.exists():
        return errors, warnings

    required_components = [
        'TodoList.tsx',      # FR-004
        'TodoItem.tsx',      # FR-004
        'TodoForm.tsx',      # FR-005
        'FilterBar.tsx',     # FR-010
        'SearchBar.tsx',     # FR-011
    ]

    for component in required_components:
        component_path = components_dir / component
        if not component_path.exists():
            warnings.append(f"Missing component: components/{component}")

    return errors, warnings


def check_lib_files(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check for required library files."""
    errors = []
    warnings = []

    lib_dir = base_dir / 'lib'
    if not lib_dir.exists():
        return errors, warnings

    required_lib_files = {
        'api.ts': 'API client for FastAPI backend',
        'constants.ts': 'Constants migrated from Phase I',
        'validation.ts': 'Client-side validation (FR-006)',
    }

    for file, description in required_lib_files.items():
        file_path = lib_dir / file
        if not file_path.exists():
            warnings.append(f"Missing lib/{file} ({description})")

    return errors, warnings


def check_type_definitions(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check for TypeScript type definitions."""
    errors = []
    warnings = []

    types_dir = base_dir / 'types'
    if not types_dir.exists():
        return errors, warnings

    todo_types_path = types_dir / 'todo.ts'
    if not todo_types_path.exists():
        warnings.append("Missing types/todo.ts (TypeScript interfaces for Todo)")

    return errors, warnings


def check_package_json(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Validate package.json dependencies."""
    errors = []
    warnings = []

    pkg_path = base_dir / 'package.json'
    if not pkg_path.exists():
        return errors, warnings

    try:
        with open(pkg_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid package.json: {e}")
        return errors, warnings

    # Check required dependencies
    deps = pkg.get('dependencies', {})
    dev_deps = pkg.get('devDependencies', {})
    all_deps = {**deps, **dev_deps}

    required_deps = {
        'next': 'Next.js 14+ (FR-001)',
        'react': 'React 18+ (FR-002)',
        'typescript': 'TypeScript support (FR-002)',
        'tailwindcss': 'Tailwind CSS (FR-003)',
        'axios': 'HTTP client for API calls',
    }

    for dep, description in required_deps.items():
        if dep not in all_deps:
            errors.append(f"Missing dependency '{dep}' ({description})")

    # Check Next.js version
    if 'next' in all_deps:
        version = all_deps['next'].lstrip('^~>=')
        major_version = int(version.split('.')[0]) if version[0].isdigit() else 0
        if major_version < 14:
            warnings.append(f"Next.js version {version} is below required 14+ (FR-001)")

    # Check React version
    if 'react' in all_deps:
        version = all_deps['react'].lstrip('^~>=')
        major_version = int(version.split('.')[0]) if version[0].isdigit() else 0
        if major_version < 18:
            errors.append(f"React version {version} is below required 18+ (FR-002)")

    return errors, warnings


def check_app_router_structure(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check App Router structure."""
    errors = []
    warnings = []

    app_dir = base_dir / 'app'
    if not app_dir.exists():
        return errors, warnings

    # Check required App Router files
    required_app_files = {
        'layout.tsx': 'Root layout (required for App Router)',
        'page.tsx': 'Homepage with todo list',
    }

    for file, description in required_app_files.items():
        file_path = app_dir / file
        if not file_path.exists():
            errors.append(f"Missing app/{file} ({description})")

    # Check for dashboard page (optional but in spec)
    dashboard_page = app_dir / 'dashboard' / 'page.tsx'
    if not dashboard_page.exists():
        warnings.append("Missing app/dashboard/page.tsx (FR-012: Dashboard page)")

    return errors, warnings


def check_environment_variables(base_dir: Path) -> Tuple[List[str], List[str]]:
    """Check environment variable configuration."""
    errors = []
    warnings = []

    env_file = base_dir / '.env.local'
    env_example = base_dir / '.env.example'

    if not env_file.exists() and not env_example.exists():
        warnings.append("No .env.local or .env.example found. API URL configuration needed.")
        return errors, warnings

    # Check for NEXT_PUBLIC_API_URL
    env_to_check = env_file if env_file.exists() else env_example
    try:
        with open(env_to_check, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'NEXT_PUBLIC_API_URL' not in content:
                warnings.append("Missing NEXT_PUBLIC_API_URL in environment file")
    except Exception as e:
        warnings.append(f"Could not read environment file: {e}")

    return errors, warnings


def print_report(errors: List[str], warnings: List[str]) -> None:
    """Print validation report."""
    print(f"\n{Color.BOLD}Next.js Setup Validation Report{Color.RESET}")
    print("=" * 60)

    if errors:
        print(f"\n{Color.RED}{Color.BOLD}ERRORS ({len(errors)}):{Color.RESET}")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {Color.RED}✗{Color.RESET} {error}")

    if warnings:
        print(f"\n{Color.YELLOW}{Color.BOLD}WARNINGS ({len(warnings)}):{Color.RESET}")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {Color.YELLOW}⚠{Color.RESET} {warning}")

    if not errors and not warnings:
        print(f"\n{Color.GREEN}✓ All checks passed! Next.js setup is valid.{Color.RESET}")
    elif not errors:
        print(f"\n{Color.GREEN}✓ No errors found. Address warnings for complete setup.{Color.RESET}")
    else:
        print(f"\n{Color.RED}✗ Validation failed. Fix errors before proceeding.{Color.RESET}")

    print("=" * 60)


def validate_nextjs_setup(frontend_dir: str = 'phase-II/frontend') -> int:
    """
    Main validation function.

    Returns:
        0 if validation passes (no errors)
        1 if validation fails (has errors)
    """
    base_dir = Path(frontend_dir)

    if not base_dir.exists():
        print(f"{Color.RED}Error: Directory '{frontend_dir}' does not exist.{Color.RESET}")
        print(f"Usage: python {sys.argv[0]} [frontend_dir]")
        return 1

    print(f"{Color.BLUE}Validating Next.js setup at: {base_dir.absolute()}{Color.RESET}\n")

    all_errors = []
    all_warnings = []

    # Run all checks
    checks = [
        ("Required Files", check_required_files),
        ("Directory Structure", check_directory_structure),
        ("Component Files", check_component_files),
        ("Library Files", check_lib_files),
        ("Type Definitions", check_type_definitions),
        ("package.json", check_package_json),
        ("App Router Structure", check_app_router_structure),
        ("Environment Variables", check_environment_variables),
    ]

    for check_name, check_func in checks:
        print(f"Checking {check_name}...", end=' ')
        errors, warnings = check_func(base_dir)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        if errors:
            print(f"{Color.RED}✗{Color.RESET}")
        elif warnings:
            print(f"{Color.YELLOW}⚠{Color.RESET}")
        else:
            print(f"{Color.GREEN}✓{Color.RESET}")

    # Print report
    print_report(all_errors, all_warnings)

    # Return exit code
    return 1 if all_errors else 0


if __name__ == '__main__':
    frontend_dir = sys.argv[1] if len(sys.argv) > 1 else 'phase-II/frontend'
    sys.exit(validate_nextjs_setup(frontend_dir))
