import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto text-center px-4">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Welcome to <span className="text-blue-600">HealthPilot</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Upload your lab reports and get plain-English analysis with personalized recommendations.
        </p>
        
        <div className="space-y-4">
          <div className="flex gap-4 justify-center">
            <Link 
              href="/auth/login"
              className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Sign In
            </Link>
            <Link 
              href="/auth/signup"
              className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition-colors"
            >
              Sign Up
            </Link>
          </div>
          
          <div className="text-sm text-gray-500">
            <p>Get started by creating an account</p>
          </div>
        </div>
      </div>
    </div>
  )
}