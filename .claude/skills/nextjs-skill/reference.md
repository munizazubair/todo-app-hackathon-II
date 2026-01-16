# NextJSSkill Reference Guide

Complete reference documentation for NextJSSkill.

---

## Overview

NextJSSkill provides expert guidance for scaffolding and managing Next.js 14+ applications, specifically tailored for Phase II of the Hackathon II Todo Application.

**Format**: Claude Code Skill
**Framework**: Next.js 14+, React 18+, TypeScript
**Activation**: Automatic based on conversation context

---

## Table of Contents

1. [TypeScript Interfaces](#typescript-interfaces)
2. [API Client](#api-client)
3. [Validation](#validation)
4. [Components](#components)
5. [Configuration](#configuration)
6. [Project Structure](#project-structure)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## TypeScript Interfaces

### Todo Interface

Matches Phase II backend schema (FR-026):

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
```

### Request/Response Interfaces

```typescript
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

**Location**: `template/types/todo.ts`

---

## API Client

### Core Functions

All 7 FastAPI endpoints:

```typescript
// GET /api/todos - List all todos
export async function getTodos(filters?: TodoFilters): Promise<TodoListResponse>

// POST /api/todos - Create new todo
export async function createTodo(data: TodoCreateInput): Promise<Todo>

// GET /api/todos/{id} - Get single todo
export async function getTodo(id: number): Promise<Todo>

// PUT /api/todos/{id} - Update todo
export async function updateTodo(id: number, data: TodoUpdateInput): Promise<Todo>

// DELETE /api/todos/{id} - Delete todo
export async function deleteTodo(id: number): Promise<void>

// PATCH /api/todos/{id}/complete - Toggle completion
export async function toggleTodoComplete(id: number): Promise<Todo>

// GET /api/health - Health check
export async function healthCheck(): Promise<{ status: string }>
```

### Configuration

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

**Location**: `template/lib/api.ts`

---

## Validation

### Zod Schemas

Client-side validation matching Phase I business logic:

```typescript
import { z } from 'zod'

// Title validation (FR-031)
export const titleSchema = z
  .string()
  .min(1, 'Title cannot be empty')
  .max(500, 'Title cannot exceed 500 characters')
  .transform((val) => val.trim())

// Status validation (FR-032)
export const statusSchema = z.enum(['pending', 'completed'])

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

// Full schemas
export const todoCreateSchema = z.object({
  title: titleSchema,
  category: categorySchema,
  due_date: dueDateSchema,
})

export const todoUpdateSchema = z.object({
  title: titleSchema.optional(),
  category: categorySchema,
  due_date: dueDateSchema,
  status: statusSchema.optional(),
})
```

**Location**: `template/lib/validation.ts`

---

## Components

### TodoList

Main component for displaying todos with filtering and search.

**Props**: None (manages own state)

**Features**:
- Fetches todos from API
- Loading states
- Error handling with toast notifications
- Integrates FilterBar and SearchBar
- Displays todo count

**Usage**:
```typescript
import TodoList from '@/components/TodoList'

export default function Home() {
  return <TodoList />
}
```

**Location**: `template/components/TodoList.tsx`

---

### TodoItem

Individual todo display component.

**Props**:
```typescript
interface TodoItemProps {
  todo: Todo
  onUpdate: () => void
}
```

**Features**:
- Checkbox for completion toggle
- Edit and delete actions
- Category and due date display
- Overdue highlighting
- Confirmation dialogs

**Usage**:
```typescript
<TodoItem todo={todo} onUpdate={handleUpdate} />
```

**Location**: `template/components/TodoItem.tsx`

---

### TodoForm

Create/edit todo form component.

**Props**:
```typescript
interface TodoFormProps {
  todo?: Todo
  onSuccess: () => void
  onCancel: () => void
}
```

**Features**:
- Title, category, due date fields
- Client-side validation with Zod
- Loading states
- Error handling

**Usage**:
```typescript
<TodoForm onSuccess={handleSuccess} onCancel={handleCancel} />
```

**Location**: `template/components/TodoForm.tsx`

---

### FilterBar

Filter controls for status and category.

**Props**:
```typescript
interface FilterBarProps {
  filters: TodoFilters
  onFilterChange: (filters: TodoFilters) => void
}
```

**Features**:
- Filter by status (all/pending/completed)
- Filter by category
- Filter count display

**Location**: `template/components/FilterBar.tsx`

---

### SearchBar

Text search component.

**Props**:
```typescript
interface SearchBarProps {
  onSearch: (search: string) => void
}
```

**Features**:
- Debounced search input (300ms)
- Search by todo title
- Clear search button

**Location**: `template/components/SearchBar.tsx`

---

## Configuration

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
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

### .env.local

```bash
# FastAPI Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Environment
NODE_ENV=development
```

---

## Project Structure

```
phase-II/frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Homepage with TodoList
│   ├── dashboard/
│   │   └── page.tsx         # Dashboard with statistics
│   └── globals.css
├── components/
│   ├── TodoList.tsx         # Main list component
│   ├── TodoItem.tsx         # Individual todo
│   ├── TodoForm.tsx         # Create/edit form
│   ├── FilterBar.tsx        # Filters
│   └── SearchBar.tsx        # Search
├── lib/
│   ├── api.ts               # API client
│   ├── constants.ts         # Constants
│   └── validation.ts        # Zod schemas
├── types/
│   └── todo.ts              # TypeScript interfaces
├── public/
│   └── images/
├── .env.local               # Environment variables
├── next.config.js           # Next.js config
├── tailwind.config.ts       # Tailwind config
├── tsconfig.json            # TypeScript config
└── package.json             # Dependencies
```

---

## Best Practices

### 1. Type Safety

Always use TypeScript interfaces:
```typescript
const [todos, setTodos] = useState<Todo[]>([])
```

### 2. Error Handling

Use try-catch with toast notifications:
```typescript
try {
  await createTodo(data)
  toast.success('Todo created successfully')
} catch (error) {
  toast.error('Failed to create todo')
}
```

### 3. Loading States

Always show loading indicators:
```typescript
const [loading, setLoading] = useState(false)

// In UI
{loading ? <Spinner /> : <Content />}
```

### 4. Validation

Validate on both client and server:
```typescript
const result = validateTodoCreate(data)
if (!result.success) {
  toast.error(result.error.message)
  return
}
```

### 5. Component Composition

Break down complex components:
```typescript
// Good
<TodoList>
  <FilterBar />
  <SearchBar />
  {todos.map(todo => <TodoItem key={todo.id} todo={todo} />)}
</TodoList>

// Bad - one giant component
```

---

## Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

### Module Not Found

```bash
rm -rf .next node_modules package-lock.json
npm install
```

### TypeScript Errors

```bash
# Regenerate types
npx next dev --turbo

# Check paths
cat tsconfig.json | grep "paths"
```

### API Connection Issues

1. Check `NEXT_PUBLIC_API_URL` in `.env.local`
2. Verify backend is running on correct port
3. Check CORS configuration in FastAPI
4. Check browser console for errors

---

## Constants Reference

### Error Messages

```typescript
export const ERROR_MESSAGES = {
  TITLE_EMPTY: 'Title cannot be empty',
  TITLE_TOO_LONG: 'Title cannot exceed 500 characters',
  INVALID_STATUS: 'Status must be "pending" or "completed"',
  CATEGORY_TOO_LONG: 'Category cannot exceed 50 characters',
  INVALID_DATE_FORMAT: 'Date must be in YYYY-MM-DD format',
  TODO_NOT_FOUND: 'Todo not found',
  NETWORK_ERROR: 'Network error. Please try again.',
}
```

### Success Messages

```typescript
export const SUCCESS_MESSAGES = {
  TODO_CREATED: 'Todo created successfully',
  TODO_UPDATED: 'Todo updated successfully',
  TODO_DELETED: 'Todo deleted successfully',
  TODO_COMPLETED: 'Todo marked as completed',
  TODO_UNCOMPLETED: 'Todo marked as pending',
}
```

### Default Categories

```typescript
export const DEFAULT_CATEGORIES = [
  'Work',
  'Personal',
  'Shopping',
  'Health',
  'Learning',
  'Other',
]
```

**Location**: `template/lib/constants.ts`

---

## Validation Scripts

### validate-nextjs-setup.py

Validates Next.js project structure against Phase II requirements.

**Usage**:
```bash
python scripts/validate-nextjs-setup.py [frontend_dir]
```

**Checks**:
- Required files
- Directory structure
- Component files
- Dependencies
- Environment variables

### generate-component.py

Generates React component boilerplate.

**Usage**:
```bash
python scripts/generate-component.py <ComponentName> [--client] [--dir <dir>]
```

**Examples**:
```bash
# Server component
python scripts/generate-component.py MyComponent

# Client component
python scripts/generate-component.py MyComponent --client

# Custom directory
python scripts/generate-component.py Layout --dir app
```

---

## Version History

- **1.0.0** (2025-12-31): Initial release
  - Phase II Next.js 14+ support
  - Complete component templates
  - API client integration
  - Validation scripts

---

**Skill**: NextJSSkill
**Version**: 1.0.0
**Format**: Claude Code
**Updated**: 2025-12-31
