'use client'

import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import EmailModal from '@/components/ui/EmailModal'
import { apiJson, apiCall, apiBlob } from '../../lib/api'
import Link from 'next/link'
import { useState, useEffect } from 'react'

interface DashboardStats {
  totalReports: number
  healthScore: string
  lastUpdated: string
  recentReports: unknown[]
}

export default function Dashboard() {
  const { user, signOut } = useUser()
  const [stats, setStats] = useState<DashboardStats>({
    totalReports: 0,
    healthScore: '--',
    lastUpdated: '--',
    recentReports: []
  })
  const [loading, setLoading] = useState(true)
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [selectedReportId, setSelectedReportId] = useState<string>('')

  useEffect(() => {
    if (user?.id) {
      fetchDashboardStats()
    }
  }, [user])

  const fetchDashboardStats = async () => {
    try {
      const data = await apiJson(`/reports/history/${user?.id}`)
      
      if (data.success && data.history) {
        setStats({
          totalReports: data.history.length,
          healthScore: data.history.length > 0 ? 'Good' : '--',
          lastUpdated: data.history.length > 0 ? 'Recently' : '--',
          recentReports: data.history.slice(0, 3) // Get last 3 reports
        })
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteReport = async (reportId: string) => {
    if (!confirm('Are you sure you want to delete this report? This action cannot be undone.')) {
      return
    }

    try {
      const response = await apiCall(`/reports/${reportId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        // Refresh the dashboard stats
        await fetchDashboardStats()
      } else {
        console.error('Failed to delete report')
        alert('Failed to delete report. Please try again.')
      }
    } catch (error) {
      console.error('Error deleting report:', error)
      alert('Error deleting report. Please try again.')
    }
  }

  const handleEmailReport = (reportId: string) => {
    setSelectedReportId(reportId)
    setIsEmailModalOpen(true)
  }

  const handleSendEmail = async (email: string) => {
    try {
      const response = await apiCall(`/reports/${selectedReportId}/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      })

      if (response.ok) {
        return { success: true, message: 'Report sent to your email successfully!' }
      } else {
        const errorData = await response.json()
        return { success: false, message: `Failed to send email: ${errorData.detail || 'Unknown error'}` }
      }
    } catch (error) {
      console.error('Error sending email:', error)
      return { success: false, message: 'Error sending email. Please try again.' }
    }
  }

  const handleDownloadReport = async (reportId: string) => {
    try {
      const response = await apiCall(`/reports/${reportId}/download`)
      
      if (response.ok) {
        // Get the filename from the response headers
        const contentDisposition = response.headers.get('content-disposition')
        let filename = `lab_report_${new Date().toISOString().split('T')[0]}.pdf`
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="(.+)"/)
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }
        
        // Create a blob from the PDF data
        const blob = await response.blob()
        
        // Create a download link
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = filename
        
        // Trigger download
        document.body.appendChild(link)
        link.click()
        
        // Cleanup
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } else {
        const errorData = await response.json()
        console.error(`Failed to download report: ${errorData.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Error downloading report:', error)
    }
  }

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
                  <p className="text-3xl font-bold text-foreground">
                    {loading ? '...' : stats.totalReports}
                  </p>
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
                  <p className="text-3xl font-bold text-foreground">
                    {loading ? '...' : stats.healthScore}
                  </p>
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
                  <p className="text-3xl font-bold text-foreground">
                    {loading ? '...' : stats.lastUpdated}
                  </p>
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
            
            {loading ? (
              <div className="text-center py-16">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                <p className="text-muted-foreground">Loading your reports...</p>
              </div>
            ) : stats.totalReports === 0 ? (
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
            ) : (
              <div className="space-y-6">
                <div className="grid gap-4">
                  {stats.recentReports.map((report: unknown, index: number) => {
                    const reportData = report as { id: string; original_filename?: string; created_at: string }
                    return (
                      <div key={index} className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="text-lg font-semibold text-white">
                              {reportData.original_filename || 'Lab Report'}
                            </h4>
                            <p className="text-gray-300 text-sm">
                              Uploaded on {new Date(reportData.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Link
                              href={`/reports/${reportData.id}`}
                              className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500/20 hover:border-blue-500/30 transition-all duration-200"
                            >
                              <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                              </svg>
                              View
                            </Link>
                            <button
                              onClick={() => handleEmailReport(reportData.id)}
                              className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-green-500/10 text-green-400 border border-green-500/20 hover:bg-green-500/20 hover:border-green-500/30 transition-all duration-200"
                            >
                              <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                              </svg>
                              Email
                            </button>
                            <button
                              onClick={() => handleDownloadReport(reportData.id)}
                              className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 hover:bg-purple-500/20 hover:border-purple-500/30 transition-all duration-200"
                            >
                              <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                              Download
                            </button>
                            <button
                              onClick={() => handleDeleteReport(reportData.id)}
                              className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 hover:border-red-500/30 transition-all duration-200"
                            >
                              <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                              Delete
                            </button>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
                <div className="text-center">
                  <Link
                    href="/upload"
                    className="btn-primary inline-flex items-center space-x-3 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-6 py-3 rounded-xl font-semibold hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <span>Upload Another Report</span>
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <EmailModal
        isOpen={isEmailModalOpen}
        onClose={() => setIsEmailModalOpen(false)}
        onSend={handleSendEmail}
      />
    </AuthGuard>
  )
}