'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { Todo } from '@/types/todo';
import { formatDate, isOverdue } from '@/lib/utils';
import { Trash2, Calendar, Tag, Clock } from 'lucide-react';
import { useState, useEffect, memo } from 'react';

interface TodoItemProps {
  todo: Todo;
  onToggleStatus: (todo: Todo) => void;
  onDelete: (id: number) => void;
}

export const TodoItem = memo(function TodoItem({ todo, onToggleStatus, onDelete }: TodoItemProps) {
  const isPending = todo.status === 'pending';
  const overdue = isPending && isOverdue(todo.due_date);
  const [timeUntilDue, setTimeUntilDue] = useState<string>('');

  // Calculate time until due date
  useEffect(() => {
    if (!todo.due_date || !isPending) return;

    const calculateTimeLeft = () => {
      const now = new Date();
      const due = new Date(todo.due_date!);
      const diff = due.getTime() - now.getTime();

      if (diff < 0) return '';

      const hours = Math.floor(diff / (1000 * 60 * 60));
      const days = Math.floor(hours / 24);

      if (days > 1) return `${days} days left`;
      if (days === 1) return '1 day left';
      if (hours > 1) return `${hours} hours left`;
      if (hours === 1) return '1 hour left';
      return 'Due soon';
    };

    setTimeUntilDue(calculateTimeLeft());
    const timer = setInterval(() => setTimeUntilDue(calculateTimeLeft()), 60000);
    return () => clearInterval(timer);
  }, [todo.due_date, isPending]);

  const showDueWarning = isPending && todo.due_date && (overdue || timeUntilDue.includes('hours') || timeUntilDue.includes('soon'));

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: isPending ? 1 : 0.5, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      whileHover={{ y: -2, transition: { duration: 0.2 } }}
      className="group relative"
    >
      {/* Glass morphism card */}
      <div
        className={`relative bg-dark-surface/50 backdrop-blur-lg border rounded-xl p-5 transition-all ${
          isPending
            ? 'border-slate-700 hover:border-accent-cyan/50 shadow-lg'
            : 'border-slate-800/50'
        }`}
      >
        {/* Gradient border on hover */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-accent-cyan/0 via-accent-purple/0 to-accent-emerald/0 group-hover:from-accent-cyan/20 group-hover:via-accent-purple/20 group-hover:to-accent-emerald/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-sm -z-10" />

        <div className="flex items-start gap-4">
          {/* Custom animated checkbox - Touch-friendly size on mobile */}
          <motion.button
            onClick={() => onToggleStatus(todo)}
            className="flex-shrink-0 pt-1 focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:ring-offset-2 focus:ring-offset-dark-bg rounded min-h-[44px] min-w-[44px] md:min-h-0 md:min-w-0 flex items-center justify-center"
            whileTap={{ scale: 0.9 }}
            aria-label={isPending ? 'Mark as completed' : 'Mark as pending'}
          >
            <div
              className={`w-6 h-6 md:w-6 md:h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                isPending
                  ? 'border-slate-500 hover:border-accent-cyan'
                  : 'border-accent-emerald bg-accent-emerald'
              }`}
            >
              <AnimatePresence>
                {!isPending && (
                  <motion.svg
                    className="w-4 h-4 text-white"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{ pathLength: 1, opacity: 1 }}
                    exit={{ pathLength: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                  >
                    <motion.path
                      d="M5 13l4 4L19 7"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </motion.svg>
                )}
              </AnimatePresence>
            </div>
          </motion.button>

          {/* Content */}
          <div className="flex-grow min-w-0">
            <h3
              className={`text-lg font-medium mb-2 transition-all ${
                isPending
                  ? 'text-white'
                  : 'text-slate-500 line-through'
              }`}
            >
              {todo.title}
            </h3>

            {/* Metadata pills */}
            <div className="flex flex-wrap gap-2">
              {/* Category */}
              {todo.category && (
                <motion.span
                  className="inline-flex items-center space-x-1.5 px-3 py-1 bg-accent-purple/10 border border-accent-purple/20 rounded-full text-sm text-accent-purple"
                  whileHover={{ scale: 1.05, boxShadow: '0 0 12px rgba(167, 139, 250, 0.3)' }}
                >
                  <Tag className="w-3.5 h-3.5" />
                  <span>{todo.category}</span>
                </motion.span>
              )}

              {/* Due Date */}
              {todo.due_date && (
                <motion.span
                  className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-sm ${
                    overdue
                      ? 'bg-red-500/10 border border-red-500/30 text-red-400'
                      : showDueWarning
                      ? 'bg-yellow-500/10 border border-yellow-500/30 text-yellow-400'
                      : 'bg-slate-700/50 border border-slate-600/30 text-slate-300'
                  }`}
                  whileHover={{ scale: 1.05 }}
                >
                  {showDueWarning ? (
                    <Clock className="w-3.5 h-3.5" />
                  ) : (
                    <Calendar className="w-3.5 h-3.5" />
                  )}
                  <span>
                    {overdue
                      ? 'Overdue'
                      : timeUntilDue || formatDate(todo.due_date)}
                  </span>
                </motion.span>
              )}
            </div>

            {/* Timestamps */}
            <div className="text-xs text-slate-500 mt-3 font-mono">
              Created {new Date(todo.created_at).toLocaleDateString()}
            </div>
          </div>

          {/* Delete Button - Touch-friendly size on mobile */}
          <motion.button
            onClick={() => onDelete(todo.id)}
            className="flex-shrink-0 p-2 min-h-[44px] min-w-[44px] md:min-h-0 md:min-w-0 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-dark-bg flex items-center justify-center"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            aria-label="Delete todo"
          >
            <Trash2 className="w-5 h-5" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
});
