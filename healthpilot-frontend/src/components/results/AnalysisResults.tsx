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
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-400 mx-auto mb-4"></div>
        <h2 className="text-2xl font-bold text-white mb-2">Analyzing your lab report...</h2>
        <p className="text-gray-300">This may take a few moments</p>
        <div className="mt-4 text-sm text-gray-400">
          Status: {jobStatus}
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="max-w-2xl mx-auto text-center">
        <h2 className="text-2xl font-bold text-white mb-4">Upload Complete</h2>
        <p className="text-gray-300">Your file has been uploaded successfully.</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="feature-card gradient-card rounded-3xl p-8 mb-6">
        <h2 className="text-2xl font-bold text-white mb-6">Analysis Results</h2>
        
        {/* Summary */}
        <div className="mb-6 p-6 bg-gray-800/50 rounded-xl border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-3">Summary</h3>
          <p className="text-gray-300 leading-relaxed">{analysis.summary}</p>
        </div>

        {/* Risk Assessment */}
        {analysis.risk_assessment && (
        <div className="mb-6 p-6 bg-gray-800/50 rounded-xl border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-3">Risk Assessment</h3>
            <div className="mb-4">
            <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${
                analysis.risk_assessment.risk_level === 'HIGH' 
                ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                : analysis.risk_assessment.risk_level === 'MODERATE'
                ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                : 'bg-green-500/20 text-green-400 border border-green-500/30'
            }`}>
                Risk Level: {analysis.risk_assessment.risk_level}
            </span>
            </div>
            {analysis.risk_assessment.risk_factors.length > 0 && (
            <div className="mb-3">
                <p className="text-gray-300 font-medium mb-2">Risk Factors:</p>
                <ul className="list-disc list-inside text-gray-400 space-y-1">
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
        <div className="mb-6 p-6 bg-gray-800/50 rounded-xl border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">⚠️ Early Warning Signals</h3>
            <div className="space-y-4">
            {analysis.early_warnings.map((warning, index) => (
                <div key={index} className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                <div className="flex items-center mb-3">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    warning.severity === 'HIGH' 
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                    }`}>
                    {warning.severity}
                    </span>
                    <span className="ml-3 text-sm font-medium text-gray-300">{warning.type}</span>
                </div>
                <p className="text-gray-300 mb-2 leading-relaxed">{warning.message}</p>
                <p className="text-sm text-gray-400 font-medium">Action: {warning.action}</p>
                </div>
            ))}
            </div>
        </div>
        )}

        {/* Statistics */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-800/50 p-4 rounded-xl text-center border border-gray-700">
            <div className="text-2xl font-bold text-blue-400">{analysis.total_tests || 0}</div>
            <div className="text-sm text-gray-300">Total Tests</div>
        </div>
        <div className="bg-gray-800/50 p-4 rounded-xl text-center border border-gray-700">
            <div className="text-2xl font-bold text-green-400">{analysis.normal_count || 0}</div>
            <div className="text-sm text-gray-300">Normal</div>
        </div>
        <div className="bg-gray-800/50 p-4 rounded-xl text-center border border-gray-700">
            <div className="text-2xl font-bold text-yellow-400">{analysis.abnormal_count || 0}</div>
            <div className="text-sm text-gray-300">Abnormal</div>
        </div>
        <div className="bg-gray-800/50 p-4 rounded-xl text-center border border-gray-700">
            <div className="text-2xl font-bold text-red-400">{analysis.critical_count || 0}</div>
            <div className="text-sm text-gray-300">Critical</div>
        </div>
        </div>

        {/* Results Table */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">Lab Results</h3>
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
                {analysis.results.map((result, index: number) => (
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

        {/* Enhanced Recommendations */}
        {analysis.recommendations && analysis.recommendations.length > 0 && (
        <div className="mb-6 p-6 bg-gray-800/50 rounded-xl border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">Recommendations</h3>
            <div className="grid gap-3">
            {analysis.recommendations.map((rec: string, index: number) => (
                <div key={index} className="flex items-start p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                <span className="text-green-400 mr-3 mt-1">•</span>
                <span className="text-gray-300">{rec}</span>
                </div>
            ))}
            </div>
        </div>
        )}
      </div>
    </div>
  )
}
