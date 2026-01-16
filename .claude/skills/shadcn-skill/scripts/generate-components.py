#!/usr/bin/env python3
"""
shadcn/ui Component Generator

Generates shadcn/ui components, hooks, and configuration files for Next.js projects.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def get_skill_template_dir() -> Path:
    """Get the path to the skill's template directory."""
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent / "template"

    if not template_dir.exists():
        print(f"{Colors.RED}Error: Template directory not found: {template_dir}{Colors.ENDC}")
        sys.exit(1)

    return template_dir


def create_directories(base_path: Path) -> None:
    """Create necessary directories."""
    directories = [
        base_path / "components",
        base_path / "lib",
        base_path / "hooks",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created directory: {directory.relative_to(base_path.parent)}")


def copy_component(template_dir: Path, target_dir: Path, component_name: str, force: bool = False) -> bool:
    """Copy a component file from template to target directory."""
    source_file = template_dir / "components" / f"{component_name}.tsx"
    target_file = target_dir / "components" / f"{component_name}.tsx"

    if not source_file.exists():
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Template not found: {component_name}.tsx")
        return False

    if target_file.exists() and not force:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} {component_name}.tsx already exists (use --force to overwrite)")
        return False

    try:
        shutil.copy2(source_file, target_file)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created {component_name}.tsx")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create {component_name}.tsx: {e}")
        return False


def copy_hook(template_dir: Path, target_dir: Path, hook_name: str, force: bool = False) -> bool:
    """Copy a hook file from template to target directory."""
    source_file = template_dir / "hooks" / f"{hook_name}.ts"
    target_file = target_dir / "hooks" / f"{hook_name}.ts"

    if not source_file.exists():
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Template not found: {hook_name}.ts")
        return False

    if target_file.exists() and not force:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} {hook_name}.ts already exists (use --force to overwrite)")
        return False

    try:
        shutil.copy2(source_file, target_file)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created {hook_name}.ts")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create {hook_name}.ts: {e}")
        return False


def create_utils_file(target_dir: Path, force: bool = False) -> bool:
    """Create lib/utils.ts with cn() function."""
    utils_file = target_dir / "lib" / "utils.ts"

    if utils_file.exists() and not force:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} lib/utils.ts already exists (use --force to overwrite)")
        return False

    utils_content = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''

    try:
        utils_file.write_text(utils_content)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created lib/utils.ts")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create lib/utils.ts: {e}")
        return False


def copy_layout(template_dir: Path, target_dir: Path, force: bool = False) -> bool:
    """Copy layout.tsx template."""
    source_file = template_dir / "layout.tsx"
    target_file = target_dir / "layout.tsx"

    if not source_file.exists():
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Template not found: layout.tsx")
        return False

    if target_file.exists() and not force:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} layout.tsx already exists (use --force to overwrite)")
        return False

    try:
        shutil.copy2(source_file, target_file)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created layout.tsx")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create layout.tsx: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate shadcn/ui components and setup files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--components",
        type=str,
        help="Comma-separated list of components to generate (default: all)"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing files"
    )
    parser.add_argument(
        "--no-layout",
        action="store_true",
        help="Skip layout.tsx generation"
    )
    parser.add_argument(
        "--no-utils",
        action="store_true",
        help="Skip utils.ts generation"
    )

    args = parser.parse_args()

    # Get paths
    template_dir = get_skill_template_dir()
    target_dir = Path(args.output_dir).resolve()

    if not target_dir.exists():
        print(f"{Colors.RED}Error: Directory does not exist: {target_dir}{Colors.ENDC}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}shadcn/ui Component Generator{Colors.ENDC}")
    print(f"Template: {Colors.BLUE}{template_dir}{Colors.ENDC}")
    print(f"Output: {Colors.BLUE}{target_dir}{Colors.ENDC}")
    print("=" * 60)
    print()

    # Create directories
    create_directories(target_dir)
    print()

    # Generate utils
    if not args.no_utils:
        create_utils_file(target_dir, args.force)
        print()

    # Determine which components to generate
    all_components = ['Button', 'Card', 'Input', 'Modal', 'Navbar']

    if args.components:
        components_to_generate = [c.strip() for c in args.components.split(',')]
    else:
        components_to_generate = all_components

    # Generate components
    success_count = 0
    for component in components_to_generate:
        if copy_component(template_dir, target_dir, component, args.force):
            success_count += 1

    print()

    # Generate hooks
    hooks = ['useModal']
    for hook in hooks:
        copy_hook(template_dir, target_dir, hook, args.force)

    print()

    # Generate layout
    if not args.no_layout:
        copy_layout(template_dir, target_dir, args.force)
        print()

    # Print summary
    print("=" * 60)
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Generation complete!{Colors.ENDC}")
    print(f"\n{Colors.BLUE}Files created:{Colors.ENDC}")
    print(f"  - {success_count} component(s)")
    print(f"  - 1 hook(s)")
    if not args.no_utils:
        print(f"  - lib/utils.ts")
    if not args.no_layout:
        print(f"  - layout.tsx (if generated)")

    print(f"\n{Colors.BLUE}Next steps:{Colors.ENDC}")
    print(f"  1. Install dependencies:")
    print(f"     npm install class-variance-authority clsx tailwind-merge")
    print(f"     npm install @radix-ui/react-slot @radix-ui/react-dialog")
    print(f"  2. Update tailwind.config.ts with shadcn/ui colors")
    print(f"  3. Update globals.css with CSS variables")
    print(f"  4. Validate setup:")
    print(f"     python .claude/skills/shadcn-skill/scripts/validate-setup.py")
    print(f"  5. Start development server: npm run dev\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
