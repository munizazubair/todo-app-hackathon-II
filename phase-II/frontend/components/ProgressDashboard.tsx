'use client';

import { motion } from 'framer-motion';
import { TodoStats } from '@/types/todo';
import { CheckCircle2, Clock, AlertCircle, ListTodo, TrendingUp, Target } from 'lucide-react';

interface ProgressDashboardProps {
  stats: TodoStats | null;
  isLoading: boolean;
}

export function ProgressDashboard({ stats, isLoading }: ProgressDashboardProps) {
  if (isLoading) {
    return <ProgressDashboardSkeleton />;
  }

  if (!stats) {
    return null;
  }

  const completionRate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;
  const circumference = 2 * Math.PI * 45; // radius = 45
  const strokeDashoffset = circumference - (completionRate / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="glass-card p-6 mb-8"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-text-primary flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-accent-cyan" />
            Progress Dashboard
          </h2>
          <p className="text-sm text-text-tertiary mt-1">Track your productivity</p>
        </div>

        {/* Streak indicator (placeholder for future) */}
        <div className="flex items-center gap-2 bg-accent-amber/10 px-3 py-1.5 rounded-full border border-accent-amber/20">
          <span className="text-lg">🔥</span>
          <span className="text-accent-amber font-semibold text-sm">Keep going!</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Circular Progress */}
        <div className="col-span-1 md:col-span-2 lg:col-span-1 flex justify-center items-center">
          <div className="relative w-32 h-32">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {/* Background circle */}
              <circle
                cx="50"
                cy="50"
                r="45"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-dark-tertiary"
              />
              {/* Progress circle */}
              <motion.circle
                cx="50"
                cy="50"
                r="45"
                stroke="url(#progressGradient)"
                strokeWidth="8"
                fill="none"
                strokeLinecap="round"
                initial={{ strokeDashoffset: circumference }}
                animate={{ strokeDashoffset }}
                transition={{ duration: 1, ease: 'easeOut' }}
                style={{ strokeDasharray: circumference }}
              />
              {/* Gradient definition */}
              <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#10B981" />
                  <stop offset="100%" stopColor="#06B6D4" />
                </linearGradient>
              </defs>
            </svg>
            {/* Center text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <motion.span
                className="text-3xl font-bold text-text-primary"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5, duration: 0.3 }}
              >
                {completionRate}%
              </motion.span>
              <span className="text-xs text-text-muted">Complete</span>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <StatCard
          icon={<ListTodo className="w-5 h-5" />}
          label="Total Tasks"
          value={stats.total}
          color="cyan"
          delay={0.1}
        />
        <StatCard
          icon={<CheckCircle2 className="w-5 h-5" />}
          label="Completed"
          value={stats.completed}
          color="emerald"
          delay={0.2}
        />
        <StatCard
          icon={<Clock className="w-5 h-5" />}
          label="Pending"
          value={stats.pending}
          color="amber"
          delay={0.3}
        />
      </div>

      {/* Overdue Warning */}
      {stats.overdue > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-4 flex items-center gap-3 bg-accent-red/10 border border-accent-red/20 rounded-lg px-4 py-3"
        >
          <AlertCircle className="w-5 h-5 text-accent-red flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-accent-red">
              {stats.overdue} overdue {stats.overdue === 1 ? 'task' : 'tasks'}
            </p>
            <p className="text-xs text-text-muted">Complete them to stay on track</p>
          </div>
        </motion.div>
      )}

      {/* Progress bar */}
      <div className="mt-6">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-text-secondary">Daily Progress</span>
          <span className="text-text-tertiary">
            {stats.completed}/{stats.total} tasks
          </span>
        </div>
        <div className="progress-bar">
          <motion.div
            className="progress-fill"
            initial={{ width: 0 }}
            animate={{ width: `${completionRate}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>
      </div>
    </motion.div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: number;
  color: 'cyan' | 'emerald' | 'amber' | 'red' | 'purple';
  delay?: number;
}

function StatCard({ icon, label, value, color, delay = 0 }: StatCardProps) {
  const colorClasses = {
    cyan: 'bg-accent-cyan/10 border-accent-cyan/20 text-accent-cyan',
    emerald: 'bg-accent-emerald/10 border-accent-emerald/20 text-accent-emerald',
    amber: 'bg-accent-amber/10 border-accent-amber/20 text-accent-amber',
    red: 'bg-accent-red/10 border-accent-red/20 text-accent-red',
    purple: 'bg-accent-purple/10 border-accent-purple/20 text-accent-purple',
  };

  const iconColorClasses = {
    cyan: 'text-accent-cyan',
    emerald: 'text-accent-emerald',
    amber: 'text-accent-amber',
    red: 'text-accent-red',
    purple: 'text-accent-purple',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.3, ease: 'easeOut' }}
      whileHover={{ scale: 1.02, transition: { duration: 0.2 } }}
      className={`stats-card ${colorClasses[color]} border`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-text-tertiary mb-1">{label}</p>
          <motion.p
            className="text-2xl font-bold text-text-primary"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: delay + 0.2, duration: 0.3 }}
          >
            {value}
          </motion.p>
        </div>
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          <span className={iconColorClasses[color]}>{icon}</span>
        </div>
      </div>
    </motion.div>
  );
}

function ProgressDashboardSkeleton() {
  return (
    <div className="glass-card p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="skeleton h-6 w-48 mb-2" />
          <div className="skeleton h-4 w-32" />
        </div>
        <div className="skeleton h-8 w-24 rounded-full" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="flex justify-center items-center">
          <div className="skeleton w-32 h-32 rounded-full" />
        </div>
        {[1, 2, 3].map((i) => (
          <div key={i} className="stats-card border border-border-primary">
            <div className="flex items-center justify-between">
              <div>
                <div className="skeleton h-3 w-16 mb-2" />
                <div className="skeleton h-8 w-12" />
              </div>
              <div className="skeleton h-10 w-10 rounded-lg" />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <div className="flex justify-between mb-2">
          <div className="skeleton h-4 w-24" />
          <div className="skeleton h-4 w-16" />
        </div>
        <div className="skeleton h-2 w-full rounded-full" />
      </div>
    </div>
  );
}
