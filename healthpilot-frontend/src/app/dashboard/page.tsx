import Link from 'next/link'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">HealthPilot</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                href="/upload"
                className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Upload Report
              </Link>
              <button className="text-gray-500 hover:text-gray-700">
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
            <div className="text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Welcome to HealthPilot!
              </h3>
              <p className="text-gray-500 mb-6">
                Upload your lab reports to get started with personalized health insights.
              </p>
              <Link 
                href="/upload"
                className="bg-blue-600 text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Upload Your First Report
              </Link>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}