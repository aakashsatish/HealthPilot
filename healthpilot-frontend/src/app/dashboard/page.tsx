'use client'

import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import Link from 'next/link'

export default function Dashboard() {
  const { user, signOut } = useUser()

  const handleLogout = async () => {
    await signOut()
  }

  return (
    <AuthGuard>
      <div className="min-h-screen gradient-bg relative overflow-hidden">
        {/* Organic background shapes */}
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        

        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          {/* Header with personality */}
          <div className="hero-text flex justify-between items-center mb-12">
            <div className="space-y-3">
              <div>
                <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-900 bg-clip-text text-transparent leading-tight">
                  HealthPilot
                </h1>
                <p className="text-xl text-muted-foreground font-light">Your Health Intelligence Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/upload"
                className="btn-primary bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-8 py-4 rounded-2xl font-bold hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
              >
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <span>Upload Report</span>
                </div>
              </Link>
              <Link
                href="/profile"
                className="btn-secondary bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-8 py-4 rounded-2xl font-bold hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
              >
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>Profile</span>
                </div>
              </Link>
              <button
                onClick={handleLogout}
                className="btn-secondary bg-gradient-to-r from-red-500 to-red-600 text-white px-8 py-4 rounded-2xl font-bold transition-all duration-300"
              >
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>Sign Out</span>
                </div>
              </button>
            </div>
          </div>

          {/* Stats Cards with personality */}
          <div className="feature-grid grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="feature-card gradient-card rounded-3xl p-8 transform rotate-1">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Total Reports</p>
                  <p className="text-3xl font-bold text-foreground">0</p>
                </div>
                <div className="icon-container">
                  <svg className="w-7 h-7 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
            </div>
            
            <div className="feature-card gradient-card rounded-3xl p-8 transform -rotate-1">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Health Score</p>
                  <p className="text-3xl font-bold text-foreground">--</p>
                </div>
                <div className="icon-container">
                  <svg className="w-7 h-7 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
            
            <div className="feature-card gradient-card rounded-3xl p-8 transform rotate-2">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Last Updated</p>
                  <p className="text-3xl font-bold text-foreground">--</p>
                </div>
                <div className="icon-container">
                  <svg className="w-7 h-7 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content with personality */}
          <div className="feature-card gradient-card rounded-3xl p-10">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-foreground">Recent Activity</h2>
              <Link href="/history" className="text-primary hover:text-accent transition-colors font-semibold">
                View All
              </Link>
            </div>
            
            <div className="text-center py-16">
              <div className="icon-container mx-auto mb-8">
                <svg className="w-12 h-12 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-foreground mb-4">No reports yet</h3>
              <p className="text-muted-foreground mb-8 max-w-lg mx-auto text-lg leading-relaxed">
                Upload your first lab report to get started with personalized health insights and AI-powered analysis.
              </p>
              <Link
                href="/upload"
                className="btn-primary inline-flex items-center space-x-3 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-10 py-5 rounded-2xl font-bold hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span>Upload Your First Report</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}