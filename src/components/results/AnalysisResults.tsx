'use client'

import { useState, useEffect } from 'react'
import { AnalysisResult } from '@/types/upload'

interface AnalysisResultsProps {
  result: any
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

        {/* Recommendations */}
        {analysis.recommendations && analysis.recommendations.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
            <ul className="space-y-2">
              {analysis.recommendations.map((rec: string, index: number) => (
                <li key={index} className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
} 