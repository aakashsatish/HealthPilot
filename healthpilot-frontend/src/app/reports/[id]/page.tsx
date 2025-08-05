'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import AuthGuard from '@/components/auth/AuthGuard'
import { ReportDetails } from '@/types/upload'

export default function ReportDetailPage() {
  const params = useParams()
  const reportId = params.id as string
  const [report, setReport] = useState<ReportDetails | null>(null)
  const [loading, setLoading] = useState(true)

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

  if (loading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-4xl mx-auto py-8 px-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading report details...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (!report) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-4xl mx-auto py-8 px-4">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">Report Not Found</h1>
              <p className="text-gray-600">The report you&apos;re looking for doesn&apos;t exist.</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto py-8 px-4">
          <div className="mb-6">
            <a href="/history" className="text-blue-600 hover:text-blue-800 mb-4 inline-block">
              ← Back to History
            </a>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {report.original_filename}
            </h1>
            <p className="text-gray-600">
              Uploaded on {new Date(report.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="grid gap-6">
            {/* Report Summary */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Summary</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <span className="text-sm font-medium text-gray-500">Risk Level</span>
                  <div className="mt-1">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      report.risk_level === 'HIGH' ? 'bg-red-100 text-red-800' :
                      report.risk_level === 'MODERATE' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {report.risk_level}
                    </span>
                  </div>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">Abnormal Results</span>
                  <div className="mt-1 text-lg font-semibold text-gray-900">
                    {report.abnormal_count}
                  </div>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">Critical Results</span>
                  <div className="mt-1 text-lg font-semibold text-gray-900">
                    {report.critical_count}
                  </div>
                </div>
              </div>
              {report.summary && (
                <div className="mt-4">
                  <span className="text-sm font-medium text-gray-500">Analysis</span>
                  <p className="mt-1 text-gray-900">{report.summary}</p>
                </div>
              )}
            </div>

            {/* Lab Results */}
            {report.analysis_result?.results && (
              <div className="bg-white rounded-lg shadow">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">Lab Results</h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reference Range</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {report.analysis_result.results.map((result, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {result.original_name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {result.value} {result.unit}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {result.reference_range}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              result.classification === 'NORMAL' 
                                ? 'bg-green-100 text-green-800'
                                : result.classification === 'HIGH' || result.classification === 'LOW'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-red-100 text-red-800'
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
    </AuthGuard>
  )
}