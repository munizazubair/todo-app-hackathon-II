# NextJSSkill Examples

Practical examples and walkthroughs for common tasks.

---

## Example 1: Complete Phase II Frontend Setup

### Step-by-Step Walkthrough

```bash
# 1. Create Next.js project
cd phase-II
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --import-alias '@/*'

cd frontend

# 2. Install dependencies
npm install axios zod react-hot-toast date-fns

# 3. Create directory structure
mkdir -p components lib types public/images

# 4. Copy templates
# From .claude/skills/nextjs-skill/template/

# 5. Configure environment
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
EOF

# 6. Run development server
npm run dev
```

---

## Example 2: Creating a New Todo

```typescript
// In TodoForm.tsx
'use client'

import { useState } from 'react'
import { createTodo } from '@/lib/api'
import { validateTodoCreate } from '@/lib/validation'
import toast from 'react-hot-toast'

export default function TodoForm({ onSuccess }: { onSuccess: () => void }) {
  const [title, setTitle] = useState('')
  const [category, setCategory] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate
    const result = validateTodoCreate({ title, category, due_date: dueDate })
    if (!result.success) {
      toast.error(result.error.errors[0].message)
      return
    }

    // Submit
    setLoading(true)
    try {
      await createTodo(result.data)
      toast.success('Todo created successfully!')
      setTitle('')
      setCategory('')
      setDueDate('')
      onSuccess()
    } catch (error) {
      toast.error('Failed to create todo')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Todo title"
        className="w-full px-4 py-2 border rounded"
        disabled={loading}
      />
      <input
        type="text"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        placeholder="Category (optional)"
        className="w-full px-4 py-2 border rounded"
        disabled={loading}
      />
      <input
        type="date"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
        className="w-full px-4 py-2 border rounded"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      >
        {loading ? 'Creating...' : 'Create Todo'}
      </button>
    </form>
  )
}
```

---

## Example 3: Filtering Todos

```typescript
// In TodoList.tsx
const [filters, setFilters] = useState<TodoFilters>({
  status: 'all',
  category: '',
  search: '',
})

// Handle filter changes
const handleStatusFilter = (status: 'all' | 'pending' | 'completed') => {
  setFilters({ ...filters, status })
}

const handleCategoryFilter = (category: string) => {
  setFilters({ ...filters, category })
}

const handleSearch = (search: string) => {
  setFilters({ ...filters, search })
}

// In JSX
<FilterBar
  filters={filters}
  onStatusChange={handleStatusFilter}
  onCategoryChange={handleCategoryFilter}
/>
<SearchBar onSearch={handleSearch} />
```

---

## Example 4: Using Validation Scripts

### Validate Project Structure

```bash
# Validate current directory
python .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py .

# Validate specific directory
python .claude/skills/nextjs-skill/scripts/validate-nextjs-setup.py phase-II/frontend

# Output example:
# Checking Required Files... ✓
# Checking Directory Structure... ✓
# Checking Component Files... ⚠
# ...
```

### Generate Components

```bash
# Generate server component
python .claude/skills/nextjs-skill/scripts/generate-component.py TodoCard

# Generate client component
python .claude/skills/nextjs-skill/scripts/generate-component.py TodoStats --client

# Generate in custom directory
python .claude/skills/nextjs-skill/scripts/generate-component.py DashboardLayout --dir app
```

---

## Example 5: Error Handling Pattern

```typescript
// lib/api.ts
import axios, { AxiosError } from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.message || 'An error occurred'
      toast.error(message)
    } else if (error.request) {
      // No response received
      toast.error('Network error. Please check your connection.')
    } else {
      // Request setup error
      toast.error('An unexpected error occurred')
    }
    return Promise.reject(error)
  }
)

export default api
```

---

## Example 6: Dashboard with Statistics

```typescript
// app/dashboard/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { getTodos } from '@/lib/api'
import type { Todo } from '@/types/todo'

export default function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    completed: 0,
    overdue: 0,
  })

  useEffect(() => {
    const fetchStats = async () => {
      const response = await getTodos({ limit: 1000 })
      const todos = response.items

      const now = new Date()
      setStats({
        total: todos.length,
        pending: todos.filter(t => t.status === 'pending').length,
        completed: todos.filter(t => t.status === 'completed').length,
        overdue: todos.filter(t =>
          t.due_date &&
          new Date(t.due_date) < now &&
          t.status === 'pending'
        ).length,
      })
    }

    fetchStats()
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 p-8">
      <StatCard title="Total Todos" value={stats.total} color="blue" />
      <StatCard title="Pending" value={stats.pending} color="yellow" />
      <StatCard title="Completed" value={stats.completed} color="green" />
      <StatCard title="Overdue" value={stats.overdue} color="red" />
    </div>
  )
}

function StatCard({ title, value, color }: { title: string; value: number; color: string }) {
  const colors = {
    blue: 'bg-blue-100 text-blue-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    green: 'bg-green-100 text-green-800',
    red: 'bg-red-100 text-red-800',
  }

  return (
    <div className={`p-6 rounded-lg ${colors[color]}`}>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-4xl font-bold">{value}</p>
    </div>
  )
}
```

---

## Example 7: Debounced Search

```typescript
// components/SearchBar.tsx
'use client'

import { useState, useEffect } from 'react'
import { useDebounce } from '@/hooks/useDebounce'

interface SearchBarProps {
  onSearch: (search: string) => void
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const debouncedSearch = useDebounce(searchTerm, 300)

  useEffect(() => {
    onSearch(debouncedSearch)
  }, [debouncedSearch])

  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Search todos..."
      className="w-full px-4 py-2 border rounded"
    />
  )
}

// hooks/useDebounce.ts
import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}
```

---

## Example 8: Integration Testing

```typescript
// __tests__/api.test.ts
import { getTodos, createTodo, deleteTodo } from '@/lib/api'

describe('API Client', () => {
  it('should fetch todos', async () => {
    const response = await getTodos()
    expect(response).toHaveProperty('items')
    expect(response).toHaveProperty('total')
  })

  it('should create and delete todo', async () => {
    // Create
    const todo = await createTodo({
      title: 'Test Todo',
      category: 'Testing',
    })
    expect(todo.id).toBeDefined()
    expect(todo.title).toBe('Test Todo')

    // Delete
    await deleteTodo(todo.id)
  })
})
```

---

**Skill**: NextJSSkill
**Version**: 1.0.0
**Updated**: 2025-12-31
