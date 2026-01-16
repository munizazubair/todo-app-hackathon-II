/**
 * TypeScript type definitions for Todo entities.
 */

/**
 * Todo status enum
 */
export type TodoStatus = 'pending' | 'completed'

/**
 * Complete Todo object from API
 */
export interface Todo {
  id: number
  title: string
  status: TodoStatus
  category: string | null
  due_date: string | null  // ISO date string (YYYY-MM-DD)
  created_at: string        // ISO datetime string
  updated_at: string        // ISO datetime string
  version: number           // For optimistic locking
}

/**
 * Todo creation payload
 */
export interface TodoCreate {
  title: string
  category?: string | null
  due_date?: string | null  // YYYY-MM-DD format
}

/**
 * Todo update payload
 */
export interface TodoUpdate {
  title: string
  category?: string | null
  due_date?: string | null  // YYYY-MM-DD format
  version: number           // Required for optimistic locking
}

/**
 * API response wrapper
 */
export interface ApiResponse<T> {
  data?: T
  error?: ApiError
}

/**
 * API error structure
 */
export interface ApiError {
  status_code: number
  message: string
  detail?: string | ValidationError[]
  request_id?: string
}

/**
 * Validation error detail
 */
export interface ValidationError {
  field: string
  error: string
}

/**
 * Paginated todos response
 */
export interface TodosResponse {
  items: Todo[]
  total: number
  limit: number
  offset: number
}

/**
 * Todo statistics
 */
export interface TodoStats {
  total: number
  pending: number
  completed: number
  overdue: number
}

/**
 * Query parameters for fetching todos
 */
export interface TodoQueryParams {
  status?: TodoStatus
  category?: string
  search?: string
  limit?: number
  offset?: number
}
