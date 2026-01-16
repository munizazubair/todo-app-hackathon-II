'use client';

import { useState, useEffect } from 'react';
import { motion, useScroll } from 'framer-motion';
import Link from 'next/link';

interface NavItem {
  label: string;
  href: string;
  id: string;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', href: '#dashboard', id: 'dashboard' },
  { label: 'Tasks', href: '#tasks', id: 'tasks' },
  { label: 'Analytics', href: '#analytics', id: 'analytics' },
];

export default function StickyHeader() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [isScrolled, setIsScrolled] = useState(false);
  const { scrollY } = useScroll();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);

      // Determine active section based on scroll position
      const sections = navItems.map(item => document.getElementById(item.id));
      const scrollPosition = window.scrollY + 100;

      for (let i = sections.length - 1; i >= 0; i--) {
        const section = sections[i];
        if (section && section.offsetTop <= scrollPosition) {
          setActiveSection(navItems[i].id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault();
    const targetId = href.replace('#', '');
    const element = document.getElementById(targetId);

    if (element) {
      const offset = 80; // Header height offset
      const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
      const offsetPosition = elementPosition - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  return (
    <motion.header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? 'bg-dark-surface/80 backdrop-blur-xl shadow-lg'
          : 'bg-transparent'
      }`}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
    >
      <nav className="container mx-auto px-6 py-4" role="navigation" aria-label="Main navigation">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link
            href="/"
            className="text-2xl font-bold tracking-tight text-white hover:text-accent-cyan transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:ring-offset-2 focus:ring-offset-dark-bg rounded-lg"
            aria-label="TodoFlow home"
          >
            <span className="bg-gradient-to-r from-accent-cyan to-accent-purple bg-clip-text text-transparent">
              Todo
            </span>
            <span className="text-white">Flow</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-1" role="menu">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={item.href}
                onClick={(e) => handleNavClick(e, item.href)}
                role="menuitem"
                aria-current={activeSection === item.id ? 'page' : undefined}
                aria-label={`Navigate to ${item.label} section`}
                className={`relative px-4 py-2 text-sm font-medium transition-colors rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:ring-offset-2 focus:ring-offset-dark-bg ${
                  activeSection === item.id
                    ? 'text-white'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {item.label}

                {/* Active indicator */}
                {activeSection === item.id && (
                  <motion.div
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-accent-cyan to-accent-purple rounded-full"
                    layoutId="activeSection"
                    transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
                  />
                )}

                {/* Glow effect on active */}
                {activeSection === item.id && (
                  <motion.div
                    className="absolute inset-0 bg-accent-cyan/10 rounded-lg -z-10"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  />
                )}
              </a>
            ))}
          </div>

          {/* Skip to content link (accessibility) */}
          <a
            href="#main-content"
            className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-accent-cyan focus:text-dark-bg focus:rounded-lg focus:ring-2 focus:ring-accent-cyan focus:ring-offset-2 focus:ring-offset-dark-bg"
          >
            Skip to content
          </a>
        </div>
      </nav>
    </motion.header>
  );
}
