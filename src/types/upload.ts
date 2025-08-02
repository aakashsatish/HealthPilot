export interface AnalysisResult {
  summary: string
  results: Array<{
    original_name: string
    value: number
    unit: string
    reference_range: string
    classification: string
  }>
  recommendations: string[]
}

export interface UploadResult {
  upload: {
    original_filename: string
    saved_filename: string
    file_path: string
    file_size: number
    uploaded_at: string
    success: boolean
  }
  report: {
    id: string
    profile_id: string
    file_path: string
    original_filename: string
    status: string
    created_at: string
    updated_at: string
  }
  job: {
    job_id: string
    status: string
  }
  message: string
  analysis?: AnalysisResult
} 