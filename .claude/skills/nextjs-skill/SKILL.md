---
name: nextjs-skill
description: Scaffolds and manages Next.js applications for Phase II of Hackathon II. Generates project structure, creates API routes, validates configurations, and suggests best practices for routing, layouts, and API design. Use when starting Phase II Next.js frontend, organizing app directory, creating API routes, or setting up Next.js architecture for the todo application.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

# Next.js Application Scaffold & Management for Phase II

## Overview

This skill helps you scaffold, organize, and manage the Next.js frontend for **Phase II** of the Hackathon II Todo Application. It provides guidance specific to the project requirements:

- **Project initialization**: Create Next.js 14+ project with TypeScript and Tailwind CSS
- **App directory structure**: Organize pages, layouts, components, and API integration
- **Phase II requirements**: Implement todo management UI per the specification
- **Configuration**: Next.js config, environment setup for FastAPI backend integration
- **Validation**: Check project structure matches Phase II specification

## Phase II Context

According to `specs/002-phase-ii-web-app/spec.md`:

**Frontend Stack**:
- Next.js 14+ with App Router
- React 18+ with TypeScript
- Tailwind CSS for responsive design
- Components: TodoList, TodoItem, TodoForm, FilterBar, SearchBar
- API integration with FastAPI backend

**File Structure** (from spec.md):
```
phase-II/
├── frontend/                     # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Homepage with todo list
│   │   └── dashboard/
│   │       └── page.tsx          # Dashboard with statistics
│   ├── components/
│   │   ├── TodoList.tsx          # Main todo list
│   │   ├── TodoItem.tsx          # Individual todo card
│   │   ├── TodoForm.tsx          # Create/edit form
│   │   ├── FilterBar.tsx         # Status/category filters
│   │   └── SearchBar.tsx         # Text search
│   ├── lib/
│   │   ├── api.ts                # API client functions
│   │   ├── constants.ts          # Frontend constants
│   │   └── validation.ts         # Client-side validation
│   ├── types/
│   │   └── todo.ts               # TypeScript interfaces
│   ├── package.json              # Frontend dependencies
│   └── next.config.js            # Next.js configuration
```

## Quick Start Commands

### Initialize Next.js Project (Phase II)

```bash
# Navigate to phase-II directory
cd phase-II

# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --no-src-dir \
  --import-alias '@/*'

# Navigate to frontend
cd frontend

# Install additional dependencies
npm install axios zod react-hot-toast date-fns

# Start development server
npm run dev
```

### Verify Setup

```bash
# Check Node.js version (should be 18+)
node --version

# Verify Next.js installation
npx next --version

# Run development server
npm run dev
# Should start on http://localhost:3000
```

## Directory Structure Setup

After creating the Next.js app, set up the Phase II structure:

```bash
# Create required directories
mkdir -p app/dashboard
mkdir -p components
mkdir -p lib
mkdir -p types
mkdir -p public/images

# Create initial TypeScript interfaces
touch types/todo.ts

# Create lib utilities
touch lib/api.ts lib/constants.ts lib/validation.ts

# Create components
touch components/TodoList.tsx
touch components/TodoItem.tsx
touch components/TodoForm.tsx
touch components/FilterBar.tsx
touch components/SearchBar.tsx
```

## TypeScript Interfaces (Phase II Spec)

### types/todo.ts

Based on backend schema from spec.md (FR-026):

```typescript
export interface Todo {
  id: number
  title: string
  status: 'pending' | 'completed'
  category: string | null
  due_date: string | null  // YYYY-MM-DD format
  created_at: string       // ISO timestamp
  updated_at: string       // ISO timestamp
}

export interface TodoCreateInput {
  title: string
  category?: string
  due_date?: string
}

export interface TodoUpdateInput {
  title?: string
  category?: string
  due_date?: string
  status?: 'pending' | 'completed'
}

export interface TodoListResponse {
  items: Todo[]
  total: number
  limit: number
  offset: number
}

export interface TodoFilters {
  status?: 'pending' | 'completed' | 'all'
  category?: string
  search?: string
  limit?: number
  offset?: number
}
```

## API Client (lib/api.ts)

Connect to FastAPI backend (spec.md: FR-014 to FR-024):

```typescript
import axios from 'axios'
import type { Todo, TodoCreateInput, TodoUpdateInput, TodoListResponse, TodoFilters } from '@/types/todo'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// GET /api/todos - List all todos with filters
export async function getTodos(filters?: TodoFilters): Promise<TodoListResponse> {
  const params = new URLSearchParams()

  if (filters?.status && filters.status !== 'all') {
    params.append('status', filters.status)
  }
  if (filters?.category) {
    params.append('category', filters.category)
  }
  if (filters?.search) {
    params.append('search', filters.search)
  }
  params.append('limit', String(filters?.limit || 20))
  params.append('offset', String(filters?.offset || 0))

  const response = await api.get<TodoListResponse>('/todos', { params })
  return response.data
}

// GET /api/todos/{id} - Get single todo
export async function getTodo(id: number): Promise<Todo> {
  const response = await api.get<Todo>(`/todos/${id}`)
  return response.data
}

// POST /api/todos - Create new todo
export async function createTodo(data: TodoCreateInput): Promise<Todo> {
  const response = await api.post<Todo>('/todos', data)
  return response.data
}

// PUT /api/todos/{id} - Update todo
export async function updateTodo(id: number, data: TodoUpdateInput): Promise<Todo> {
  const response = await api.put<Todo>(`/todos/${id}`, data)
  return response.data
}

// DELETE /api/todos/{id} - Delete todo
export async function deleteTodo(id: number): Promise<void> {
  await api.delete(`/todos/${id}`)
}

// PATCH /api/todos/{id}/complete - Toggle completion
export async function toggleTodoComplete(id: number): Promise<Todo> {
  const response = await api.patch<Todo>(`/todos/${id}/complete`)
  return response.data
}

// GET /api/health - Health check
export async function healthCheck(): Promise<{ status: string }> {
  const response = await api.get('/health')
  return response.data
}
```

## Client-Side Validation (lib/validation.ts)

Mirrors Phase I validation (from `phase-I/src/models.py`):

```typescript
import { z } from 'zod'

// Title validation: non-empty, max 500 characters, trimmed (FR-031)
export const titleSchema = z
  .string()
  .min(1, 'Title cannot be empty')
  .max(500, 'Title cannot exceed 500 characters')
  .transform((val) => val.trim())

// Status validation (FR-032)
export const statusSchema = z.enum(['pending', 'completed'], {
  errorMap: () => ({ message: 'Status must be "pending" or "completed"' }),
})

// Category validation (FR-033)
export const categorySchema = z
  .string()
  .max(50, 'Category cannot exceed 50 characters')
  .optional()

// Due date validation (FR-034)
export const dueDateSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Date must be in YYYY-MM-DD format')
  .optional()

// Full todo creation schema
export const todoCreateSchema = z.object({
  title: titleSchema,
  category: categorySchema,
  due_date: dueDateSchema,
})

// Full todo update schema
export const todoUpdateSchema = z.object({
  title: titleSchema.optional(),
  category: categorySchema,
  due_date: dueDateSchema,
  status: statusSchema.optional(),
})

// Validation helper
export function validateTodoCreate(data: unknown) {
  return todoCreateSchema.safeParse(data)
}

export function validateTodoUpdate(data: unknown) {
  return todoUpdateSchema.safeParse(data)
}
```

## Constants (lib/constants.ts)

Migrated from `phase-I/src/constants.py`:

```typescript
export const TODO_STATUS = {
  PENDING: 'pending' as const,
  COMPLETED: 'completed' as const,
}

export const ERROR_MESSAGES = {
  TITLE_EMPTY: 'Title cannot be empty',
  TITLE_TOO_LONG: 'Title cannot exceed 500 characters',
  INVALID_STATUS: 'Status must be "pending" or "completed"',
  CATEGORY_TOO_LONG: 'Category cannot exceed 50 characters',
  INVALID_DATE_FORMAT: 'Date must be in YYYY-MM-DD format',
  TODO_NOT_FOUND: 'Todo not found',
  NETWORK_ERROR: 'Network error. Please try again.',
}

export const SUCCESS_MESSAGES = {
  TODO_CREATED: 'Todo created successfully',
  TODO_UPDATED: 'Todo updated successfully',
  TODO_DELETED: 'Todo deleted successfully',
  TODO_COMPLETED: 'Todo marked as completed',
  TODO_UNCOMPLETED: 'Todo marked as pending',
}

export const DEFAULT_CATEGORIES = [
  'Work',
  'Personal',
  'Shopping',
  'Health',
  'Learning',
  'Other',
]
```

## Component Templates

### TodoList Component (components/TodoList.tsx)

Replaces `phase-I/src/cli.py::display_todos`:

```typescript
'use client'

import { useState, useEffect } from 'react'
import { getTodos } from '@/lib/api'
import type { Todo, TodoFilters } from '@/types/todo'
import TodoItem from './TodoItem'
import FilterBar from './FilterBar'
import SearchBar from './SearchBar'
import toast from 'react-hot-toast'

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<TodoFilters>({ status: 'all' })
  const [total, setTotal] = useState(0)

  const fetchTodos = async () => {
    setLoading(true)
    try {
      const response = await getTodos(filters)
      setTodos(response.items)
      setTotal(response.total)
    } catch (error) {
      toast.error('Failed to load todos')
      console.error('Error fetching todos:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTodos()
  }, [filters])

  const handleFilterChange = (newFilters: TodoFilters) => {
    setFilters(newFilters)
  }

  const handleTodoUpdate = () => {
    fetchTodos()
  }

  if (loading) {
    return <div className="text-center py-8">Loading todos...</div>
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-4">Your Todos</h1>
        <SearchBar onSearch={(search) => setFilters({ ...filters, search })} />
        <FilterBar filters={filters} onFilterChange={handleFilterChange} />
      </div>

      <div className="mb-4 text-sm text-gray-600">
        Total: {total} todo{total !== 1 ? 's' : ''}
      </div>

      {todos.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No todos found. Create your first todo!
        </div>
      ) : (
        <div className="space-y-3">
          {todos.map((todo) => (
            <TodoItem key={todo.id} todo={todo} onUpdate={handleTodoUpdate} />
          ))}
        </div>
      )}
    </div>
  )
}
```

### TodoItem Component (components/TodoItem.tsx)

```typescript
'use client'

import { useState } from 'react'
import { toggleTodoComplete, deleteTodo } from '@/lib/api'
import type { Todo } from '@/types/todo'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

interface TodoItemProps {
  todo: Todo
  onUpdate: () => void
}

export default function TodoItem({ todo, onUpdate }: TodoItemProps) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleToggleComplete = async () => {
    try {
      await toggleTodoComplete(todo.id)
      toast.success(todo.status === 'pending' ? 'Todo completed' : 'Todo reopened')
      onUpdate()
    } catch (error) {
      toast.error('Failed to update todo')
      console.error(error)
    }
  }

  const handleDelete = async () => {
    if (!confirm(`Delete "${todo.title}"? This cannot be undone.`)) return

    setIsDeleting(true)
    try {
      await deleteTodo(todo.id)
      toast.success('Todo deleted successfully')
      onUpdate()
    } catch (error) {
      toast.error('Failed to delete todo')
      console.error(error)
      setIsDeleting(false)
    }
  }

  const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && todo.status === 'pending'

  return (
    <div className={`border rounded-lg p-4 ${todo.status === 'completed' ? 'bg-green-50' : 'bg-white'} ${isOverdue ? 'border-red-400' : 'border-gray-200'}`}>
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={todo.status === 'completed'}
          onChange={handleToggleComplete}
          className="mt-1 h-5 w-5"
        />

        <div className="flex-1">
          <h3 className={`text-lg font-medium ${todo.status === 'completed' ? 'line-through text-gray-500' : ''}`}>
            {todo.title}
          </h3>

          <div className="flex gap-3 mt-2 text-sm text-gray-600">
            {todo.category && (
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                {todo.category}
              </span>
            )}
            {todo.due_date && (
              <span className={`px-2 py-1 rounded ${isOverdue ? 'bg-red-100 text-red-800' : 'bg-gray-100'}`}>
                Due: {format(new Date(todo.due_date), 'MMM dd, yyyy')}
              </span>
            )}
          </div>
        </div>

        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="text-red-600 hover:text-red-800 disabled:opacity-50"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
```

## Configuration Files

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
```

### .env.local

```bash
# FastAPI Backend URL (FR-017: CORS configured for this origin)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Next.js Configuration
NODE_ENV=development
```

### tailwind.config.ts

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
      colors: {
        primary: '#3b82f6',
        secondary: '#10b981',
      },
    },
  },
  plugins: [],
}

export default config
```

## Root Layout (app/layout.tsx)

```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App - Phase II',
  description: 'Full-stack todo application with Next.js and FastAPI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Toaster position="top-right" />
        {children}
      </body>
    </html>
  )
}
```

## Homepage (app/page.tsx)

Replaces `phase-I/src/main.py` command loop:

```typescript
import TodoList from '@/components/TodoList'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <TodoList />
    </main>
  )
}
```

## Phase II Success Criteria Checklist

Per spec.md (SC-001 to SC-010):

- [ ] SC-001: Web UI loads in under 2 seconds
- [ ] SC-002: All Phase I CRUD operations work in web interface
- [ ] SC-007: UI is responsive on mobile (320px) and desktop (1920px)
- [ ] FR-006: Client-side validation matches Phase I rules (max 500 chars, non-empty)
- [ ] FR-007: Loading states displayed during API calls
- [ ] FR-008: Error messages shown via toast notifications
- [ ] FR-009: Confirmation dialog before deleting todos
- [ ] FR-013: Responsive layout works on mobile, tablet, desktop

## Common Tasks

### Add a New Component

```bash
# Create component file
touch components/NewComponent.tsx

# Component template
cat > components/NewComponent.tsx << 'EOF'
'use client'

export default function NewComponent() {
  return <div>New Component</div>
}
EOF
```

### Run Development Server

```bash
cd phase-II/frontend
npm run dev
# Access at http://localhost:3000
```

### Build for Production

```bash
npm run build
npm start
```

### Run Type Checking

```bash
npx tsc --noEmit
```

### Run Linting

```bash
npm run lint
```

## Integration with FastAPI Backend

The frontend connects to the FastAPI backend via the API client in `lib/api.ts`. Ensure:

1. Backend is running on `http://localhost:8000` (or set `NEXT_PUBLIC_API_URL`)
2. CORS is configured in FastAPI to allow frontend origin (FR-017)
3. All endpoints match the spec (FR-019 to FR-024)

## When to Use This Skill

This skill activates when you:
- Start Phase II frontend implementation
- Need to create Next.js components for todo management
- Set up API integration with FastAPI backend
- Validate frontend structure against Phase II spec
- Implement responsive UI with Tailwind CSS
- Create forms with client-side validation

Ask Claude about Phase II Next.js implementation, and this skill will guide you!
