'use client';

import { useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';
import { Target } from 'lucide-react';

export default function FocusSection() {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: false, amount: 0.4 });
  const [focusedIndex, setFocusedIndex] = useState(1);

  const tasks = [
    'Review team feedback',
    'Complete project proposal',
    'Update documentation',
  ];

  return (
    <section
      id="focus"
      ref={ref}
      className="min-h-screen flex items-center justify-center py-20 px-6 bg-gradient-to-b from-slate-950 via-dark-surface to-dark-bg"
    >
      <div className="max-w-4xl mx-auto w-full">
        <div className="text-center mb-16">
          <motion.div
            className="inline-flex items-center space-x-2 mb-4"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={isInView ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.5 }}
          >
            <Target className="w-8 h-8 text-accent-purple" />
            <h2 className="text-4xl md:text-6xl font-bold tracking-tight text-white">
              Focus & Execute
            </h2>
          </motion.div>
          <motion.p
            className="text-xl text-slate-400"
            initial={{ opacity: 0 }}
            animate={isInView ? { opacity: 1 } : { opacity: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            One task at a time, distraction-free
          </motion.p>
        </div>

        {/* Task cards with focus effect */}
        <div className="space-y-6 relative">
          {tasks.map((task, index) => {
            const isFocused = index === focusedIndex;

            return (
              <motion.div
                key={index}
                className={`relative cursor-pointer transition-all ${
                  isFocused ? 'z-10' : 'z-0'
                }`}
                onClick={() => setFocusedIndex(index)}
                initial={{ opacity: 0, y: 20 }}
                animate={
                  isInView
                    ? {
                        opacity: isFocused ? 1 : 0.4,
                        y: 0,
                        filter: isFocused ? 'blur(0px)' : 'blur(2px)',
                        scale: isFocused ? 1.02 : 1,
                      }
                    : { opacity: 0, y: 20 }
                }
                transition={{
                  duration: 0.4,
                  delay: index * 0.1,
                  ease: [0.4, 0, 0.2, 1],
                }}
                whileHover={!isFocused ? { scale: 1.01 } : {}}
              >
                {/* Card */}
                <div
                  className={`bg-dark-surface/50 backdrop-blur-lg border rounded-2xl p-8 transition-all ${
                    isFocused
                      ? 'border-accent-purple shadow-2xl shadow-accent-purple/20'
                      : 'border-slate-800'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div
                        className={`w-4 h-4 rounded-full border-2 transition-all ${
                          isFocused
                            ? 'border-accent-purple bg-accent-purple/20'
                            : 'border-slate-600'
                        }`}
                      />
                      <span className="text-xl font-medium text-white">{task}</span>
                    </div>

                    {isFocused && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="px-3 py-1 bg-accent-purple/20 border border-accent-purple/30 rounded-full text-sm text-accent-purple font-medium"
                      >
                        In Focus
                      </motion.div>
                    )}
                  </div>
                </div>

                {/* Glow effect */}
                {isFocused && (
                  <motion.div
                    className="absolute -inset-1 bg-gradient-to-r from-accent-purple/30 to-accent-cyan/30 rounded-2xl blur-xl -z-10"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  />
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Focus tip */}
        <motion.p
          className="text-center text-slate-500 mt-8 text-sm"
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : { opacity: 0 }}
          transition={{ delay: 0.8 }}
        >
          Click any task to bring it into focus
        </motion.p>
      </div>
    </section>
  );
}
