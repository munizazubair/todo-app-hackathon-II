---
name: tailwind-skill
description: Scaffolds and manages Tailwind CSS setup for Next.js apps. Generates base config, global styles, example components, and validates integration.
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# TailwindSkill - Tailwind CSS Configuration & Management

Expert guidance for integrating and managing Tailwind CSS in Next.js 14+ applications.

---

## Overview

TailwindSkill provides comprehensive support for Tailwind CSS integration with Next.js projects:

- **Configuration Generation**: Create optimized tailwind.config.ts files
- **Global Styles Setup**: Generate and configure globals.css with base styles
- **Component Templates**: Pre-built Tailwind-styled components
- **Validation Tools**: Verify Tailwind integration and configuration
- **Best Practices**: Follow industry-standard Tailwind patterns
- **Theme Customization**: Extend default theme with custom colors, fonts, spacing

---

## Core Capabilities

### 1. Configuration Management

Generate production-ready Tailwind configuration:

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

export default config
```

### 2. Global Styles Setup

Generate globals.css with Tailwind directives and custom styles:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors;
  }
}
```

### 3. Component Templates

Pre-built components following Tailwind best practices:

#### Button Component
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false
}: ButtonProps) {
  const baseClasses = 'font-medium rounded-lg transition-colors focus:outline-none focus:ring-2'

  const variants = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-300',
    secondary: 'bg-gray-500 text-white hover:bg-gray-600 focus:ring-gray-300',
    outline: 'border-2 border-blue-500 text-blue-500 hover:bg-blue-50 focus:ring-blue-300'
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
    >
      {children}
    </button>
  )
}
```

#### Card Component
```typescript
interface CardProps {
  title?: string
  children: React.ReactNode
  footer?: React.ReactNode
  className?: string
}

export default function Card({ title, children, footer, className = '' }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md overflow-hidden ${className}`}>
      {title && (
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        </div>
      )}
      <div className="px-6 py-4">
        {children}
      </div>
      {footer && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          {footer}
        </div>
      )}
    </div>
  )
}
```

#### Navbar Component
```typescript
export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-800">My App</h1>
          </div>

          <div className="hidden md:flex space-x-8">
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              Home
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              About
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">
              Contact
            </a>
          </div>

          <div className="flex items-center">
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
              Sign In
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
```

---

## Installation & Setup

### Quick Start

1. **Install Tailwind CSS**:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

2. **Generate Configuration**:
```bash
python .claude/skills/tailwind-skill/scripts/generate-config.py
```

3. **Import Global Styles**:
```typescript
// app/layout.tsx
import './globals.css'
```

4. **Validate Setup**:
```bash
python .claude/skills/tailwind-skill/scripts/validate-setup.py
```

---

## Theme Customization

### Custom Colors

```typescript
theme: {
  extend: {
    colors: {
      brand: {
        50: '#f0fdfa',
        100: '#ccfbf1',
        500: '#14b8a6',
        600: '#0d9488',
        900: '#134e4a',
      },
    },
  },
}
```

### Custom Fonts

```typescript
theme: {
  extend: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      heading: ['Poppins', 'sans-serif'],
      mono: ['Fira Code', 'monospace'],
    },
  },
}
```

### Custom Spacing

```typescript
theme: {
  extend: {
    spacing: {
      '18': '4.5rem',
      '88': '22rem',
      '128': '32rem',
    },
  },
}
```

---

## Best Practices

### 1. Use @layer Directives

```css
@layer components {
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}

@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent;
  }
}
```

### 2. Responsive Design

```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

### 3. Dark Mode Support

```typescript
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  {/* Dark mode aware */}
</div>
```

### 4. Component Extraction

Extract repeated patterns into components rather than utility classes.

---

## Utility Scripts

### validate-setup.py

Validates Tailwind CSS integration:
- Checks for tailwind.config.ts
- Verifies globals.css exists and contains @tailwind directives
- Confirms globals.css import in layout.tsx
- Color-coded success/failure output

**Usage**:
```bash
python .claude/skills/tailwind-skill/scripts/validate-setup.py [project_dir]
```

### generate-config.py

Generates Tailwind configuration files:
- Creates tailwind.config.ts with recommended theme extensions
- Generates globals.css with base styles and custom layers
- Optional: Creates example components

**Usage**:
```bash
python .claude/skills/tailwind-skill/scripts/generate-config.py [--output-dir path]
```

---

## Template Files

Pre-configured files available in `template/`:

- `tailwind.config.ts` - Production-ready Tailwind configuration
- `globals.css` - Base styles with Tailwind directives
- `components/Button.tsx` - Reusable button component
- `components/Card.tsx` - Card layout component
- `components/Navbar.tsx` - Navigation bar component

---

## Integration with Next.js

### App Router Setup

```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js and Tailwind CSS',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

### Page Example

```typescript
// app/page.tsx
import Button from '@/components/Button'
import Card from '@/components/Card'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Welcome to My App
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card title="Getting Started">
            <p className="text-gray-600 mb-4">
              Start building your application with pre-configured Tailwind CSS.
            </p>
            <Button variant="primary">Learn More</Button>
          </Card>

          <Card title="Documentation">
            <p className="text-gray-600 mb-4">
              Explore our comprehensive documentation and examples.
            </p>
            <Button variant="outline">Read Docs</Button>
          </Card>
        </div>
      </div>
    </main>
  )
}
```

---

## Common Patterns

### Grid Layouts

```typescript
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Items */}
</div>
```

### Flexbox Layouts

```typescript
<div className="flex items-center justify-between">
  {/* Content */}
</div>
```

### Form Styling

```typescript
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
/>
```

### Loading States

```typescript
<div className="animate-pulse">
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

---

## When to Use This Skill

Activate TailwindSkill when you need to:
- Set up Tailwind CSS in a Next.js project
- Generate Tailwind configuration files
- Create Tailwind-styled components
- Validate Tailwind integration
- Customize the default Tailwind theme
- Follow Tailwind CSS best practices
- Implement responsive designs
- Add dark mode support

---

**Version**: 1.0.0
**Format**: Claude Code Skill
**Framework**: Tailwind CSS 3+ with Next.js 14+
**Updated**: 2025-12-31
