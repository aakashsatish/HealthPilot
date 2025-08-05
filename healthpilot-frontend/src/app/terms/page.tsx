'use client'

import Link from 'next/link'

export default function TermsPage() {
  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden">
      {/* Organic background shapes */}
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">Terms of Service</h1>
          <p className="text-xl text-gray-300">Our terms and conditions of use</p>
        </div>

        {/* Content */}
        <div className="feature-card gradient-card rounded-3xl p-10">
          <div className="prose prose-invert max-w-none">
            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Acceptance of Terms</h2>
                <p className="text-gray-300 leading-relaxed">
                  By accessing and using HealthPilot, you accept and agree to be bound by the terms and provision of this agreement. 
                  If you do not agree to abide by the above, please do not use this service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Service Description</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  HealthPilot provides AI-powered analysis of lab reports and health recommendations. Our services include:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Lab report analysis and interpretation</li>
                  <li>Personalized health recommendations</li>
                  <li>Health trend tracking and history</li>
                  <li>AI-powered insights and early warnings</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Medical Disclaimer</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  <strong className="text-white">Important:</strong> HealthPilot is not a substitute for professional medical advice, diagnosis, or treatment. 
                  Our analysis is for informational purposes only and should not be used to:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Make medical decisions without consulting healthcare providers</li>
                  <li>Self-diagnose or self-treat medical conditions</li>
                  <li>Replace professional medical consultation</li>
                  <li>Delay seeking medical attention when needed</li>
                </ul>
                <p className="text-gray-300 leading-relaxed mt-4">
                  Always consult with qualified healthcare professionals for medical advice and treatment.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">User Responsibilities</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  As a user of HealthPilot, you agree to:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Provide accurate and complete information</li>
                  <li>Maintain the security of your account credentials</li>
                  <li>Use the service only for lawful purposes</li>
                  <li>Not share your account with others</li>
                  <li>Report any security concerns immediately</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Intellectual Property</h2>
                <p className="text-gray-300 leading-relaxed">
                  HealthPilot and its original content, features, and functionality are owned by HealthPilot and are protected by 
                  international copyright, trademark, patent, trade secret, and other intellectual property laws.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Limitation of Liability</h2>
                <p className="text-gray-300 leading-relaxed">
                  HealthPilot shall not be liable for any indirect, incidental, special, consequential, or punitive damages, 
                  including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from 
                  your use of the service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Service Availability</h2>
                <p className="text-gray-300 leading-relaxed">
                  We strive to maintain high availability but cannot guarantee uninterrupted service. We may perform maintenance, 
                  updates, or modifications that could temporarily affect service availability.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Changes to Terms</h2>
                <p className="text-gray-300 leading-relaxed">
                  We reserve the right to modify these terms at any time. We will notify users of any material changes via email 
                  or through the service. Continued use of the service after changes constitutes acceptance of the new terms.
                </p>
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