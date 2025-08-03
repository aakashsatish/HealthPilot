'use client'

import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import Link from 'next/link'

export default function Dashboard() {
  const { user, signOut } = useUser()

  const handleLogout = async () => {
    await signOut()
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Welcome back, {user?.email}</p>
            </div>
            <div className="flex gap-4">
              <Link
                href="/upload"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Upload Report
              </Link>
              <button
                onClick={handleLogout}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <div className="text-gray-600">
              <p>No recent uploads yet.</p>
              <p className="mt-2">
                <Link href="/upload" className="text-blue-600 hover:text-blue-700">
                  Upload your first lab report
                </Link>{' '}
                to get started with personalized health insights.
              </p>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}