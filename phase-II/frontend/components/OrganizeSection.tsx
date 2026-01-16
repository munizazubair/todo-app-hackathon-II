'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { staggerContainer, staggerItem } from '@/lib/animations';
import { Calendar, Clock, ListTodo } from 'lucide-react';

export default function OrganizeSection() {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: false, amount: 0.3 });

  const sections = [
    {
      title: 'Today',
      icon: Calendar,
      tasks: ['Review quarterly goals', 'Team standup at 10 AM'],
      color: 'accent-cyan',
    },
    {
      title: 'Upcoming',
      icon: Clock,
      tasks: ['Prepare presentation', 'Client meeting Friday'],
      color: 'accent-purple',
    },
    {
      title: 'Completed',
      icon: ListTodo,
      tasks: ['Morning workout', 'Code review'],
      color: 'accent-emerald',
    },
  ];

  return (
    <section
      id="organize"
      ref={ref}
      className="min-h-screen flex items-center justify-center py-20 px-6 bg-gradient-to-b from-dark-surface via-dark-bg to-slate-950"
    >
      <div className="max-w-6xl mx-auto w-full">
        <div className="text-center mb-16">
          <motion.h2
            className="text-4xl md:text-6xl font-bold tracking-tight text-white mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
            transition={{ duration: 0.5 }}
          >
            Organize Your{' '}
            <span className="bg-gradient-to-r from-accent-purple to-accent-emerald bg-clip-text text-transparent">
              Workflow
            </span>
          </motion.h2>
          <motion.p
            className="text-xl text-slate-400"
            initial={{ opacity: 0 }}
            animate={isInView ? { opacity: 1 } : { opacity: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Tasks automatically align into clear, actionable sections
          </motion.p>
        </div>

        <motion.div
          className="grid md:grid-cols-3 gap-6"
          variants={staggerContainer}
          initial="initial"
          animate={isInView ? 'animate' : 'initial'}
        >
          {sections.map((section, index) => {
            const Icon = section.icon;
            return (
              <motion.div
                key={section.title}
                variants={staggerItem}
                className="relative group"
                style={{ transformOrigin: 'top' }}
              >
                {/* Card */}
                <div className="bg-dark-surface/50 backdrop-blur-lg border border-slate-800 rounded-2xl p-6 h-full hover:border-slate-700 transition-all">
                  {/* Header */}
                  <div className="flex items-center space-x-3 mb-6">
                    <div className={`p-2 rounded-lg bg-${section.color}/10`}>
                      <Icon className={`w-6 h-6 text-${section.color}`} />
                    </div>
                    <h3 className="text-xl font-bold text-white">{section.title}</h3>
                  </div>

                  {/* Tasks */}
                  <div className="space-y-3">
                    {section.tasks.map((task, taskIndex) => (
                      <motion.div
                        key={taskIndex}
                        className="p-3 bg-dark-muted/30 rounded-lg border border-slate-700/30"
                        initial={{ x: -20, opacity: 0 }}
                        animate={
                          isInView
                            ? { x: 0, opacity: 1 }
                            : { x: -20, opacity: 0 }
                        }
                        transition={{
                          duration: 0.3,
                          delay: 0.4 + index * 0.1 + taskIndex * 0.05,
                        }}
                      >
                        <p className="text-sm text-slate-300">{task}</p>
                      </motion.div>
                    ))}
                  </div>

                  {/* Count badge */}
                  <motion.div
                    className="mt-4 inline-flex items-center space-x-2 text-sm text-slate-500"
                    initial={{ scale: 0 }}
                    animate={isInView ? { scale: 1 } : { scale: 0 }}
                    transition={{ duration: 0.3, delay: 0.6 + index * 0.1 }}
                  >
                    <span className="text-lg font-bold">{section.tasks.length}</span>
                    <span>tasks</span>
                  </motion.div>
                </div>

                {/* Parallax glow effect */}
                <motion.div
                  className={`absolute -inset-0.5 bg-gradient-to-r from-${section.color}/20 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity blur-xl -z-10`}
                  initial={{ opacity: 0 }}
                  animate={isInView ? { opacity: 0 } : { opacity: 0 }}
                />
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
