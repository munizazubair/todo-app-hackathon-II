---
name: shadcn-skill
description: Scaffolds and manages shadcn/ui components for Next.js + Tailwind projects. Generates example components, layout, and validates integration.
allowed-tools: Read, Write, Edit, Bash, Glob
model: sonnet
---

# ShadcnSkill - shadcn/ui Component System

Expert guidance for integrating and managing shadcn/ui components in Next.js 14+ applications with Tailwind CSS.

---

## Overview

ShadcnSkill provides comprehensive support for shadcn/ui integration:

- **Component Generation**: Create pre-styled shadcn/ui components
- **Layout Configuration**: Set up shadcn UI Provider integration
- **Validation Tools**: Verify shadcn/ui setup and dependencies
- **Best Practices**: Follow shadcn/ui design patterns
- **Tailwind Integration**: Seamless Tailwind CSS compatibility
- **Dark Mode Support**: Built-in theme switching capabilities

---

## What is shadcn/ui?

shadcn/ui is not a component library. It's a collection of re-usable components that you can copy and paste into your apps. Built on:

- **Radix UI** - Unstyled, accessible components
- **Tailwind CSS** - Utility-first styling
- **class-variance-authority** - Component variants
- **TypeScript** - Full type safety

### Key Differences

Unlike traditional component libraries:
- ✅ Own your components (copy to your codebase)
- ✅ Customize freely without constraints
- ✅ No package dependencies to maintain
- ✅ Full control over implementation
- ✅ Accessible by default (Radix UI primitives)

---

## Core Components

This skill provides 5 essential shadcn/ui components:

### 1. Button Component

```typescript
import { Button } from '@/components/Button'

<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

**Features:**
- Multiple variants (default, destructive, outline, ghost, link)
- Size options (default, sm, lg, icon)
- Loading states
- Disabled states
- Full accessibility

### 2. Card Component

```typescript
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/Card'

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content goes here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Features:**
- Composable structure
- Header, content, footer sections
- Flexible layout
- Hover effects

### 3. Input Component

```typescript
import { Input } from '@/components/Input'

<Input type="email" placeholder="Email" />
<Input type="password" placeholder="Password" disabled />
<Input className="w-full" />
```

**Features:**
- Form-ready inputs
- Disabled states
- Error states
- Full accessibility
- Compatible with React Hook Form

### 4. Modal (Dialog) Component

```typescript
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/Modal'

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Modal</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Modal Title</DialogTitle>
      <DialogDescription>Modal description</DialogDescription>
    </DialogHeader>
    <div>Modal content</div>
  </DialogContent>
</Dialog>
```

**Features:**
- Accessible dialogs
- Focus management
- Backdrop dismiss
- Keyboard navigation
- Composable structure

### 5. Navbar Component

```typescript
import { Navbar } from '@/components/Navbar'

<Navbar />
```

**Features:**
- Responsive design
- Mobile menu toggle
- Theme switcher
- User menu dropdown
- Navigation links

---

## Installation & Setup

### Quick Start

```bash
# 1. Install dependencies
npm install class-variance-authority clsx tailwind-merge
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-slot

# 2. Generate components
python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir ./app

# 3. Validate setup
python .claude/skills/shadcn-skill/scripts/validate-setup.py .
```

### Manual Setup

1. **Create utils/cn.ts** (className utility):

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

2. **Update tailwind.config.ts**:

```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}

export default config
```

3. **Update globals.css**:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

## Component Usage Patterns

### Form with Input and Button

```typescript
'use client'

import { useState } from 'react'
import { Input } from '@/components/Input'
import { Button } from '@/components/Button'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle login
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
      <div>
        <label className="block text-sm font-medium mb-2">Email</label>
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@example.com"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Password</label>
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
        />
      </div>
      <Button type="submit" className="w-full">
        Sign In
      </Button>
    </form>
  )
}
```

### Card with Actions

```typescript
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/Card'
import { Button } from '@/components/Button'

export default function ProductCard() {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Premium Plan</CardTitle>
        <CardDescription>Best for professionals</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-4xl font-bold">$29<span className="text-lg text-muted-foreground">/month</span></div>
        <ul className="mt-4 space-y-2 text-sm">
          <li>✓ Unlimited projects</li>
          <li>✓ Priority support</li>
          <li>✓ Advanced analytics</li>
        </ul>
      </CardContent>
      <CardFooter>
        <Button className="w-full">Subscribe Now</Button>
      </CardFooter>
    </Card>
  )
}
```

### Modal with useModal Hook

```typescript
'use client'

import { Button } from '@/components/Button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/Modal'
import { useModal } from '@/hooks/useModal'

export default function DeleteButton() {
  const { isOpen, openModal, closeModal } = useModal()

  const handleDelete = () => {
    // Perform delete action
    closeModal()
  }

  return (
    <>
      <Button variant="destructive" onClick={openModal}>
        Delete Item
      </Button>

      <Dialog open={isOpen} onOpenChange={closeModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Are you sure?</DialogTitle>
            <DialogDescription>
              This action cannot be undone. This will permanently delete your item.
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end gap-3 mt-4">
            <Button variant="outline" onClick={closeModal}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Delete
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
```

---

## CLI-Style Usage

### Apply shadcn Skill to Project

```bash
# Generate all components and setup
python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir ./app
```

### Validate shadcn Setup

```bash
# Check if shadcn/ui is properly configured
python .claude/skills/shadcn-skill/scripts/validate-setup.py .
```

### Generate Specific Components

```bash
# Generate only specific components
python .claude/skills/shadcn-skill/scripts/generate-components.py --components Button,Card,Input
```

---

## Best Practices

### 1. Component Composition

Build complex UIs by composing primitives:

```typescript
// Good - Composable
<Card>
  <CardHeader>
    <CardTitle>...</CardTitle>
  </CardHeader>
  <CardContent>...</CardContent>
</Card>

// Avoid - Monolithic
<ComplexCard title="..." content="..." />
```

### 2. Use cn() Utility

Always use the `cn()` utility for className merging:

```typescript
import { cn } from '@/lib/utils'

<Button className={cn("mt-4", isActive && "bg-primary")} />
```

### 3. Leverage Variants

Use class-variance-authority for component variants:

```typescript
const buttonVariants = cva(
  "inline-flex items-center justify-center",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        destructive: "bg-destructive text-destructive-foreground",
      },
    },
  }
)
```

### 4. Maintain Accessibility

shadcn/ui components use Radix UI primitives for accessibility:
- Proper ARIA attributes
- Keyboard navigation
- Focus management
- Screen reader support

---

## Dark Mode Integration

shadcn/ui supports dark mode out of the box:

```typescript
'use client'

import { useEffect, useState } from 'react'

export function ThemeToggle() {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')
    root.classList.add(theme)
  }, [theme])

  return (
    <button
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      className="px-4 py-2 rounded-lg border"
    >
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  )
}
```

---

## When to Use This Skill

Activate ShadcnSkill when you need to:
- Set up shadcn/ui in a Next.js project
- Generate shadcn/ui component templates
- Integrate Radix UI with Tailwind CSS
- Create accessible, styled components
- Implement form inputs with validation
- Add modals and dialogs
- Build card-based layouts
- Validate shadcn/ui configuration

---

**Version**: 1.0.0
**Format**: Claude Code Skill
**Framework**: shadcn/ui + Next.js 14+ + Tailwind CSS 3+
**Updated**: 2025-12-31
