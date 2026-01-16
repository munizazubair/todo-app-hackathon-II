'use client';

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center px-6 bg-gradient-to-b from-dark-bg to-dark-surface">
      <motion.div
        className="max-w-2xl w-full text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Error Icon */}
        <motion.div
          className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-500/10 border border-red-500/20 mb-8"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
        >
          <AlertTriangle className="w-10 h-10 text-red-400" />
        </motion.div>

        {/* Error Title */}
        <motion.h1
          className="text-4xl md:text-5xl font-bold text-white mb-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          Oops! Something went wrong
        </motion.h1>

        {/* Error Message */}
        <motion.p
          className="text-xl text-slate-400 mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          We encountered an unexpected error. Don't worry, your todos are safe.
        </motion.p>

        {/* Error Details (Development Only) */}
        {process.env.NODE_ENV === 'development' && (
          <motion.div
            className="glass-morphism rounded-xl p-6 mb-8 text-left"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <h3 className="text-sm font-medium text-slate-300 mb-2">Error Details:</h3>
            <p className="text-sm text-red-400 font-mono break-all">
              {error.message || 'Unknown error'}
            </p>
            {error.digest && (
              <p className="text-xs text-slate-500 font-mono mt-2">
                Error ID: {error.digest}
              </p>
            )}
          </motion.div>
        )}

        {/* Action Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <button
            onClick={reset}
            className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-accent-cyan to-accent-purple text-white rounded-lg font-medium hover:shadow-lg hover:shadow-accent-cyan/20 transition-all"
          >
            <RefreshCw className="w-5 h-5" />
            Try Again
          </button>
          <a
            href="/"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 glass-morphism text-slate-300 rounded-lg font-medium hover:border-accent-cyan/50 transition-all"
          >
            <Home className="w-5 h-5" />
            Go Home
          </a>
        </motion.div>

        {/* Help Text */}
        <motion.p
          className="text-sm text-slate-500 mt-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          If the problem persists, please refresh the page or contact support.
        </motion.p>
      </motion.div>
    </div>
  );
}
