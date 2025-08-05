'use client'

import Link from 'next/link'
import { useUser } from '@/contexts/UserContext'

export default function Home() {
  const { user, signOut } = useUser()

  const handleLogout = async () => {
    await signOut()
  }

  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden">
      {/* Organic background shapes */}
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      

      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          {/* Hero Section with personality */}
          <div className="hero-text mb-12">
            <div className="text-center mb-4">
              <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-900 bg-clip-text text-transparent leading-tight">
                HealthPilot
              </h1>
            </div>
            <p className="text-2xl md:text-3xl text-muted-foreground mb-4 font-light">
              Your Health Intelligence Platform
            </p>
            <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Upload your lab reports and get AI-powered analysis with personalized recommendations in plain English.
            </p>
          </div>

          {/* Asymmetric Features Grid */}
          <div className="asymmetric-grid mb-12">
            <div className="feature-card gradient-card p-8 rounded-3xl transform rotate-1">
              <div className="icon-container mb-6">
                <svg className="w-8 h-8 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-foreground">AI-Powered Analysis</h3>
              <p className="text-muted-foreground text-base leading-relaxed">
                Get intelligent insights from your lab results with our advanced AI system that understands your unique health profile.
              </p>
            </div>
            
            <div className="feature-card gradient-card p-8 rounded-3xl transform -rotate-1">
              <div className="icon-container mb-6">
                <svg className="w-8 h-8 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-foreground">Personalized Insights</h3>
              <p className="text-muted-foreground text-base leading-relaxed">
                Receive recommendations tailored to your age, sex, medical history, and lifestyle factors for truly personalized care.
              </p>
            </div>
            
            <div className="feature-card gradient-card p-8 rounded-3xl transform rotate-2">
              <div className="icon-container mb-6">
                <svg className="w-8 h-8 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-foreground">Track Progress</h3>
              <p className="text-muted-foreground text-base leading-relaxed">
                Monitor your health trends over time with detailed history, comparisons, and early warning signals.
              </p>
            </div>
          </div>

          {/* Call to Action with personality */}
          <div className="cta-section space-y-6">
            {user ? (
              // Authenticated user navigation
              <div className="flex flex-col sm:flex-row gap-6 justify-center">
                <Link 
                  href="/dashboard"
                  className="btn-primary inline-flex items-center space-x-3 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                  </svg>
                  <span>Go to Dashboard</span>
                </Link>
                <Link 
                  href="/upload"
                  className="btn-secondary inline-flex items-center space-x-3 bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <span>Upload Report</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="btn-secondary inline-flex items-center space-x-3 bg-gradient-to-r from-red-500 to-red-600 text-white px-10 py-5 rounded-2xl font-bold text-lg transition-all duration-300"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>Sign Out</span>
                </button>
              </div>
            ) : (
              // Unauthenticated user navigation
              <div className="flex flex-col sm:flex-row gap-6 justify-center">
                <Link 
                  href="/auth/login"
                  className="btn-primary inline-flex items-center space-x-3 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  <span>Sign In</span>
                </Link>
                <Link 
                  href="/auth/signup"
                  className="btn-secondary inline-flex items-center space-x-3 bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                  <span>Sign Up</span>
                </Link>
              </div>
            )}
            
            <div className="text-muted-foreground">
              {user ? (
                <p className="text-lg font-medium">Welcome back, <span className="font-bold text-foreground">{user.email}</span>!</p>
              ) : (
                <p className="text-lg font-medium">Get started by creating an account</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}