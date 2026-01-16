import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Background Layers (Research: Avoid pure black)
        dark: {
          bg: '#0A0A0F',
          surface: '#121218',
          tertiary: '#1A1A24',
          muted: '#2a2a2a',
        },
        // Accent Colors (WCAG AA Compliant)
        accent: {
          cyan: '#06B6D4',
          'cyan-dark': '#0891B2',
          purple: '#8B5CF6',
          'purple-dark': '#7C3AED',
          emerald: '#10B981',
          'emerald-dark': '#059669',
          amber: '#F59E0B',
          'amber-dark': '#D97706',
          red: '#EF4444',
          'red-dark': '#DC2626',
        },
        // Priority Colors (P1-P4 System)
        priority: {
          p1: '#EF4444',
          'p1-bg': 'rgba(239, 68, 68, 0.1)',
          p2: '#F59E0B',
          'p2-bg': 'rgba(245, 158, 11, 0.1)',
          p3: '#06B6D4',
          'p3-bg': 'rgba(6, 182, 212, 0.1)',
          p4: '#6B7280',
          'p4-bg': 'rgba(107, 114, 128, 0.1)',
        },
        // Text Colors (WCAG AA Compliant)
        text: {
          primary: '#F9FAFB',
          secondary: '#D1D5DB',
          tertiary: '#9CA3AF',
          muted: '#6B7280',
        },
        // Glass & Border
        glass: {
          DEFAULT: 'rgba(255, 255, 255, 0.05)',
          hover: 'rgba(255, 255, 255, 0.08)',
        },
        border: {
          primary: 'rgba(255, 255, 255, 0.1)',
          secondary: 'rgba(255, 255, 255, 0.05)',
        },
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        'slide-up': 'slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'scale-in': 'scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'pulse-subtle': 'pulseSubtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'draw-checkmark': 'drawCheckmark 0.5s ease-out forwards',
        'count-up': 'countUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        drawCheckmark: {
          '0%': { strokeDashoffset: '100' },
          '100%': { strokeDashoffset: '0' },
        },
        countUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
export default config
