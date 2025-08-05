export interface AnalysisResult {
  summary: string
  results: Array<{
    original_name: string
    value: number
    unit: string
    reference_range: string
    classification: string
    status?: string
    interpretation?: string
  }>
  recommendations: string[]
  risk_assessment?: {
    risk_level: string
    risk_factors: string[]
    recommendations: string[]
  }
  early_warnings?: Array<{
    type: string
    severity: string
    message: string
    action: string
  }>
  critical_findings?: Array<{
    test_name: string
    value: number
    unit: string
    classification: string
  }>
  abnormal_findings?: Array<{
    test_name: string
    value: number
    unit: string
    classification: string
  }>
  total_tests?: number
  normal_count?: number
  abnormal_count?: number
  critical_count?: number
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

// NEW TYPES FOR HISTORY FEATURES
export interface ReportHistory {
  id: string
  original_filename: string
  report_date: string
  lab_name: string
  status: string
  created_at: string
  summary: string
  risk_level: string
  abnormal_count: number
  critical_count: number
}

export interface ReportDetails {
  id: string
  original_filename: string
  report_date: string
  lab_name: string
  status: string
  created_at: string
  analysis_result: AnalysisResult
  summary: string
  risk_level: string
  abnormal_count: number
  critical_count: number
  email: string
  age: number
  sex: string
}

export interface TestTrend {
  test_value: number
  test_unit: string
  classification: string
  reference_range: string
  report_date: string
  created_at: string
}

export interface ReportComparison {
  report_1: {
    id: string
    date: string
    summary: string
    risk_level: string
    results: Array<{
      test_name: string
      value: number
      unit: string
      classification: string
    }>
  }
  report_2: {
    id: string
    date: string
    summary: string
    risk_level: string
    results: Array<{
      test_name: string
      value: number
      unit: string
      classification: string
    }>
  }
  changes: Array<{
    test_name: string
    value_1: number | null
    value_2: number | null
    change: number | null
    change_percent: number | null
    unit: string
    classification_1: string | null
    classification_2: string | null
    status: string
  }>
}