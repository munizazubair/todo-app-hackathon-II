# TailwindSkill Examples

Practical examples and walkthroughs for Tailwind CSS integration in Next.js.

---

## Example 1: Complete Tailwind Setup in Next.js

### Step-by-Step Walkthrough

```bash
# 1. Create Next.js project (if not already created)
npx create-next-app@latest my-app --typescript --tailwind --app

# 2. Navigate to project
cd my-app

# 3. Verify Tailwind installation
ls tailwind.config.ts
ls postcss.config.js

# 4. Generate enhanced configuration (optional)
python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir .

# 5. Validate setup
python .claude/skills/tailwind-skill/scripts/validate-setup.py .

# 6. Run development server
npm run dev
```

### Expected Output

```
✓ tailwind.config.ts exists
✓ globals.css exists
✓ globals.css contains @tailwind directives
✓ globals.css imported in app/layout.tsx
✓ All checks passed!
```

---

## Example 2: Importing globals.css

### In app/layout.tsx

```typescript
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

### In app/globals.css

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
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-300;
  }

  .btn-secondary {
    @apply btn bg-gray-500 text-white hover:bg-gray-600 focus:ring-gray-300;
  }

  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500;
  }

  .card {
    @apply bg-white rounded-lg shadow-md overflow-hidden;
  }
}
```

---

## Example 3: Using Example Components

### Button Component

```typescript
// components/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false,
  type = 'button'
}: ButtonProps) {
  const baseClasses = 'font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed'

  const variants = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-300',
    secondary: 'bg-gray-500 text-white hover:bg-gray-600 focus:ring-gray-300',
    outline: 'border-2 border-blue-500 text-blue-500 hover:bg-blue-50 focus:ring-blue-300',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-300'
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]}`}
    >
      {children}
    </button>
  )
}
```

### Usage Example

```typescript
// app/page.tsx
import Button from '@/components/Button'

export default function Home() {
  return (
    <div className="p-8 space-y-4">
      <h1 className="text-3xl font-bold mb-8">Button Examples</h1>

      <div className="flex gap-4">
        <Button variant="primary">Primary Button</Button>
        <Button variant="secondary">Secondary Button</Button>
        <Button variant="outline">Outline Button</Button>
        <Button variant="ghost">Ghost Button</Button>
      </div>

      <div className="flex gap-4">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </div>

      <div className="flex gap-4">
        <Button disabled>Disabled Button</Button>
      </div>
    </div>
  )
}
```

---

## Example 4: Card Component

### Component Definition

```typescript
// components/Card.tsx
interface CardProps {
  title?: string
  subtitle?: string
  children: React.ReactNode
  footer?: React.ReactNode
  className?: string
  onClick?: () => void
}

export default function Card({
  title,
  subtitle,
  children,
  footer,
  className = '',
  onClick
}: CardProps) {
  return (
    <div
      className={`bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow ${
        onClick ? 'cursor-pointer' : ''
      } ${className}`}
      onClick={onClick}
    >
      {(title || subtitle) && (
        <div className="px-6 py-4 border-b border-gray-200">
          {title && <h3 className="text-lg font-semibold text-gray-800">{title}</h3>}
          {subtitle && <p className="text-sm text-gray-600 mt-1">{subtitle}</p>}
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

### Usage Example

```typescript
// app/page.tsx
import Card from '@/components/Card'
import Button from '@/components/Button'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card
            title="Total Users"
            subtitle="Active users in the system"
            footer={<Button variant="outline" size="sm">View Details</Button>}
          >
            <p className="text-4xl font-bold text-blue-600">1,234</p>
            <p className="text-sm text-green-600 mt-2">↑ 12% from last month</p>
          </Card>

          <Card
            title="Revenue"
            subtitle="Total revenue this month"
            footer={<Button variant="outline" size="sm">View Report</Button>}
          >
            <p className="text-4xl font-bold text-green-600">$45,678</p>
            <p className="text-sm text-green-600 mt-2">↑ 8% from last month</p>
          </Card>

          <Card
            title="Tasks"
            subtitle="Pending tasks"
            footer={<Button variant="outline" size="sm">Manage Tasks</Button>}
          >
            <p className="text-4xl font-bold text-orange-600">23</p>
            <p className="text-sm text-red-600 mt-2">↓ 3% from last month</p>
          </Card>
        </div>
      </div>
    </div>
  )
}
```

---

## Example 5: Navbar Component

### Component Definition

```typescript
// components/Navbar.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">MyApp</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-8">
            <Link
              href="/"
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              Home
            </Link>
            <Link
              href="/about"
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              About
            </Link>
            <Link
              href="/services"
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              Services
            </Link>
            <Link
              href="/contact"
              className="text-gray-600 hover:text-gray-900 transition-colors font-medium"
            >
              Contact
            </Link>
          </div>

          {/* CTA Button */}
          <div className="hidden md:flex items-center">
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors font-medium">
              Get Started
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-600 hover:text-gray-900 focus:outline-none"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {mobileMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              href="/"
              className="block px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md font-medium"
            >
              Home
            </Link>
            <Link
              href="/about"
              className="block px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md font-medium"
            >
              About
            </Link>
            <Link
              href="/services"
              className="block px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md font-medium"
            >
              Services
            </Link>
            <Link
              href="/contact"
              className="block px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md font-medium"
            >
              Contact
            </Link>
            <button className="w-full text-left px-3 py-2 bg-blue-500 text-white hover:bg-blue-600 rounded-md font-medium">
              Get Started
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}
```

---

## Example 6: Customizing tailwind.config.ts

### Basic Customization

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Custom colors
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        accent: {
          light: '#fbbf24',
          DEFAULT: '#f59e0b',
          dark: '#d97706',
        },
      },

      // Custom fonts
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },

      // Custom spacing
      spacing: {
        '18': '4.5rem',
        '112': '28rem',
        '128': '32rem',
      },

      // Custom animations
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-slow': 'bounce 3s infinite',
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
      },
    },
  },
  plugins: [],
}

export default config
```

### Using Custom Theme

```typescript
// Using custom colors
<div className="bg-brand-500 text-white">
<button className="bg-accent hover:bg-accent-dark">

// Using custom spacing
<div className="p-18 gap-128">

// Using custom animations
<div className="animate-fade-in">
<div className="animate-slide-up">
```

---

## Example 7: Responsive Todo List

### Complete Example

```typescript
// app/todos/page.tsx
'use client'

import { useState } from 'react'
import Card from '@/components/Card'
import Button from '@/components/Button'

interface Todo {
  id: number
  title: string
  completed: boolean
}

export default function TodosPage() {
  const [todos, setTodos] = useState<Todo[]>([
    { id: 1, title: 'Complete project setup', completed: true },
    { id: 2, title: 'Design UI components', completed: false },
    { id: 3, title: 'Implement API integration', completed: false },
  ])

  const [newTodo, setNewTodo] = useState('')

  const addTodo = () => {
    if (newTodo.trim()) {
      setTodos([...todos, { id: Date.now(), title: newTodo, completed: false }])
      setNewTodo('')
    }
  }

  const toggleTodo = (id: number) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">
          My Todo List
        </h1>

        {/* Add Todo Form */}
        <Card className="mb-6">
          <div className="flex gap-2">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addTodo()}
              placeholder="Add a new todo..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Button onClick={addTodo}>Add</Button>
          </div>
        </Card>

        {/* Todo List */}
        <div className="space-y-3">
          {todos.map(todo => (
            <Card
              key={todo.id}
              className="hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => toggleTodo(todo.id)}
            >
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleTodo(todo.id)}
                  className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
                />
                <span className={`flex-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {todo.title}
                </span>
              </div>
            </Card>
          ))}
        </div>

        {/* Stats */}
        <div className="mt-8 grid grid-cols-2 gap-4">
          <Card className="text-center">
            <p className="text-sm text-gray-600">Total</p>
            <p className="text-2xl font-bold text-gray-900">{todos.length}</p>
          </Card>
          <Card className="text-center">
            <p className="text-sm text-gray-600">Completed</p>
            <p className="text-2xl font-bold text-green-600">
              {todos.filter(t => t.completed).length}
            </p>
          </Card>
        </div>
      </div>
    </div>
  )
}
```

---

## Example 8: Using Validation Script

### Validate Tailwind Setup

```bash
# Navigate to project directory
cd my-nextjs-app

# Run validation
python .claude/skills/tailwind-skill/scripts/validate-setup.py .

# Expected output:
# ✓ tailwind.config.ts exists
# ✓ globals.css exists
# ✓ globals.css contains @tailwind directives
# ✓ globals.css imported in app/layout.tsx
# ✓ All checks passed!
```

### Generate Configuration

```bash
# Generate enhanced Tailwind config and globals.css
python .claude/skills/tailwind-skill/scripts/generate-config.py --output-dir .

# Generated files:
# - tailwind.config.ts (with theme extensions)
# - app/globals.css (with custom layers)
```

---

**Skill**: TailwindSkill
**Version**: 1.0.0
**Updated**: 2025-12-31
