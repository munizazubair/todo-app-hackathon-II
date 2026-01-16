-- Example SQL Queries for Neon Postgres
-- Todo Application CRUD Operations

-- =============================================================================
-- INSERT QUERIES
-- =============================================================================

-- Insert single todo with positional parameters
INSERT INTO todos (title, description, completed, priority)
VALUES ($1, $2, $3, $4)
RETURNING *;

-- Insert single todo with example data
INSERT INTO todos (title, description, completed, priority)
VALUES ('Complete project documentation', 'Write comprehensive docs for Phase II', false, 'high')
RETURNING *;

-- Batch insert multiple todos
INSERT INTO todos (title, description, completed, priority, due_date)
VALUES
    ('Setup database', 'Configure Neon Postgres', true, 'high', NULL),
    ('Create API endpoints', 'Build REST API with FastAPI', false, 'high', NOW() + INTERVAL '3 days'),
    ('Design UI components', 'Create reusable React components', false, 'medium', NOW() + INTERVAL '5 days'),
    ('Write tests', 'Add unit and integration tests', false, 'medium', NOW() + INTERVAL '7 days'),
    ('Deploy application', 'Deploy to production', false, 'low', NOW() + INTERVAL '14 days')
RETURNING *;

-- Upsert (insert or update on conflict)
INSERT INTO todos (id, title, description, completed, priority)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (id) DO UPDATE
SET title = EXCLUDED.title,
    description = EXCLUDED.description,
    completed = EXCLUDED.completed,
    priority = EXCLUDED.priority,
    updated_at = CURRENT_TIMESTAMP
RETURNING *;

-- =============================================================================
-- SELECT QUERIES
-- =============================================================================

-- Select all todos
SELECT * FROM todos ORDER BY created_at DESC;

-- Select with pagination
SELECT * FROM todos
ORDER BY created_at DESC
LIMIT $1 OFFSET $2;

-- Select by ID
SELECT * FROM todos WHERE id = $1;

-- Select active (incomplete) todos
SELECT * FROM todos
WHERE completed = false
ORDER BY created_at DESC;

-- Select completed todos
SELECT * FROM todos
WHERE completed = true
ORDER BY updated_at DESC;

-- Select by priority
SELECT * FROM todos
WHERE priority = $1
ORDER BY created_at DESC;

-- Select with multiple filters
SELECT * FROM todos
WHERE completed = $1 AND priority = $2
ORDER BY created_at DESC;

-- Select todos due soon (next 7 days)
SELECT * FROM todos
WHERE completed = false
  AND due_date IS NOT NULL
  AND due_date BETWEEN NOW() AND NOW() + INTERVAL '7 days'
ORDER BY due_date ASC;

-- Select overdue todos
SELECT * FROM todos
WHERE completed = false
  AND due_date IS NOT NULL
  AND due_date < NOW()
ORDER BY due_date ASC;

-- Full-text search (case-insensitive)
SELECT * FROM todos
WHERE title ILIKE $1 OR description ILIKE $1
ORDER BY created_at DESC;

-- Search with wildcard
SELECT * FROM todos
WHERE title ILIKE '%' || $1 || '%'
   OR description ILIKE '%' || $1 || '%'
ORDER BY created_at DESC;

-- =============================================================================
-- AGGREGATION QUERIES
-- =============================================================================

-- Count total todos
SELECT COUNT(*) as total FROM todos;

-- Count by status
SELECT
    COUNT(*) FILTER (WHERE completed = true) as completed,
    COUNT(*) FILTER (WHERE completed = false) as active,
    COUNT(*) as total
FROM todos;

-- Count by priority
SELECT
    priority,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed,
    COUNT(*) FILTER (WHERE completed = false) as active
FROM todos
GROUP BY priority
ORDER BY
    CASE priority
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
        ELSE 4
    END;

-- Statistics dashboard
SELECT
    COUNT(*) as total_todos,
    COUNT(*) FILTER (WHERE completed = true) as completed_count,
    COUNT(*) FILTER (WHERE completed = false) as active_count,
    COUNT(*) FILTER (WHERE priority = 'high') as high_priority,
    COUNT(*) FILTER (WHERE due_date < NOW() AND completed = false) as overdue,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE completed = true) / NULLIF(COUNT(*), 0),
        2
    ) as completion_percentage
FROM todos;

-- Todos created per day (last 30 days)
SELECT
    DATE(created_at) as date,
    COUNT(*) as count
FROM todos
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- =============================================================================
-- UPDATE QUERIES
-- =============================================================================

-- Update single field (mark as completed)
UPDATE todos
SET completed = $1, updated_at = CURRENT_TIMESTAMP
WHERE id = $2
RETURNING *;

-- Update multiple fields
UPDATE todos
SET title = $1,
    description = $2,
    priority = $3,
    updated_at = CURRENT_TIMESTAMP
WHERE id = $4
RETURNING *;

-- Partial update (COALESCE for optional fields)
UPDATE todos
SET title = COALESCE($1, title),
    description = COALESCE($2, description),
    completed = COALESCE($3, completed),
    priority = COALESCE($4, priority),
    due_date = COALESCE($5, due_date),
    updated_at = CURRENT_TIMESTAMP
WHERE id = $6
RETURNING *;

-- Mark all high priority todos as completed
UPDATE todos
SET completed = true, updated_at = CURRENT_TIMESTAMP
WHERE priority = 'high' AND completed = false
RETURNING *;

-- Update priority for overdue todos
UPDATE todos
SET priority = 'high', updated_at = CURRENT_TIMESTAMP
WHERE completed = false
  AND due_date IS NOT NULL
  AND due_date < NOW()
  AND priority != 'high'
RETURNING *;

-- Toggle completion status
UPDATE todos
SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;

-- =============================================================================
-- DELETE QUERIES
-- =============================================================================

-- Delete by ID
DELETE FROM todos
WHERE id = $1
RETURNING *;

-- Delete completed todos
DELETE FROM todos
WHERE completed = true
RETURNING *;

-- Delete old completed todos (older than 30 days)
DELETE FROM todos
WHERE completed = true
  AND updated_at < NOW() - INTERVAL '30 days'
RETURNING *;

-- Delete todos without due date and low priority
DELETE FROM todos
WHERE due_date IS NULL
  AND priority = 'low'
  AND completed = true
RETURNING *;

-- Soft delete (if you add a deleted_at column)
-- UPDATE todos
-- SET deleted_at = CURRENT_TIMESTAMP
-- WHERE id = $1
-- RETURNING *;

-- Delete all todos (CAUTION: destructive!)
-- Uncomment to use:
-- DELETE FROM todos;

-- =============================================================================
-- ADVANCED QUERIES
-- =============================================================================

-- Todos with priority ranking
SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY priority ORDER BY created_at) as priority_rank
FROM todos
WHERE completed = false
ORDER BY
    CASE priority
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
        ELSE 4
    END,
    created_at;

-- Recent activity (last 10 updates)
SELECT * FROM todos
ORDER BY updated_at DESC
LIMIT 10;

-- Todos grouped by week
SELECT
    DATE_TRUNC('week', created_at) as week,
    COUNT(*) as count,
    COUNT(*) FILTER (WHERE completed = true) as completed
FROM todos
GROUP BY week
ORDER BY week DESC;

-- Completion rate by priority
SELECT
    priority,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE completed = true) as completed,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE completed = true) / COUNT(*),
        2
    ) as completion_rate
FROM todos
WHERE priority IS NOT NULL
GROUP BY priority
ORDER BY
    CASE priority
        WHEN 'high' THEN 1
        WHEN 'medium' THEN 2
        WHEN 'low' THEN 3
    END;

-- =============================================================================
-- UTILITY QUERIES
-- =============================================================================

-- Get table size
SELECT
    pg_size_pretty(pg_total_relation_size('todos')) as total_size,
    pg_size_pretty(pg_relation_size('todos')) as table_size,
    pg_size_pretty(pg_indexes_size('todos')) as indexes_size;

-- Get table statistics
SELECT
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE tablename = 'todos';

-- Get index usage
SELECT
    indexrelname as index_name,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND tablename = 'todos'
ORDER BY idx_scan DESC;

-- Analyze query performance (EXPLAIN ANALYZE)
EXPLAIN ANALYZE
SELECT * FROM todos
WHERE completed = false AND priority = 'high'
ORDER BY created_at DESC;

-- =============================================================================
-- END OF QUERIES
-- =============================================================================
