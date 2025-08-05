'use client'

import { useTheme } from '@/contexts/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className="fixed top-4 right-4 z-50 p-3 rounded-full bg-transparent backdrop-blur-sm border border-gray-300 dark:border-gray-600 shadow-lg hover:bg-gray-100/50 dark:hover:bg-gray-800/50 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95"
      aria-label="Toggle theme"
    >
      <div className="relative w-5 h-5">
        {/* Sun icon - white in dark mode */}
        <svg 
          className={`absolute inset-0 w-5 h-5 transition-all duration-300 ease-in-out ${
            theme === 'dark' 
              ? 'opacity-100 rotate-0 scale-100 text-white' 
              : 'opacity-0 -rotate-90 scale-75'
          }`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        
        {/* Moon icon - black in light mode */}
        <svg 
          className={`absolute inset-0 w-5 h-5 transition-all duration-300 ease-in-out ${
            theme === 'light' 
              ? 'opacity-100 rotate-0 scale-100 text-gray-900' 
              : 'opacity-0 rotate-90 scale-75'
          }`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </div>
    </button>
  )
} 