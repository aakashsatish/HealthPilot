'use client'

import { useState, useEffect } from 'react'
import { AnalysisResult } from '@/types/upload'

interface AnalysisResultsProps {
  result: {
    job?: {
      job_id: string
    }
  }
  isProcessing: boolean
  onAnalysisComplete: (analysis: AnalysisResult) => void
}

export default function AnalysisResults({ result, isProcessing, onAnalysisComplete }: AnalysisResultsProps) {
  const [jobStatus, setJobStatus] = useState('queued')
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)

  useEffect(() => {
    if (result?.job?.job_id) {
      checkJobStatus()
    }
  }, [result])

  const checkJobStatus = async () => {
    try {
      const response = await fetch(`http://localhost:8000/jobs/${result.job?.job_id}`)
      const jobData = await response.json()
      
      setJobStatus(jobData.status)
      
      if (jobData.status === 'finished' && jobData.result) {
        setAnalysis(jobData.result.analysis)
        onAnalysisComplete(jobData.result.analysis)
      } else if (jobData.status === 'failed') {
        console.error('Job failed:', jobData.result)
      } else if (isProcessing) {
        // Check again in 2 seconds
        setTimeout(checkJobStatus, 2000)
      }
    } catch (error) {
      console.error('Error checking job status:', error)
    }
  }

  if (isProcessing) {
    return (
      <div className="max-w-2xl mx-auto text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing your lab report...</h2>
        <p className="text-gray-600">This may take a few moments</p>
        <div className="mt-4 text-sm text-gray-500">
          Status: {jobStatus}
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Upload Complete</h2>
        <p className="text-gray-600">Your file has been uploaded successfully.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Results</h2>
        
        {/* Summary */}
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Summary</h3>
          <p className="text-blue-800">{analysis.summary}</p>
        </div>

        {/* Risk Assessment */}
        {analysis.risk_assessment && (
        <div className="mb-6 p-4 bg-orange-50 rounded-lg border-l-4 border-orange-400">
            <h3 className="text-lg font-semibold text-orange-900 mb-2">Risk Assessment</h3>
            <div className="mb-3">
            <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${
                analysis.risk_assessment.risk_level === 'HIGH' 
                ? 'bg-red-100 text-red-800'
                : analysis.risk_assessment.risk_level === 'MODERATE'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-green-100 text-green-800'
            }`}>
                Risk Level: {analysis.risk_assessment.risk_level}
            </span>
            </div>
            {analysis.risk_assessment.risk_factors.length > 0 && (
            <div className="mb-3">
                <p className="text-orange-800 font-medium mb-1">Risk Factors:</p>
                <ul className="list-disc list-inside text-orange-700">
                {analysis.risk_assessment.risk_factors.map((factor, index) => (
                    <li key={index}>{factor}</li>
                ))}
                </ul>
            </div>
            )}
        </div>
        )}

        {/* Early Warnings */}
        {analysis.early_warnings && analysis.early_warnings.length > 0 && (
        <div className="mb-6 p-4 bg-red-50 rounded-lg border-l-4 border-red-400">
            <h3 className="text-lg font-semibold text-red-900 mb-2">⚠️ Early Warning Signals</h3>
            <div className="space-y-3">
            {analysis.early_warnings.map((warning, index) => (
                <div key={index} className="p-3 bg-white rounded border-l-4 border-red-300">
                <div className="flex items-center mb-2">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    warning.severity === 'HIGH' 
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                    {warning.severity}
                    </span>
                    <span className="ml-2 text-sm font-medium text-gray-700">{warning.type}</span>
                </div>
                <p className="text-red-800 mb-1">{warning.message}</p>
                <p className="text-sm text-red-700 font-medium">Action: {warning.action}</p>
                </div>
            ))}
            </div>
        </div>
        )}

        {/* Statistics */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-blue-600">{analysis.total_tests || 0}</div>
            <div className="text-sm text-blue-800">Total Tests</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-green-600">{analysis.normal_count || 0}</div>
            <div className="text-sm text-green-800">Normal</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-yellow-600">{analysis.abnormal_count || 0}</div>
            <div className="text-sm text-yellow-800">Abnormal</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-red-600">{analysis.critical_count || 0}</div>
            <div className="text-sm text-red-800">Critical</div>
        </div>
        </div>

        {/* Results Table */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Lab Results</h3>
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
                {analysis.results.map((result, index: number) => (
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

        {/* Enhanced Recommendations */}
        {analysis.recommendations && analysis.recommendations.length > 0 && (
        <div className="mb-6 p-4 bg-green-50 rounded-lg">
            <h3 className="text-lg font-semibold text-green-900 mb-4">Recommendations</h3>
            <div className="grid gap-3">
            {analysis.recommendations.map((rec: string, index: number) => (
                <div key={index} className="flex items-start p-3 bg-white rounded-lg shadow-sm">
                <span className="text-green-600 mr-3 mt-1">•</span>
                <span className="text-gray-700">{rec}</span>
                </div>
            ))}
            </div>
        </div>
        )}
      </div>
    </div>
  )
}
