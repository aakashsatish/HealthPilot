'use client'

import { useState } from 'react'
import FileUpload from '@/components/upload/FileUpload'
import AnalysisResults from '@/components/results/AnalysisResults'
import { UploadResult, AnalysisResult } from '@/types/upload'

export default function UploadPage() {
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleUploadSuccess = (result: UploadResult) => {
    setUploadResult(result)
    setIsProcessing(true)
  }

  const handleAnalysisComplete = (analysis: AnalysisResult) => {
    setIsProcessing(false)
    // Update the result with analysis data
    setUploadResult((prev) => {
      if (!prev) return null
      return {
        ...prev,
        analysis: analysis
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Upload Lab Report
          </h1>
          <p className="text-lg text-gray-600">
            Upload your blood test results to get personalized health insights
          </p>
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
  )
} 