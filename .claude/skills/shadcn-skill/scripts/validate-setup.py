#!/usr/bin/env python3
"""
shadcn/ui Setup Validator

Validates that shadcn/ui is properly configured in a Next.js project.
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


def check_dependencies(base_path: Path) -> Tuple[bool, List[str]]:
    """Check if required npm packages are installed."""
    package_json = base_path / "package.json"

    if not package_json.exists():
        return False, ["package.json not found"]

    try:
        import json
        with open(package_json, 'r') as f:
            data = json.load(f)

        dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

        required_packages = {
            'class-variance-authority': 'CVA for component variants',
            'clsx': 'Conditional className utility',
            'tailwind-merge': 'Tailwind class merging',
        }

        radix_packages = {
            '@radix-ui/react-slot': 'Slot primitive',
            '@radix-ui/react-dialog': 'Dialog/Modal primitive',
        }

        missing = []
        for package, description in required_packages.items():
            if package not in dependencies:
                missing.append(f"{package} ({description})")

        radix_missing = []
        for package in radix_packages.keys():
            if package not in dependencies:
                radix_missing.append(package)

        if missing:
            return False, missing

        if len(radix_missing) == len(radix_packages):
            return False, ["No Radix UI packages found - install at least @radix-ui/react-slot and @radix-ui/react-dialog"]

        return True, []

    except Exception as e:
        return False, [f"Error reading package.json: {e}"]


def check_utils_file(base_path: Path) -> Tuple[bool, Path]:
    """Check if lib/utils.ts exists with cn() function."""
    possible_paths = [
        base_path / "lib" / "utils.ts",
        base_path / "app" / "lib" / "utils.ts",
        base_path / "src" / "lib" / "utils.ts",
    ]

    for utils_path in possible_paths:
        if utils_path.exists():
            try:
                content = utils_path.read_text()
                if 'cn' in content and 'twMerge' in content and 'clsx' in content:
                    return True, utils_path
            except Exception:
                continue

    return False, possible_paths[0]


def check_tailwind_config(base_path: Path) -> Tuple[bool, str]:
    """Check if tailwind.config has shadcn/ui colors."""
    ts_config = base_path / "tailwind.config.ts"
    js_config = base_path / "tailwind.config.js"

    config_file = ts_config if ts_config.exists() else js_config if js_config.exists() else None

    if not config_file:
        return False, "tailwind.config.ts/js not found"

    try:
        content = config_file.read_text()

        # Check for shadcn/ui color variables
        shadcn_indicators = [
            'hsl(var(--background))',
            'hsl(var(--foreground))',
            'hsl(var(--primary))',
            '--border',
            '--input',
        ]

        found = any(indicator in content for indicator in shadcn_indicators)

        if found:
            return True, str(config_file.name)
        else:
            return False, f"{config_file.name} exists but missing shadcn/ui color configuration"

    except Exception as e:
        return False, f"Error reading {config_file.name}: {e}"


def check_globals_css(base_path: Path) -> Tuple[bool, Path]:
    """Check if globals.css has shadcn/ui CSS variables."""
    possible_paths = [
        base_path / "app" / "globals.css",
        base_path / "src" / "app" / "globals.css",
        base_path / "styles" / "globals.css",
    ]

    for globals_path in possible_paths:
        if globals_path.exists():
            try:
                content = globals_path.read_text()

                # Check for shadcn/ui CSS variables
                required_vars = ['--background', '--foreground', '--primary', '--border']

                if all(var in content for var in required_vars):
                    return True, globals_path
            except Exception:
                continue

    return False, possible_paths[0]


def check_components(base_path: Path) -> Tuple[int, List[str]]:
    """Check for shadcn/ui components."""
    possible_component_dirs = [
        base_path / "components",
        base_path / "app" / "components",
        base_path / "src" / "components",
    ]

    components_to_check = ['Button.tsx', 'Card.tsx', 'Input.tsx', 'Modal.tsx', 'Navbar.tsx']

    found_components = []

    for comp_dir in possible_component_dirs:
        if comp_dir.exists():
            for component in components_to_check:
                if (comp_dir / component).exists():
                    found_components.append(component)

    return len(found_components), components_to_check


def check_layout(base_path: Path) -> bool:
    """Check if layout.tsx exists."""
    possible_layouts = [
        base_path / "app" / "layout.tsx",
        base_path / "src" / "app" / "layout.tsx",
    ]

    for layout_path in possible_layouts:
        if layout_path.exists():
            return True

    return False


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
        description="Validate shadcn/ui setup in Next.js project"
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Project directory to validate (default: current directory)"
    )

    args = parser.parse_args()

    # Get absolute path
    base_path = Path(args.project_dir).resolve()

    if not base_path.exists():
        print(f"{Colors.RED}Error: Directory does not exist: {base_path}{Colors.ENDC}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}shadcn/ui Setup Validator{Colors.ENDC}")
    print(f"Validating: {Colors.BLUE}{base_path}{Colors.ENDC}")
    print("=" * 60)
    print()

    all_passed = True

    # Check 1: Dependencies
    deps_ok, missing_deps = check_dependencies(base_path)
    print_check(
        "Required dependencies installed",
        deps_ok,
        f"Missing: {', '.join(missing_deps)}" if not deps_ok else ""
    )
    if not deps_ok and missing_deps:
        print(f"  {Colors.BLUE}Run: npm install class-variance-authority clsx tailwind-merge{Colors.ENDC}")
        print(f"  {Colors.BLUE}Run: npm install @radix-ui/react-slot @radix-ui/react-dialog{Colors.ENDC}")
        all_passed = False

    # Check 2: Utils file
    utils_ok, utils_path = check_utils_file(base_path)
    print_check(
        "lib/utils.ts exists with cn() function",
        utils_ok,
        f"Create {utils_path} with cn() utility" if not utils_ok else ""
    )
    if not utils_ok:
        all_passed = False

    # Check 3: Tailwind config
    tailwind_ok, tailwind_msg = check_tailwind_config(base_path)
    print_check(
        "Tailwind config has shadcn/ui colors",
        tailwind_ok,
        tailwind_msg if not tailwind_ok else ""
    )
    if not tailwind_ok:
        all_passed = False

    # Check 4: globals.css
    globals_ok, globals_path = check_globals_css(base_path)
    print_check(
        "globals.css has shadcn/ui CSS variables",
        globals_ok,
        f"Update {globals_path} with shadcn/ui CSS variables" if not globals_ok else ""
    )
    if not globals_ok:
        all_passed = False

    # Check 5: Components
    found_count, components_list = check_components(base_path)
    components_ok = found_count > 0
    print_check(
        f"shadcn/ui components ({found_count}/{len(components_list)} found)",
        components_ok,
        "No components found - run generate-components.py" if not components_ok else ""
    )
    if not components_ok:
        all_passed = False

    # Check 6: Layout
    layout_ok = check_layout(base_path)
    print_check(
        "layout.tsx exists",
        layout_ok,
        "Create app/layout.tsx" if not layout_ok else ""
    )
    if not layout_ok:
        all_passed = False

    # Print summary
    print()
    print("=" * 60)

    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed!{Colors.ENDC}")
        print(f"\nYour shadcn/ui setup is correctly configured.")
        print(f"\n{Colors.BLUE}Next steps:{Colors.ENDC}")
        print(f"  1. Start development server: npm run dev")
        print(f"  2. Use shadcn/ui components in your pages")
        print(f"  3. Check documentation: .claude/skills/shadcn-skill/reference.md\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some checks failed{Colors.ENDC}")
        print(f"\nPlease fix the issues above and run validation again.")
        print(f"\n{Colors.BLUE}Quick fix:{Colors.ENDC}")
        print(f"  python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir {base_path}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
