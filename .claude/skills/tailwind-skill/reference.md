# TailwindSkill Reference Guide

Complete reference documentation for Tailwind CSS integration in Next.js applications.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Global Styles](#global-styles)
5. [Utility Classes](#utility-classes)
6. [Responsive Design](#responsive-design)
7. [Dark Mode](#dark-mode)
8. [Custom Components](#custom-components)
9. [Best Practices](#best-practices)

---

## Overview

Tailwind CSS is a utility-first CSS framework that enables rapid UI development with pre-defined classes.

### Key Benefits

- **Utility-First**: Build designs directly in HTML/JSX with utility classes
- **Responsive**: Mobile-first responsive design system
- **Customizable**: Extensive theme configuration options
- **Performance**: Purges unused CSS in production
- **Consistency**: Enforces design system through configuration
- **Developer Experience**: IntelliSense support, no context switching

### Version Compatibility

- **Tailwind CSS**: 3.0+
- **Next.js**: 14.0+
- **React**: 18.0+
- **TypeScript**: 5.0+

---

## Installation

### Step 1: Install Dependencies

```bash
npm install -D tailwindcss postcss autoprefixer
```

### Step 2: Initialize Tailwind

```bash
npx tailwindcss init -p
```

This creates:
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration

### Step 3: Configure TypeScript (Recommended)

Rename `tailwind.config.js` to `tailwind.config.ts` for type safety:

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

export default config
```

### Step 4: Create Global Styles

Create `app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 5: Import Global Styles

In `app/layout.tsx`:

```typescript
import './globals.css'
```

---

## Configuration

### Content Paths

Specify which files Tailwind should scan for class names:

```typescript
content: [
  './pages/**/*.{js,ts,jsx,tsx,mdx}',
  './components/**/*.{js,ts,jsx,tsx,mdx}',
  './app/**/*.{js,ts,jsx,tsx,mdx}',
  './src/**/*.{js,ts,jsx,tsx,mdx}',
]
```

### Theme Extension

Extend the default theme with custom values:

```typescript
theme: {
  extend: {
    // Custom colors
    colors: {
      primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        200: '#bfdbfe',
        300: '#93c5fd',
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        800: '#1e40af',
        900: '#1e3a8a',
      },
      accent: '#f59e0b',
    },

    // Custom fonts
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
      mono: ['Fira Code', 'monospace'],
    },

    // Custom spacing
    spacing: {
      '18': '4.5rem',
      '88': '22rem',
      '128': '32rem',
    },

    // Custom border radius
    borderRadius: {
      '4xl': '2rem',
    },

    // Custom breakpoints
    screens: {
      'xs': '475px',
      '3xl': '1920px',
    },

    // Custom animations
    animation: {
      'fade-in': 'fadeIn 0.5s ease-in',
      'slide-up': 'slideUp 0.3s ease-out',
    },

    keyframes: {
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' },
      },
      slideUp: {
        '0%': { transform: 'translateY(10px)', opacity: '0' },
        '100%': { transform: 'translateY(0)', opacity: '1' },
      },
    },
  },
}
```

### Plugins

Add official Tailwind plugins:

```typescript
plugins: [
  require('@tailwindcss/forms'),
  require('@tailwindcss/typography'),
  require('@tailwindcss/aspect-ratio'),
  require('@tailwindcss/container-queries'),
]
```

Install plugins:
```bash
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
```

---

## Global Styles

### Base Styles

Use `@layer base` for global element styles:

```css
@layer base {
  h1 {
    @apply text-4xl font-bold;
  }

  h2 {
    @apply text-3xl font-semibold;
  }

  h3 {
    @apply text-2xl font-semibold;
  }

  a {
    @apply text-blue-600 hover:text-blue-800 underline;
  }
}
```

### Component Styles

Use `@layer components` for reusable component classes:

```css
@layer components {
  .btn {
    @apply px-4 py-2 rounded-lg font-medium transition-colors;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600;
  }

  .btn-secondary {
    @apply btn bg-gray-500 text-white hover:bg-gray-600;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }

  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
}
```

### Utility Styles

Use `@layer utilities` for custom utilities:

```css
@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
}
```

### CSS Variables

Define CSS variables for theming:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --border: 214.3 31.8% 91.4%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
  }
}
```

---

## Utility Classes

### Layout

```typescript
// Container
<div className="container mx-auto px-4">

// Flexbox
<div className="flex items-center justify-between">
<div className="flex flex-col gap-4">

// Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Positioning
<div className="relative">
<div className="absolute top-0 right-0">
<div className="fixed bottom-4 right-4">
```

### Spacing

```typescript
// Padding
<div className="p-4">         // All sides
<div className="px-4 py-2">   // Horizontal & Vertical
<div className="pt-4 pb-2">   // Top & Bottom

// Margin
<div className="m-4">         // All sides
<div className="mx-auto">     // Horizontal center
<div className="mt-4 mb-2">   // Top & Bottom

// Gap
<div className="flex gap-4">
<div className="grid gap-x-4 gap-y-2">
```

### Typography

```typescript
// Font size
<h1 className="text-4xl">
<p className="text-base">
<small className="text-sm">

// Font weight
<span className="font-bold">
<span className="font-semibold">
<span className="font-normal">

// Text color
<p className="text-gray-900">
<p className="text-blue-500">
<p className="text-red-600">

// Text alignment
<p className="text-left">
<p className="text-center">
<p className="text-right">
```

### Colors

```typescript
// Background
<div className="bg-white">
<div className="bg-gray-100">
<div className="bg-blue-500">

// Text
<p className="text-gray-900">
<p className="text-white">

// Border
<div className="border border-gray-300">
<div className="border-2 border-blue-500">
```

### Borders & Shadows

```typescript
// Border radius
<div className="rounded">
<div className="rounded-lg">
<div className="rounded-full">

// Shadows
<div className="shadow-sm">
<div className="shadow-md">
<div className="shadow-lg">
```

---

## Responsive Design

Tailwind uses a mobile-first breakpoint system:

### Breakpoints

| Prefix | Min Width | Description |
|--------|-----------|-------------|
| `sm:` | 640px | Small devices |
| `md:` | 768px | Medium devices |
| `lg:` | 1024px | Large devices |
| `xl:` | 1280px | Extra large devices |
| `2xl:` | 1536px | 2X large devices |

### Usage Examples

```typescript
// Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

// Responsive text size
<h1 className="text-2xl md:text-4xl lg:text-6xl">

// Responsive padding
<div className="p-4 md:p-8 lg:p-12">

// Responsive display
<div className="hidden md:block">

// Responsive flex direction
<div className="flex flex-col md:flex-row">
```

---

## Dark Mode

### Enable Dark Mode

In `tailwind.config.ts`:

```typescript
const config: Config = {
  darkMode: 'class', // or 'media'
  // ...
}
```

### Using Dark Mode Classes

```typescript
// Background colors
<div className="bg-white dark:bg-gray-900">

// Text colors
<p className="text-gray-900 dark:text-white">

// Borders
<div className="border-gray-200 dark:border-gray-700">

// Complex example
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700">
```

### Toggle Dark Mode

```typescript
'use client'

import { useState, useEffect } from 'react'

export default function ThemeToggle() {
  const [darkMode, setDarkMode] = useState(false)

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-gray-700"
    >
      {darkMode ? '☀️ Light' : '🌙 Dark'}
    </button>
  )
}
```

---

## Custom Components

### Form Components

```typescript
// Input
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
  placeholder="Enter text..."
/>

// Select
<select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
  <option>Option 1</option>
  <option>Option 2</option>
</select>

// Textarea
<textarea
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
  rows={4}
  placeholder="Enter message..."
/>

// Checkbox
<input
  type="checkbox"
  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
/>
```

### Layout Components

```typescript
// Container
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

// Section
<section className="py-12 bg-gray-50">

// Grid Layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

---

## Best Practices

### 1. Use Consistent Spacing

Stick to Tailwind's spacing scale (4px increments):
```typescript
// Good
<div className="p-4 gap-2">

// Avoid arbitrary values
<div className="p-[17px]">
```

### 2. Extract Component Classes

For repeated patterns, create component classes:
```css
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600;
  }
}
```

### 3. Use Semantic Color Names

```typescript
// Good
colors: {
  primary: '#3b82f6',
  secondary: '#6b7280',
}

// Avoid
colors: {
  blue: '#3b82f6',
}
```

### 4. Leverage Responsive Utilities

```typescript
<div className="text-sm md:text-base lg:text-lg">
```

### 5. Group Related Classes

```typescript
// Layout
<div className="flex items-center justify-between">
// Spacing
<div className="p-4 m-2 gap-4">
// Colors
<div className="bg-white text-gray-900 border-gray-200">
```

### 6. Use @apply Sparingly

Only use `@apply` for component classes, not in JSX:
```typescript
// Good (in CSS)
.btn { @apply px-4 py-2; }

// Avoid (in JSX)
// Use utility classes directly instead
```

---

## Performance Optimization

### Purge Unused CSS

Tailwind automatically purges unused CSS in production. Ensure your content paths are correct:

```typescript
content: [
  './app/**/*.{js,ts,jsx,tsx,mdx}',
  './components/**/*.{js,ts,jsx,tsx,mdx}',
]
```

### JIT Mode

Tailwind CSS uses Just-In-Time mode by default (v3+), generating styles on-demand.

---

**Skill**: TailwindSkill
**Version**: 1.0.0
**Updated**: 2025-12-31
