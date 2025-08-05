'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import { ReportHistory } from '@/types/upload'

export default function HistoryPage() {
  const { user } = useUser()
  const [history, setHistory] = useState<ReportHistory[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedReport, setSelectedReport] = useState<string | null>(null)

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
        return 'bg-red-100 text-red-800'
      case 'MODERATE':
        return 'bg-yellow-100 text-yellow-800'
      case 'LOW':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
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
                  <div className="text-3xl font-bold text-blue-600 mb-2">{history.length}</div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 font-medium">Total Reports</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform -rotate-1">
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    {history.filter(r => r.risk_level === 'LOW').length}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 font-medium">Low Risk</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform rotate-2">
                  <div className="text-3xl font-bold text-yellow-600 mb-2">
                    {history.filter(r => r.risk_level === 'MODERATE').length}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 font-medium">Moderate Risk</div>
                </div>
                <div className="feature-card gradient-card rounded-3xl p-8 transform -rotate-2">
                  <div className="text-3xl font-bold text-red-600 mb-2">
                    {history.filter(r => r.risk_level === 'HIGH').length}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300 font-medium">High Risk</div>
                </div>
              </div>

              {/* Reports List with personality */}
              <div className="feature-card gradient-card rounded-3xl">
                <div className="px-8 py-6 border-b border-gray-200 dark:border-gray-700">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Recent Reports</h2>
                </div>
                <div className="divide-y divide-gray-200">
                  {history.map((report) => (
                    <div key={report.id} className="p-6 hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <h3 className="text-lg font-medium text-gray-900">
                              {report.original_filename}
                            </h3>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getRiskLevelColor(report.risk_level)}`}>
                              {report.risk_level || 'UNKNOWN'}
                            </span>
                          </div>
                          <div className="mt-2 text-sm text-gray-600">
                            <span className="font-medium">Date:</span> {formatDate(report.created_at)}
                            {report.lab_name && (
                              <>
                                <span className="mx-2">•</span>
                                <span className="font-medium">Lab:</span> {report.lab_name}
                              </>
                            )}
                          </div>
                          {report.summary && (
                            <p className="mt-2 text-sm text-gray-700">{report.summary}</p>
                          )}
                          <div className="mt-2 flex space-x-4 text-sm text-gray-500">
                            <span>Abnormal: {report.abnormal_count || 0}</span>
                            <span>Critical: {report.critical_count || 0}</span>
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setSelectedReport(report.id)}
                            className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 font-medium"
                          >
                            View Details
                          </button>
                          <button
                            onClick={() => window.open(`/reports/${report.id}`, '_blank')}
                            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                          >
                            Compare
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
    </AuthGuard>
  )
}