'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { todoApi, ApiError } from '@/lib/api';
import { Todo, TodoStats } from '@/types/todo';
import { TodoList } from '@/components/TodoList';
import { ProgressDashboard } from '@/components/ProgressDashboard';
import StickyHeader from '@/components/StickyHeader';
import LandingHero from '@/components/LandingHero';
import ProgressSection from '@/components/ProgressSection';
import { celebrateCompletion, getMilestoneMessage } from '@/lib/celebrations';
import { Plus, Search, Filter } from 'lucide-react';

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [stats, setStats] = useState<TodoStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [milestoneMessage, setMilestoneMessage] = useState<string | null>(null);

  // Form state
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [dueDate, setDueDate] = useState('');

  // Load todos and stats
  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [todosData, statsData] = await Promise.all([
        todoApi.getTodos({
          status: filter === 'all' ? undefined : filter,
          category: categoryFilter || undefined,
          search: searchQuery || undefined,
          limit: 100,
        }),
        todoApi.getStats(),
      ]);

      setTodos(todosData.items);
      setStats(statsData);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError('Failed to load todos');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      loadData();
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [filter, categoryFilter, searchQuery]);

  const handleCreate = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      await todoApi.createTodo({
        title: title.trim(),
        category: category.trim() || undefined,
        due_date: dueDate || undefined,
      });
      setTitle('');
      setCategory('');
      setDueDate('');
      setShowCreateForm(false);
      loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      }
    }
  }, [title, category, dueDate]);

  const handleToggleStatus = useCallback(async (todo: Todo) => {
    try {
      const newStatus = todo.status === 'pending' ? 'completed' : 'pending';
      await todoApi.updateTodoStatus(todo.id, newStatus, todo.version);

      // Trigger celebration if completing a task
      if (newStatus === 'completed' && stats) {
        const newCompletedCount = stats.completed + 1;
        celebrateCompletion(newCompletedCount);

        // Show milestone message if applicable
        const message = getMilestoneMessage(newCompletedCount);
        if (message) {
          setMilestoneMessage(message);
          setTimeout(() => setMilestoneMessage(null), 3000);
        }
      }

      loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      }
    }
  }, [stats]);

  const handleDelete = useCallback(async (id: number) => {
    try {
      await todoApi.deleteTodo(id);
      loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      }
    }
  }, []);

  return (
    <div className="min-h-screen">
      {/* Sticky Navigation */}
      <StickyHeader />

      {/* Dashboard Section - Landing Hero */}
      <LandingHero />

      {/* Tasks Section - Main Todo Application */}
      <section
        id="tasks"
        className="min-h-screen py-24 px-6 bg-gradient-to-b from-dark-surface to-dark-bg"
        role="main"
        aria-label="Todo management application"
      >
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-4">
              Your <span className="bg-gradient-to-r from-accent-cyan to-accent-purple bg-clip-text text-transparent">Tasks</span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Manage your todos with clarity and purpose
            </p>
          </motion.div>

          {/* Progress Dashboard */}
          <ProgressDashboard stats={stats} isLoading={loading} />

          {/* Create Todo Button/Form */}
          <div className="mb-8">
            {!showCreateForm ? (
              <motion.button
                onClick={() => setShowCreateForm(true)}
                className="w-full glass-morphism rounded-2xl p-6 text-left hover:border-accent-cyan/50 transition-all group"
                whileHover={{ scale: 1.01 }}
                aria-label="Create new task form"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-accent-cyan to-accent-purple flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Plus className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-medium text-white">Create New Task</div>
                    <div className="text-sm text-slate-400">Click to add a new todo</div>
                  </div>
                </div>
              </motion.button>
            ) : (
              <motion.form
                onSubmit={handleCreate}
                className="glass-morphism rounded-2xl p-8"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Title *
                    </label>
                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      className="w-full px-4 py-3 bg-dark-muted/50 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:border-transparent"
                      placeholder="What needs to be done?"
                      maxLength={500}
                      autoFocus
                      required
                      aria-required="true"
                      aria-label="Todo title"
                    />
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">
                        Category
                      </label>
                      <input
                        type="text"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="w-full px-4 py-3 bg-dark-muted/50 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-accent-purple focus:border-transparent"
                        placeholder="e.g., Work, Personal"
                        maxLength={50}
                        aria-label="Todo category"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-300 mb-2">
                        Due Date
                      </label>
                      <input
                        type="date"
                        value={dueDate}
                        onChange={(e) => setDueDate(e.target.value)}
                        className="w-full px-4 py-3 bg-dark-muted/50 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent-emerald focus:border-transparent"
                        aria-label="Todo due date"
                      />
                    </div>
                  </div>
                  <div className="flex gap-3 pt-2">
                    <button
                      type="submit"
                      disabled={!title.trim()}
                      className="flex-1 px-6 py-3 bg-gradient-to-r from-accent-cyan to-accent-purple text-white rounded-lg font-medium hover:shadow-lg hover:shadow-accent-cyan/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                      Create Task
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowCreateForm(false)}
                      className="px-6 py-3 border border-slate-700 text-slate-300 rounded-lg font-medium hover:bg-dark-muted/50 transition-all"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </motion.form>
            )}
          </div>

          {/* Filters */}
          <div className="mb-8 space-y-4">
            <div className="flex flex-wrap gap-3" role="group" aria-label="Filter todos by status">
              {(['all', 'pending', 'completed'] as const).map((status) => (
                <button
                  key={status}
                  onClick={() => setFilter(status)}
                  className={`px-6 py-2.5 rounded-lg font-medium transition-all ${
                    filter === status
                      ? 'bg-gradient-to-r from-accent-cyan to-accent-purple text-white shadow-lg'
                      : 'glass-morphism text-slate-300 hover:border-accent-cyan/50'
                  }`}
                  aria-label={`Filter ${status} todos`}
                  aria-pressed={filter === status}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </button>
              ))}
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="search"
                  placeholder="Search tasks..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 glass-morphism rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:border-transparent"
                  aria-label="Search todos by title"
                />
              </div>
              <div className="relative">
                <Filter className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Filter by category..."
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 glass-morphism rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-accent-purple focus:border-transparent"
                  aria-label="Filter todos by category"
                />
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg">
              {error}
            </div>
          )}

          {/* Todo List */}
          {loading ? (
            <div className="text-center py-20">
              <div className="inline-flex gap-2">
                <div className="w-3 h-3 bg-accent-cyan rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-3 h-3 bg-accent-purple rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-3 h-3 bg-accent-emerald rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <p className="text-slate-400 mt-4 text-lg">Loading tasks...</p>
            </div>
          ) : todos.length === 0 ? (
            <div className="text-center py-20 glass-morphism rounded-2xl">
              <div className="text-6xl mb-6">📝</div>
              <h3 className="text-2xl font-bold text-white mb-3">No tasks yet</h3>
              <p className="text-slate-400 mb-6">Create your first task to get started</p>
            </div>
          ) : (
            <TodoList
              todos={todos}
              onToggleStatus={handleToggleStatus}
              onDelete={handleDelete}
            />
          )}
        </div>
      </section>

      {/* Analytics Section */}
      <ProgressSection stats={stats} isLoading={loading} />

      {/* Footer */}
      <footer className="py-8 px-6 bg-dark-bg/50 border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto text-center text-slate-500 text-sm">
          <p>Built with Next.js, Tailwind CSS, and Framer Motion</p>
        </div>
      </footer>

      {/* Milestone Toast */}
      {milestoneMessage && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.9 }}
          className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50"
        >
          <div className="glass-card px-6 py-4 rounded-2xl border border-accent-emerald/30 bg-accent-emerald/10 shadow-xl shadow-accent-emerald/20">
            <p className="text-lg font-semibold text-text-primary text-center">
              {milestoneMessage}
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
