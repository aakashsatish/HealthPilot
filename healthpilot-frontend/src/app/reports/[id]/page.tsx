'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import AuthGuard from '@/components/auth/AuthGuard'
import EmailModal from '@/components/ui/EmailModal'
import { ReportDetails } from '@/types/upload'

export default function ReportDetailPage() {
  const params = useParams()
  const reportId = params.id as string
  const [report, setReport] = useState<ReportDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)

  useEffect(() => {
    fetchReportDetails()
  }, [reportId])

  const fetchReportDetails = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/reports/${reportId}`)
      const data = await response.json()
      
      if (data.success) {
        setReport(data.report)
      }
    } catch (error) {
      console.error('Error fetching report details:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteReport = async () => {
    if (!confirm('Are you sure you want to delete this report? This action cannot be undone.')) {
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/reports/${reportId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        // Redirect to history page after successful deletion
        window.location.href = '/history'
      } else {
        console.error('Failed to delete report')
        alert('Failed to delete report. Please try again.')
      }
    } catch (error) {
      console.error('Error deleting report:', error)
      alert('Error deleting report. Please try again.')
    }
  }

  const handleEmailReport = () => {
    setIsEmailModalOpen(true)
  }

  const handleSendEmail = async (email: string) => {
    try {
      const response = await fetch(`http://localhost:8000/reports/${reportId}/email`, {
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

  const handleDownloadReport = async () => {
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
        <div className="min-h-screen gradient-bg">
          <div className="max-w-4xl mx-auto py-8 px-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto"></div>
              <p className="mt-4 text-gray-300">Loading report details...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (!report) {
    return (
      <AuthGuard>
        <div className="min-h-screen gradient-bg">
          <div className="max-w-4xl mx-auto py-8 px-4">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-white mb-4">Report Not Found</h1>
              <p className="text-gray-300">The report you&apos;re looking for doesn&apos;t exist.</p>
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
        
        <div className="max-w-4xl mx-auto py-8 px-4">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <a href="/history" className="text-blue-400 hover:text-blue-300 inline-block font-medium">
                ← Back to History
              </a>
              <div className="flex items-center space-x-3">
                <button
                  onClick={handleEmailReport}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg bg-green-500/10 text-green-400 border border-green-500/20 hover:bg-green-500/20 hover:border-green-500/30 transition-all duration-200"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Email Report
                </button>
                <button
                  onClick={handleDownloadReport}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 hover:bg-purple-500/20 hover:border-purple-500/30 transition-all duration-200"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download Report
                </button>
                <button
                  onClick={handleDeleteReport}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 hover:border-red-500/30 transition-all duration-200"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete Report
                </button>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              {report.original_filename}
            </h1>
            <p className="text-gray-300">
              Uploaded on {new Date(report.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="grid gap-6">
            {/* Report Summary */}
            <div className="feature-card gradient-card rounded-3xl p-8">
              <h2 className="text-xl font-semibold text-white mb-6">Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <span className="text-sm font-medium text-gray-300">Risk Level</span>
                  <div className="mt-2">
                    <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${
                      report.risk_level === 'HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                      report.risk_level === 'MODERATE' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                      'bg-green-500/20 text-green-400 border border-green-500/30'
                    }`}>
                      {report.risk_level}
                    </span>
                  </div>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-300">Abnormal Results</span>
                  <div className="mt-2 text-lg font-semibold text-white">
                    {report.abnormal_count}
                  </div>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-300">Critical Results</span>
                  <div className="mt-2 text-lg font-semibold text-white">
                    {report.critical_count}
                  </div>
                </div>
              </div>
              {report.summary && (
                <div className="mt-6">
                  <span className="text-sm font-medium text-gray-300">Analysis</span>
                  <p className="mt-2 text-gray-300 leading-relaxed">{report.summary}</p>
                </div>
              )}
            </div>

            {/* Lab Results */}
            {report.analysis_result?.results && (
              <div className="feature-card gradient-card rounded-3xl">
                <div className="px-8 py-6 border-b border-gray-700">
                  <h2 className="text-xl font-semibold text-white">Lab Results</h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-700">
                    <thead className="bg-gray-800/50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Test</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Value</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Reference Range</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Status</th>
                      </tr>
                    </thead>
                    <tbody className="bg-gray-800/30 divide-y divide-gray-700">
                      {report.analysis_result.results.map((result, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-800/30' : 'bg-gray-700/30'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">
                            {result.original_name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                            {result.value} {result.unit}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                            {result.reference_range}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              result.classification === 'NORMAL' 
                                ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                                : result.classification === 'HIGH' || result.classification === 'LOW'
                                ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                                : 'bg-red-500/20 text-red-400 border border-red-500/30'
                            }`}>
                              {result.classification}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
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