#!/usr/bin/env python3
"""
Tailwind CSS Configuration Generator

Generates enhanced tailwind.config.ts and globals.css files for Next.js projects.
"""

import os
import sys
import argparse
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


TAILWIND_CONFIG_CONTENT = '''import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

export default config
'''

GLOBALS_CSS_CONTENT = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
  }

  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold;
  }

  h1 {
    @apply text-4xl;
  }

  h2 {
    @apply text-3xl;
  }

  h3 {
    @apply text-2xl;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed;
  }

  .btn-primary {
    @apply btn bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-300;
  }

  .btn-secondary {
    @apply btn bg-secondary-500 text-white hover:bg-secondary-600 focus:ring-secondary-300;
  }

  .btn-outline {
    @apply btn border-2 border-primary-500 text-primary-500 hover:bg-primary-50 focus:ring-primary-300;
  }

  .btn-ghost {
    @apply btn text-gray-700 hover:bg-gray-100 focus:ring-gray-300;
  }

  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed;
  }

  .card {
    @apply bg-white rounded-lg shadow-md overflow-hidden;
  }

  .card-header {
    @apply px-6 py-4 border-b border-gray-200;
  }

  .card-body {
    @apply px-6 py-4;
  }

  .card-footer {
    @apply px-6 py-4 bg-gray-50 border-t border-gray-200;
  }
}

@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-primary-500 to-purple-600 bg-clip-text text-transparent;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .container-custom {
    @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
  }
}
'''

POSTCSS_CONFIG_CONTENT = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''


def create_tailwind_config(output_dir: Path) -> bool:
    """Create tailwind.config.ts file."""
    config_path = output_dir / "tailwind.config.ts"

    try:
        config_path.write_text(TAILWIND_CONFIG_CONTENT)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created {config_path}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create {config_path}: {e}")
        return False


def create_globals_css(output_dir: Path) -> bool:
    """Create globals.css file."""
    # Check if app/ or src/app/ directory exists
    app_dir = output_dir / "app"
    src_app_dir = output_dir / "src" / "app"

    if app_dir.exists():
        globals_path = app_dir / "globals.css"
    elif src_app_dir.exists():
        globals_path = src_app_dir / "globals.css"
    else:
        # Create app directory if it doesn't exist
        app_dir.mkdir(parents=True, exist_ok=True)
        globals_path = app_dir / "globals.css"

    try:
        globals_path.write_text(GLOBALS_CSS_CONTENT)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created {globals_path}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create {globals_path}: {e}")
        return False


def create_postcss_config(output_dir: Path) -> bool:
    """Create postcss.config.js file."""
    postcss_path = output_dir / "postcss.config.js"

    # Don't overwrite if it already exists
    if postcss_path.exists():
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} postcss.config.js already exists, skipping")
        return True

    try:
        postcss_path.write_text(POSTCSS_CONFIG_CONTENT)
        print(f"{Colors.GREEN}✓{Colors.ENDC} Created {postcss_path}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.ENDC} Failed to create {postcss_path}: {e}")
        return False


def check_dependencies(output_dir: Path) -> bool:
    """Check if required dependencies are installed."""
    package_json = output_dir / "package.json"

    if not package_json.exists():
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} package.json not found")
        return False

    try:
        import json
        with open(package_json, 'r') as f:
            data = json.load(f)

        dev_dependencies = data.get('devDependencies', {})
        dependencies = data.get('dependencies', {})

        required = ['tailwindcss', 'postcss', 'autoprefixer']
        missing = []

        for package in required:
            if package not in dev_dependencies and package not in dependencies:
                missing.append(package)

        if missing:
            print(f"\n{Colors.YELLOW}⚠ Missing dependencies:{Colors.ENDC}")
            print(f"  Run: npm install -D {' '.join(missing)}\n")
            return False

        return True

    except Exception as e:
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} Could not check dependencies: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate enhanced Tailwind CSS configuration files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--with-postcss",
        action="store_true",
        help="Also generate postcss.config.js"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing files"
    )

    args = parser.parse_args()

    # Get absolute path
    output_dir = Path(args.output_dir).resolve()

    if not output_dir.exists():
        print(f"{Colors.RED}Error: Directory does not exist: {output_dir}{Colors.ENDC}")
        sys.exit(1)

    print(f"\n{Colors.BOLD}Tailwind CSS Configuration Generator{Colors.ENDC}")
    print(f"Output directory: {Colors.BLUE}{output_dir}{Colors.ENDC}")
    print("=" * 60)
    print()

    # Check if files already exist
    config_exists = (output_dir / "tailwind.config.ts").exists()
    app_globals = output_dir / "app" / "globals.css"
    src_globals = output_dir / "src" / "app" / "globals.css"
    globals_exists = app_globals.exists() or src_globals.exists()

    if (config_exists or globals_exists) and not args.force:
        print(f"{Colors.YELLOW}⚠ Warning: Some files already exist{Colors.ENDC}")
        if config_exists:
            print(f"  - tailwind.config.ts")
        if globals_exists:
            print(f"  - globals.css")
        print(f"\nUse --force to overwrite existing files")
        sys.exit(1)

    # Generate files
    success = True

    success &= create_tailwind_config(output_dir)
    success &= create_globals_css(output_dir)

    if args.with_postcss:
        success &= create_postcss_config(output_dir)

    # Check dependencies
    print()
    check_dependencies(output_dir)

    # Print summary
    print()
    print("=" * 60)

    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Configuration files generated successfully!{Colors.ENDC}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.ENDC}")
        print(f"  1. Ensure globals.css is imported in your layout.tsx:")
        print(f"     import './globals.css'")
        print(f"  2. Install dependencies (if not already installed):")
        print(f"     npm install -D tailwindcss postcss autoprefixer")
        print(f"  3. Validate setup:")
        print(f"     python .claude/skills/tailwind-skill/scripts/validate-setup.py")
        print(f"  4. Start development server:")
        print(f"     npm run dev\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some files could not be generated{Colors.ENDC}")
        print(f"\nPlease check the errors above and try again.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
