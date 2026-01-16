'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { CheckCircle2, TrendingUp, AlertCircle, Clock } from 'lucide-react';
import { TodoStats } from '@/types/todo';

interface ProgressSectionProps {
  stats: TodoStats | null;
  isLoading: boolean;
}

export default function ProgressSection({ stats, isLoading }: ProgressSectionProps) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: false, amount: 0.4 });

  const totalTasks = stats?.total || 0;
  const completedTasks = stats?.completed || 0;
  const pendingTasks = stats?.pending || 0;
  const overdueTasks = stats?.overdue || 0;
  const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  return (
    <section
      id="analytics"
      ref={ref}
      className="min-h-screen flex items-center justify-center py-20 px-6 bg-gradient-to-b from-dark-bg via-slate-950 to-dark-surface"
    >
      <div className="max-w-4xl mx-auto w-full">
        <div className="text-center mb-16">
          <motion.div
            className="inline-flex items-center space-x-2 mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
            transition={{ duration: 0.5 }}
          >
            <TrendingUp className="w-8 h-8 text-accent-emerald" />
            <h2 className="text-4xl md:text-6xl font-bold tracking-tight text-white">
              Track Your Progress
            </h2>
          </motion.div>
          <motion.p
            className="text-xl text-slate-400"
            initial={{ opacity: 0 }}
            animate={isInView ? { opacity: 1 } : { opacity: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Celebrate every completion, stay motivated
          </motion.p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Progress Ring */}
          <motion.div
            className="bg-dark-surface/50 backdrop-blur-lg border border-slate-800 rounded-2xl p-8 flex items-center justify-center"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <div className="relative w-64 h-64">
              {/* Background circle */}
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="128"
                  cy="128"
                  r="120"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-dark-muted"
                />
                {/* Progress circle */}
                <motion.circle
                  cx="128"
                  cy="128"
                  r="120"
                  stroke="url(#gradient)"
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                  strokeDasharray={2 * Math.PI * 120}
                  initial={{ strokeDashoffset: 2 * Math.PI * 120 }}
                  animate={
                    isInView
                      ? {
                          strokeDashoffset:
                            2 * Math.PI * 120 * (1 - progress / 100),
                        }
                      : { strokeDashoffset: 2 * Math.PI * 120 }
                  }
                  transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1] }}
                />
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="rgba(16, 185, 129, 0.8)" />
                    <stop offset="100%" stopColor="rgba(34, 211, 238, 0.8)" />
                  </linearGradient>
                </defs>
              </svg>

              {/* Center text */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <motion.div
                  className="text-6xl font-bold text-white"
                  key={completedTasks}
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  {Math.round(progress)}%
                </motion.div>
                <p className="text-slate-400 mt-2">Completed</p>
              </div>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0, x: 20 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 20 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            {[
              {
                label: 'Total Tasks',
                value: totalTasks,
                icon: <span className="text-4xl">📋</span>,
                color: 'text-white',
                borderColor: 'border-slate-800',
              },
              {
                label: 'Completed',
                value: completedTasks,
                icon: <CheckCircle2 className="w-10 h-10 text-accent-emerald" />,
                color: 'text-accent-emerald',
                borderColor: 'border-accent-emerald shadow-lg shadow-accent-emerald/10',
              },
              {
                label: 'Pending',
                value: pendingTasks,
                icon: <Clock className="w-10 h-10 text-accent-amber" />,
                color: 'text-accent-amber',
                borderColor: 'border-slate-800',
              },
              {
                label: 'Overdue',
                value: overdueTasks,
                icon: <AlertCircle className="w-10 h-10 text-accent-red" />,
                color: overdueTasks > 0 ? 'text-accent-red' : 'text-white',
                borderColor: overdueTasks > 0 ? 'border-accent-red shadow-lg shadow-accent-red/10' : 'border-slate-800',
              },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                className={`bg-dark-surface/50 backdrop-blur-lg border rounded-xl p-6 ${stat.borderColor}`}
                initial={{ opacity: 0, y: 20 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                transition={{ duration: 0.3, delay: 0.6 + index * 0.1 }}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">{stat.label}</p>
                    <motion.div
                      className={`text-4xl font-bold ${stat.color}`}
                      key={`${stat.label}-${stat.value}`}
                      initial={{ scale: 1.2 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                    >
                      {isLoading ? '-' : stat.value}
                    </motion.div>
                  </div>
                  <div>{stat.icon}</div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Progress message */}
        {!isLoading && totalTasks > 0 && (
          <motion.div
            className="mt-12 text-center"
            initial={{ opacity: 0 }}
            animate={isInView ? { opacity: 1 } : { opacity: 0 }}
            transition={{ delay: 1 }}
          >
            <motion.div
              className={`inline-flex items-center space-x-3 rounded-full px-6 py-3 ${
                progress >= 75
                  ? 'bg-accent-emerald/10 border border-accent-emerald/30'
                  : progress >= 50
                  ? 'bg-accent-cyan/10 border border-accent-cyan/30'
                  : 'bg-accent-amber/10 border border-accent-amber/30'
              }`}
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15 }}
            >
              <CheckCircle2 className={`w-6 h-6 ${
                progress >= 75 ? 'text-accent-emerald' : progress >= 50 ? 'text-accent-cyan' : 'text-accent-amber'
              }`} />
              <span className={`font-medium ${
                progress >= 75 ? 'text-accent-emerald' : progress >= 50 ? 'text-accent-cyan' : 'text-accent-amber'
              }`}>
                {progress >= 75
                  ? 'Excellent progress!'
                  : progress >= 50
                  ? 'Good momentum!'
                  : progress > 0
                  ? 'Keep going!'
                  : 'Start completing tasks!'}
              </span>
            </motion.div>
          </motion.div>
        )}
      </div>
    </section>
  );
}
