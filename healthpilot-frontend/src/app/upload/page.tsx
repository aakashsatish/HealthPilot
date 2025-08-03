'use client'

import { useState } from 'react'
import FileUpload from '@/components/upload/FileUpload'
import AnalysisResults from '@/components/results/AnalysisResults'
import { UploadResult, AnalysisResult } from '@/types/upload'
import AuthGuard from '@/components/auth/AuthGuard'
import Link from 'next/link'

export default function UploadPage() {
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleUploadSuccess = (result: UploadResult) => {
    setUploadResult(result)
    setIsProcessing(true)
  }

  const handleAnalysisComplete = (analysis: AnalysisResult) => {
    setIsProcessing(false)
    setUploadResult((prev) => {
      if (!prev) return null
      return {
        ...prev,
        analysis: analysis
      }
    })
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Upload Lab Report
              </h1>
              <p className="text-lg text-gray-600">
                Upload your blood test results to get personalized health insights
              </p>
            </div>
            <Link
              href="/dashboard"
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              Back to Dashboard
            </Link>
          </div>

          {!uploadResult ? (
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          ) : (
            <AnalysisResults 
              result={uploadResult} 
              isProcessing={isProcessing}
              onAnalysisComplete={handleAnalysisComplete}
            />
          )}
        </div>
      </div>
    </AuthGuard>
  )
}