'use client';

import { useEffect, useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { scrollReveal, getSafeAnimationConfig } from '@/lib/animations';

interface StorytellingSection {
  id: string;
  title: string;
  subtitle: string;
  children: React.ReactNode;
  className?: string;
}

export default function StorytellingSection({
  id,
  title,
  subtitle,
  children,
  className = '',
}: StorytellingSection) {
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { once: false, amount: 0.3 });

  return (
    <motion.section
      id={id}
      ref={ref}
      className={`min-h-screen flex items-center justify-center py-20 px-6 ${className}`}
      initial="initial"
      animate={isInView ? 'animate' : 'initial'}
      variants={getSafeAnimationConfig(scrollReveal)}
    >
      <div className="max-w-6xl mx-auto w-full">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-6xl font-bold tracking-tight text-white mb-4">
            {title}
          </h2>
          <p className="text-xl md:text-2xl text-slate-400 font-light leading-relaxed">
            {subtitle}
          </p>
        </div>
        {children}
      </div>
    </motion.section>
  );
}
