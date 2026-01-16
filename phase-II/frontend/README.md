# Phase II Frontend - Next.js Todo Application

Modern web-based todo application built with Next.js 14, React 18, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.0+
- **UI Library**: React 18+
- **Styling**: Tailwind CSS 3+
- **Components**: shadcn/ui (Radix UI)
- **Icons**: Lucide React
- **Testing**: Jest + React Testing Library

## Setup Instructions

### 1. Prerequisites

- Node.js 18 or higher
- npm or yarn

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Initialize shadcn/ui

The project uses shadcn/ui components. Components are already installed, but you can add more:

```bash
npx shadcn-ui@latest add [component-name]
```

### 5. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 6. Build for Production

```bash
npm run build
npm start
```

## Features

- ✅ Create, read, update, and delete todos
- ✅ Mark todos as complete/incomplete
- ✅ Filter todos by status (all/pending/completed)
- ✅ Search todos by title
- ✅ Organize todos with categories
- ✅ Set due dates for todos
- ✅ View overdue todos
- ✅ Dashboard with statistics
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Accessible UI (WCAG AA compliance)
- ✅ Toast notifications for user feedback

## Running Tests

```bash
npm test
```

Watch mode:

```bash
npm run test:watch
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Homepage (todo list)
│   └── dashboard/          # Dashboard page
├── components/             # React components
│   ├── TodoList.tsx        # Main todo list
│   ├── TodoItem.tsx        # Individual todo card
│   ├── TodoForm.tsx        # Create/edit form
│   ├── FilterBar.tsx       # Status/category filters
│   ├── SearchBar.tsx       # Search input
│   └── ...
├── lib/                    # Utilities and helpers
│   ├── api.ts              # API client functions
│   ├── constants.ts        # Constants
│   ├── utils.ts            # Utility functions
│   └── validation.ts       # Client-side validation
├── types/                  # TypeScript type definitions
│   └── todo.ts             # Todo types
├── tests/                  # Test files
└── package.json
```

## Development

### Adding a New Component

1. Create component file in `components/`
2. Use TypeScript for type safety
3. Style with Tailwind CSS
4. Add tests in `tests/components/`

### API Integration

API client functions are in `lib/api.ts`. All functions return promises and handle errors automatically.

**Available Functions:**

```typescript
import { todoApi } from '@/lib/api'

// Fetch todos with filters
const response = await todoApi.getTodos({
  status: 'pending',      // optional: 'pending' | 'completed'
  category: 'Work',       // optional: filter by category
  search: 'meeting',      // optional: search in title
  limit: 20,              // optional: default 20
  offset: 0               // optional: default 0
})
// Returns: { items: Todo[], total: number, limit: number, offset: number }

// Create todo
const newTodo = await todoApi.createTodo({
  title: 'Buy groceries',
  category: 'Shopping',   // optional
  due_date: '2025-12-31'  // optional: YYYY-MM-DD
})

// Update todo
const updatedTodo = await todoApi.updateTodo(todoId, {
  title: 'Buy organic groceries',
  category: 'Shopping',
  due_date: '2025-12-31',
  version: currentVersion  // required for optimistic locking
})

// Toggle status
const toggled = await todoApi.updateTodoStatus(
  todoId,
  'completed',      // 'pending' | 'completed'
  currentVersion    // required for optimistic locking
)

// Delete todo
await todoApi.deleteTodo(todoId)

// Get statistics
const stats = await todoApi.getStats()
// Returns: { total: number, pending: number, completed: number, overdue: number }
```

**Error Handling:**

```typescript
import { ApiError } from '@/lib/api'

try {
  await todoApi.createTodo({ title: 'New task' })
} catch (err) {
  if (err instanceof ApiError) {
    console.error(err.detail)      // Human-readable error message
    console.error(err.status)      // HTTP status code
    console.error(err.requestId)   // Request ID for debugging
  }
}
```

### Using shadcn/ui Components

shadcn/ui components are copied into the project. To use:

```tsx
import { Button } from '@/components/ui/button'
import { Dialog } from '@/components/ui/dialog'

<Button variant="default">Click me</Button>
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API base URL (default: http://localhost:8000/api)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Minimum mobile width: 320px

## Keyboard Shortcuts

- `Tab`: Navigate between form inputs
- `Enter`: Submit forms
- `Escape`: Close dialogs
- Arrow keys: Navigate todo list

## Accessibility

This application follows WCAG AA guidelines:
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support
- Focus indicators
- Color contrast ratios
