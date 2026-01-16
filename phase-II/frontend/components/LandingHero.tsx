'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { scaleIn } from '@/lib/animations';
import { ArrowDown, Sparkles, Target, Zap } from 'lucide-react';

export default function LandingHero() {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: false, amount: 0.4 });

  const handleScrollToTasks = () => {
    const tasksSection = document.getElementById('tasks');
    if (tasksSection) {
      const offset = 80;
      const elementPosition = tasksSection.getBoundingClientRect().top + window.pageYOffset;
      window.scrollTo({
        top: elementPosition - offset,
        behavior: 'smooth',
      });
    }
  };

  return (
    <section
      id="dashboard"
      ref={ref}
      className="min-h-screen flex items-center justify-center py-20 px-6 bg-gradient-to-b from-dark-bg via-slate-950 to-dark-surface"
    >
      <div className="max-w-4xl mx-auto w-full text-center">
        <motion.div
          initial="initial"
          animate={isInView ? 'animate' : 'initial'}
          variants={scaleIn}
        >
          {/* Badge */}
          <motion.div
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent-purple/10 border border-accent-purple/20 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
            transition={{ delay: 0.1 }}
          >
            <Sparkles className="w-4 h-4 text-accent-purple" />
            <span className="text-sm font-medium text-accent-purple">Professional Task Management</span>
          </motion.div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-6">
            Capture What{' '}
            <span className="bg-gradient-to-r from-accent-cyan to-accent-purple bg-clip-text text-transparent">
              Matters
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-slate-400 mb-12 leading-relaxed max-w-2xl mx-auto">
            Transform chaos into clarity. Organize, prioritize, and accomplish your goals with ease.
          </p>
        </motion.div>

        {/* Feature highlights */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ delay: 0.3 }}
        >
          {[
            { icon: Target, label: 'Stay Focused', desc: 'Prioritize what matters' },
            { icon: Zap, label: 'Be Productive', desc: 'Track your progress' },
            { icon: Sparkles, label: 'Celebrate Wins', desc: 'Milestone rewards' },
          ].map((feature, index) => (
            <motion.div
              key={feature.label}
              className="p-6 rounded-2xl bg-dark-surface/30 border border-slate-800/50 backdrop-blur-sm"
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
              transition={{ delay: 0.4 + index * 0.1 }}
            >
              <feature.icon className="w-8 h-8 text-accent-cyan mb-3 mx-auto" />
              <h3 className="text-lg font-semibold text-white mb-1">{feature.label}</h3>
              <p className="text-sm text-slate-400">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ delay: 0.6 }}
        >
          <button
            onClick={handleScrollToTasks}
            className="group inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-accent-cyan to-accent-purple text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-accent-cyan/25 transition-all duration-300 hover:scale-105"
          >
            Get Started
            <ArrowDown className="w-5 h-5 group-hover:translate-y-1 transition-transform" />
          </button>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="mt-16"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <div className="inline-flex flex-col items-center">
            <span className="text-sm text-slate-500 mb-2">Scroll to manage tasks</span>
            <motion.div
              animate={{ y: [0, 8, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-6 h-10 rounded-full border-2 border-slate-700 flex items-start justify-center p-2"
            >
              <motion.div className="w-1.5 h-1.5 bg-accent-cyan rounded-full" />
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
