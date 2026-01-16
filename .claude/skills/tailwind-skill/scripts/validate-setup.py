#!/usr/bin/env python3
"""
Tailwind CSS Setup Validator

Validates that Tailwind CSS is properly configured in a Next.js project.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, List


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def check_file_exists(file_path: Path) -> bool:
    """Check if a file exists."""
    return file_path.is_file()


def check_tailwind_config(base_path: Path) -> Tuple[bool, str]:
    """Check if tailwind.config.ts or tailwind.config.js exists."""
    ts_config = base_path / "tailwind.config.ts"
    js_config = base_path / "tailwind.config.js"

    if ts_config.exists():
        return True, "tailwind.config.ts"
    elif js_config.exists():
        return True, "tailwind.config.js"
    else:
        return False, "tailwind.config.ts or tailwind.config.js"


def check_globals_css(base_path: Path) -> Tuple[bool, Path]:
    """Check if globals.css exists."""
    # Check in app/ directory
    app_globals = base_path / "app" / "globals.css"
    if app_globals.exists():
        return True, app_globals

    # Check in src/app/ directory
    src_app_globals = base_path / "src" / "app" / "globals.css"
    if src_app_globals.exists():
        return True, src_app_globals

    # Check in styles/ directory (older Next.js projects)
    styles_globals = base_path / "styles" / "globals.css"
    if styles_globals.exists():
        return True, styles_globals

    return False, app_globals


def check_tailwind_directives(globals_css_path: Path) -> Tuple[bool, List[str]]:
    """Check if globals.css contains Tailwind directives."""
    required_directives = [
        "@tailwind base",
        "@tailwind components",
        "@tailwind utilities"
    ]

    try:
        content = globals_css_path.read_text()
        missing_directives = []

        for directive in required_directives:
            if directive not in content:
                missing_directives.append(directive)

        return len(missing_directives) == 0, missing_directives
    except Exception as e:
        return False, [f"Error reading file: {e}"]


def check_globals_import(base_path: Path, globals_css_path: Path) -> bool:
    """Check if globals.css is imported in layout.tsx."""
    # Determine the relative path to globals.css
    layout_files = [
        base_path / "app" / "layout.tsx",
        base_path / "app" / "layout.js",
        base_path / "src" / "app" / "layout.tsx",
        base_path / "src" / "app" / "layout.js",
    ]

    for layout_file in layout_files:
        if not layout_file.exists():
            continue

        try:
            content = layout_file.read_text()

            # Check for various import patterns
            import_patterns = [
                "import './globals.css'",
                'import "./globals.css"',
                "import '../globals.css'",
                'import "../globals.css"',
                "import '@/app/globals.css'",
                'import "@/app/globals.css"',
                "import '@/styles/globals.css'",
                'import "@/styles/globals.css"',
            ]

            for pattern in import_patterns:
                if pattern in content:
                    return True

        except Exception:
            continue

    return False


def check_postcss_config(base_path: Path) -> bool:
    """Check if postcss.config.js exists."""
    postcss_js = base_path / "postcss.config.js"
    postcss_mjs = base_path / "postcss.config.mjs"

    return postcss_js.exists() or postcss_mjs.exists()


def check_package_json(base_path: Path) -> Tuple[bool, List[str]]:
    """Check if tailwindcss is in package.json dependencies."""
    package_json = base_path / "package.json"

    if not package_json.exists():
        return False, ["package.json not found"]

    try:
        import json
        with open(package_json, 'r') as f:
            data = json.load(f)

        dev_dependencies = data.get('devDependencies', {})
        dependencies = data.get('dependencies', {})

        required_packages = ['tailwindcss', 'postcss', 'autoprefixer']
        missing_packages = []

        for package in required_packages:
            if package not in dev_dependencies and package not in dependencies:
                missing_packages.append(package)

        return len(missing_packages) == 0, missing_packages

    except Exception as e:
        return False, [f"Error reading package.json: {e}"]


def print_check(check_name: str, passed: bool, details: str = ""):
    """Print a validation check result."""
    if passed:
        print(f"{Colors.GREEN}✓{Colors.ENDC} {check_name}")
    else:
        print(f"{Colors.RED}✗{Colors.ENDC} {check_name}")
        if details:
            print(f"  {Colors.YELLOW}{details}{Colors.ENDC}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Tailwind CSS setup in Next.js project"
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

    print(f"\n{Colors.BOLD}Tailwind CSS Setup Validator{Colors.ENDC}")
    print(f"Validating: {Colors.BLUE}{base_path}{Colors.ENDC}")
    print("=" * 60)
    print()

    all_passed = True

    # Check 1: Tailwind config file
    config_exists, config_name = check_tailwind_config(base_path)
    print_check(
        f"{config_name} exists",
        config_exists,
        "Run: npx tailwindcss init -p" if not config_exists else ""
    )
    if not config_exists:
        all_passed = False

    # Check 2: PostCSS config
    postcss_exists = check_postcss_config(base_path)
    print_check(
        "postcss.config.js exists",
        postcss_exists,
        "Run: npx tailwindcss init -p" if not postcss_exists else ""
    )
    if not postcss_exists:
        all_passed = False

    # Check 3: globals.css exists
    globals_exists, globals_path = check_globals_css(base_path)
    print_check(
        "globals.css exists",
        globals_exists,
        f"Create {globals_path}" if not globals_exists else ""
    )
    if not globals_exists:
        all_passed = False

    # Check 4: Tailwind directives in globals.css
    if globals_exists:
        directives_ok, missing = check_tailwind_directives(globals_path)
        print_check(
            "globals.css contains @tailwind directives",
            directives_ok,
            f"Missing: {', '.join(missing)}" if not directives_ok else ""
        )
        if not directives_ok:
            all_passed = False
    else:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Skipping @tailwind directives check (globals.css not found)")

    # Check 5: globals.css imported in layout
    if globals_exists:
        import_ok = check_globals_import(base_path, globals_path)
        print_check(
            "globals.css imported in layout.tsx",
            import_ok,
            "Add: import './globals.css' to your layout.tsx" if not import_ok else ""
        )
        if not import_ok:
            all_passed = False
    else:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Skipping globals.css import check (globals.css not found)")

    # Check 6: Package dependencies
    packages_ok, missing_packages = check_package_json(base_path)
    print_check(
        "Required packages installed",
        packages_ok,
        f"Missing: {', '.join(missing_packages)}" if not packages_ok else ""
    )
    if not packages_ok and missing_packages:
        print(f"  {Colors.BLUE}Run: npm install -D {' '.join(missing_packages)}{Colors.ENDC}")
        all_passed = False

    # Print summary
    print()
    print("=" * 60)

    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed!{Colors.ENDC}")
        print(f"\nYour Tailwind CSS setup is correctly configured.")
        print(f"\n{Colors.BLUE}Next steps:{Colors.ENDC}")
        print(f"  1. Start development server: npm run dev")
        print(f"  2. Use Tailwind classes in your components")
        print(f"  3. Check documentation: .claude/skills/tailwind-skill/reference.md\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some checks failed{Colors.ENDC}")
        print(f"\nPlease fix the issues above and run validation again.")
        print(f"\n{Colors.BLUE}Quick fix:{Colors.ENDC}")
        print(f"  python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir {base_path}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
