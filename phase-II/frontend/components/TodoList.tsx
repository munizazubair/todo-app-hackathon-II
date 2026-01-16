'use client'

import { Todo } from '@/types/todo'
import { TodoItem } from './TodoItem'

interface TodoListProps {
  todos: Todo[]
  onToggleStatus: (todo: Todo) => void
  onDelete: (id: number) => void
}

export function TodoList({ todos, onToggleStatus, onDelete }: TodoListProps) {
  if (todos.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
        <p className="text-gray-600 dark:text-gray-400">
          No todos found. Create one to get started!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggleStatus={onToggleStatus}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
