#!/usr/bin/env python3
"""
Generate Next.js component boilerplate for Phase II.

This script creates React component files with TypeScript and proper structure.

Usage:
    python scripts/generate-component.py <component_name> [--client] [--dir <directory>]

Examples:
    python scripts/generate-component.py TodoCard --client
    python scripts/generate-component.py Layout --dir app
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


COMPONENT_TEMPLATE = '''import React from 'react'

interface {component_name}Props {{
  // Add your props here
}}

export default function {component_name}(props: {component_name}Props) {{
  return (
    <div>
      <h1>{component_name}</h1>
    </div>
  )
}}
'''

CLIENT_COMPONENT_TEMPLATE = ''''use client'

import {{ useState }} from 'react'

interface {component_name}Props {{
  // Add your props here
}}

export default function {component_name}(props: {component_name}Props) {{
  const [state, setState] = useState<any>(null)

  return (
    <div>
      <h1>{component_name}</h1>
    </div>
  )
}}
'''


def generate_component(
    component_name: str,
    is_client: bool = False,
    target_dir: str = 'components'
) -> None:
    """Generate a React component file."""

    # Validate component name
    if not component_name:
        print("Error: Component name is required")
        sys.exit(1)

    if not component_name[0].isupper():
        print(f"Error: Component name '{component_name}' must start with uppercase letter")
        sys.exit(1)

    # Determine base directory (assume running from project root)
    base_dir = Path('phase-II/frontend')
    if not base_dir.exists():
        print(f"Error: Frontend directory not found at {base_dir}")
        print("Make sure you're running this from the project root")
        sys.exit(1)

    # Create target directory if it doesn't exist
    component_dir = base_dir / target_dir
    component_dir.mkdir(parents=True, exist_ok=True)

    # Generate file path
    file_name = f"{component_name}.tsx"
    file_path = component_dir / file_name

    if file_path.exists():
        response = input(f"File {file_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    # Select template
    template = CLIENT_COMPONENT_TEMPLATE if is_client else COMPONENT_TEMPLATE

    # Generate content
    content = template.format(component_name=component_name)

    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Created component: {file_path}")
    print(f"  Type: {'Client Component' if is_client else 'Server Component'}")
    print(f"\nNext steps:")
    print(f"  1. Import in your page: import {component_name} from '@/{target_dir}/{component_name}'")
    print(f"  2. Add props to the interface")
    print(f"  3. Implement component logic")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Next.js component boilerplate'
    )
    parser.add_argument(
        'component_name',
        help='Name of the component (PascalCase)'
    )
    parser.add_argument(
        '--client',
        action='store_true',
        help='Generate a client component (with "use client" directive)'
    )
    parser.add_argument(
        '--dir',
        default='components',
        help='Target directory (default: components)'
    )

    args = parser.parse_args()

    generate_component(
        component_name=args.component_name,
        is_client=args.client,
        target_dir=args.dir
    )


if __name__ == '__main__':
    main()
