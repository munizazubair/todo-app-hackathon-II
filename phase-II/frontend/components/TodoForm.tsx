'use client'

import { useState } from 'react'
import { TodoCreate } from '@/types/todo'
import { MAX_TITLE_LENGTH, ERR_TITLE_EMPTY, ERR_TITLE_TOO_LONG } from '@/lib/constants'

interface TodoFormProps {
  onSubmit: (data: TodoCreate) => Promise<void>
}

export function TodoForm({ onSubmit }: TodoFormProps) {
  const [title, setTitle] = useState('')
  const [category, setCategory] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // Validation
    const trimmedTitle = title.trim()
    if (!trimmedTitle) {
      setError(ERR_TITLE_EMPTY)
      return
    }
    if (trimmedTitle.length > MAX_TITLE_LENGTH) {
      setError(ERR_TITLE_TOO_LONG)
      return
    }

    try {
      setLoading(true)
      await onSubmit({
        title: trimmedTitle,
        category: category.trim() || null,
        due_date: dueDate || null,
      })
      // Clear form on success
      setTitle('')
      setCategory('')
      setDueDate('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
        Create New Todo
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Title Input */}
        <div>
          <label
            htmlFor="title"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={MAX_TITLE_LENGTH}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="Enter todo title"
            disabled={loading}
          />
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {title.length}/{MAX_TITLE_LENGTH} characters
          </div>
        </div>

        {/* Category Input */}
        <div>
          <label
            htmlFor="category"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Category (optional)
          </label>
          <input
            type="text"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            maxLength={50}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
            placeholder="e.g., Work, Personal"
            disabled={loading}
          />
        </div>

        {/* Due Date Input */}
        <div>
          <label
            htmlFor="dueDate"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
          >
            Due Date (optional)
          </label>
          <input
            type="date"
            id="dueDate"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
            disabled={loading}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-400 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !title.trim()}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Creating...' : 'Create Todo'}
        </button>
      </form>
    </div>
  )
}
