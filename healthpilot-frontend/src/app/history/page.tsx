'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import EmailModal from '@/components/ui/EmailModal'
import { ReportHistory } from '@/types/upload'

export default function HistoryPage() {
  const { user } = useUser()
  const [history, setHistory] = useState<ReportHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedReport, setSelectedReport] = useState<string | null>(null)
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [selectedReportId, setSelectedReportId] = useState<string>('')

  useEffect(() => {
    if (user) {
      fetchHistory()
    }
  }, [user])

  const fetchHistory = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/reports/history/${user?.id}`)
      const data = await response.json()
      
      if (data.success) {
        setHistory(data.history)
      }
    } catch (error) {
      console.error('Error fetching history:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel?.toUpperCase()) {
      case 'HIGH':
        return 'bg-red-500/20 text-red-400 border border-red-500/30'
      case 'MODERATE':
        return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
      case 'LOW':
        return 'bg-green-500/20 text-green-400 border border-green-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const handleDeleteReport = async (reportId: string) => {
    if (!confirm('Are you sure you want to delete this report? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/reports/${reportId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        // Refresh the history after successful deletion
        await fetchHistory()
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
      const response = await fetch(`http://localhost:8000/reports/${selectedReportId}/email`, {
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
      const response = await fetch(`http://localhost:8000/reports/${reportId}/download`)
      
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

  if (loading) {
    return (
      <AuthGuard>
        <div className="min-h-screen gradient-bg relative overflow-hidden">
          <div className="max-w-6xl mx-auto py-12 px-4">
            <div className="text-center">
              <div className="icon-container mx-auto mb-6 animate-pulse">
                <svg className="w-12 h-12 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <p className="text-xl text-gray-600 dark:text-gray-300 font-medium">Loading your history...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="min-h-screen gradient-bg relative overflow-hidden">
        {/* Organic background shapes */}
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        
        <div className="max-w-7xl mx-auto py-12 px-4">
          <div className="hero-text text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
              Your Lab Report History
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
              Track your health over time and compare results
            </p>
          </div>

          {history.length === 0 ? (
            <div className="feature-card gradient-card rounded-3xl p-12 text-center">
              <div className="icon-container mx-auto mb-6">
                <svg className="w-12 h-12 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">No reports yet</h3>
              <p className="text-gray-600 dark:text-gray-300 mb-8 text-lg leading-relaxed">Upload your first lab report to get started</p>
              <a
                href="/upload"
                className="btn-primary inline-flex items-center space-x-3 bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-8 py-4 rounded-2xl font-bold hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300"
              >
                Upload Report
              </a>
            </div>
          ) : (
            <div className="grid gap-8">
              {/* Statistics Summary with personality */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="feature-card gradient-card rounded-3xl p-8 transform rotate-1">
                  <div className="text-3xl font-bold text-blue-400 mb-2">{history.length}</div>
                  <div className="text-sm text-gray-300 font-medium">Total Reports</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform -rotate-1">
                  <div className="text-3xl font-bold text-green-400 mb-2">
                    {history.filter(r => r.risk_level === 'LOW').length}
                  </div>
                  <div className="text-sm text-gray-300 font-medium">Low Risk</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform rotate-2">
                  <div className="text-3xl font-bold text-yellow-400 mb-2">
                    {history.filter(r => r.risk_level === 'MODERATE').length}
                  </div>
                  <div className="text-sm text-gray-300 font-medium">Moderate Risk</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform -rotate-2">
                  <div className="text-3xl font-bold text-red-400 mb-2">
                    {history.filter(r => r.risk_level === 'HIGH').length}
                  </div>
                  <div className="text-sm text-gray-300 font-medium">High Risk</div>
                </div>
              </div>

              {/* Reports List with personality */}
              <div className="feature-card gradient-card rounded-3xl">
                <div className="px-8 py-6 border-b border-gray-700">
                  <h2 className="text-2xl font-bold text-white">Recent Reports</h2>
                </div>
                <div className="divide-y divide-gray-700">
                  {history.map((report) => (
                    <div key={report.id} className="p-6 hover:bg-gray-800/30">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <h3 className="text-lg font-medium text-white">
                              {report.original_filename}
                            </h3>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRiskLevelColor(report.risk_level)}`}>
                              {report.risk_level || 'UNKNOWN'}
                            </span>
                          </div>
                          <div className="mt-2 text-sm text-gray-300">
                            <span className="font-medium">Date:</span> {formatDate(report.created_at)}
                            {report.lab_name && (
                              <>
                                <span className="mx-2">•</span>
                                <span className="font-medium">Lab:</span> {report.lab_name}
                              </>
                            )}
                          </div>
                          {report.summary && (
                            <p className="mt-2 text-sm text-gray-300">{report.summary}</p>
                          )}
                          <div className="mt-2 flex space-x-4 text-sm text-gray-400">
                            <span>Abnormal: {report.abnormal_count || 0}</span>
                            <span>Critical: {report.critical_count || 0}</span>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setSelectedReport(report.id)}
                            className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500/20 hover:border-blue-500/30 transition-all duration-200"
                          >
                            <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                            View
                          </button>
                          <button
                            onClick={() => handleEmailReport(report.id)}
                            className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-green-500/10 text-green-400 border border-green-500/20 hover:bg-green-500/20 hover:border-green-500/30 transition-all duration-200"
                          >
                            <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            Email
                          </button>
                          <button
                            onClick={() => handleDownloadReport(report.id)}
                            className="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 hover:bg-purple-500/20 hover:border-purple-500/30 transition-all duration-200"
                          >
                            <svg className="w-3 h-3 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            Download
                          </button>
                          <button
                            onClick={() => handleDeleteReport(report.id)}
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
                  ))}
                </div>
              </div>
            </div>
          )}
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