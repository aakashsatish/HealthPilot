'use client'

import Link from 'next/link'

export default function PrivacyPage() {
  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden">
      {/* Organic background shapes */}
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">Privacy Policy</h1>
          <p className="text-xl text-gray-300">How we protect and handle your data</p>
        </div>

        {/* Content */}
        <div className="feature-card gradient-card rounded-3xl p-10">
          <div className="prose prose-invert max-w-none">
            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Information We Collect</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  HealthPilot collects information you provide directly to us, including:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Account information (email, name)</li>
                  <li>Health profile data (age, sex, medical conditions, medications)</li>
                  <li>Lab report files you upload for analysis</li>
                  <li>Analysis results and recommendations</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">How We Use Your Information</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  We use your information to:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Provide AI-powered lab report analysis</li>
                  <li>Generate personalized health recommendations</li>
                  <li>Track your health trends over time</li>
                  <li>Improve our analysis algorithms</li>
                  <li>Send important service updates</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Data Security</h2>
                <p className="text-gray-300 leading-relaxed">
                  We implement industry-standard security measures to protect your health data:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4 mt-4">
                  <li>End-to-end encryption for data transmission</li>
                  <li>Secure cloud storage with access controls</li>
                  <li>Regular security audits and updates</li>
                  <li>HIPAA-compliant data handling practices</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Data Sharing</h2>
                <p className="text-gray-300 leading-relaxed">
                  We do not sell, trade, or rent your personal health information to third parties. 
                  Your data is only used to provide our analysis services and improve our platform.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Your Rights</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  You have the right to:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Access your personal data</li>
                  <li>Request correction of inaccurate information</li>
                  <li>Delete your account and associated data</li>
                  <li>Export your data in a portable format</li>
                  <li>Opt out of non-essential communications</li>
                </ul>
              </section>

              <div className="text-sm text-gray-400 mt-8 pt-6 border-t border-gray-700">
                <p>Last updated: August 2025</p>
              </div>
            </div>
          </div>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-8">
          <Link 
            href="/"
            className="btn-secondary inline-flex items-center space-x-2 bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-6 py-3 rounded-xl font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Back to Home</span>
          </Link>
        </div>
      </div>
    </div>
  )
} 