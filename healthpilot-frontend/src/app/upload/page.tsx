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
      <div className="min-h-screen gradient-bg relative overflow-hidden">
        {/* Organic background shapes */}
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        
        <div className="max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          {/* Header with personality */}
          <div className="hero-text flex justify-between items-center mb-12">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
                Upload Lab Report
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
                Upload your blood test results to get personalized health insights
              </p>
            </div>
            <Link
              href="/dashboard"
              className="btn-secondary bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-6 py-3 rounded-xl font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
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