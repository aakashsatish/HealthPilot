'use client'

import Link from 'next/link'

export default function AboutPage() {
  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden">
      {/* Organic background shapes */}
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">About HealthPilot</h1>
          <p className="text-xl text-gray-300">Your AI-powered health intelligence platform</p>
        </div>

        {/* Content */}
        <div className="feature-card gradient-card rounded-3xl p-10">
          <div className="prose prose-invert max-w-none">
            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Our Mission</h2>
                <p className="text-gray-300 leading-relaxed">
                  HealthPilot was created to democratize health intelligence by making lab report analysis accessible, 
                  understandable, and actionable for everyone. We believe that everyone deserves to understand their health data 
                  in plain English, with personalized insights that help them make informed decisions about their well-being.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">What We Do</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  HealthPilot uses advanced AI technology to analyze your lab reports and provide:
                </p>
                <ul className="list-disc list-inside text-gray-300 space-y-2 ml-4">
                  <li>Plain-English explanations of your results</li>
                  <li>Personalized health recommendations</li>
                  <li>Early warning signals for potential health issues</li>
                  <li>Trend tracking over time</li>
                  <li>Risk assessments based on your profile</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Technology Stack</h2>
                <p className="text-gray-300 leading-relaxed mb-4">
                  HealthPilot is built with modern, secure technologies:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Frontend</h3>
                    <ul className="list-disc list-inside text-gray-300 space-y-1 ml-4">
                      <li>Next.js 14 with App Router</li>
                      <li>TypeScript for type safety</li>
                      <li>Tailwind CSS for styling</li>
                      <li>Supabase for authentication</li>
                    </ul>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">Backend</h3>
                    <ul className="list-disc list-inside text-gray-300 space-y-1 ml-4">
                      <li>Python FastAPI</li>
                      <li>Ollama (Llama 3.1 8B) for AI</li>
                      <li>Tesseract OCR for text extraction</li>
                      <li>PostgreSQL database</li>
                    </ul>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Developer</h2>
                <div className="bg-gray-800/50 rounded-xl p-6">
                  <div className="flex items-center space-x-4 mb-4">
                    <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-bold text-xl">A</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-white">Aakash Satish</h3>
                      <p className="text-gray-300">Full-Stack Developer & Health Tech Enthusiast</p>
                    </div>
                  </div>
                  <p className="text-gray-300 leading-relaxed mb-4">
                    I&apos;m passionate about using technology to improve healthcare accessibility and understanding. 
                    HealthPilot represents my vision of making complex health data understandable and actionable for everyone.
                  </p>
                  <div className="flex space-x-4">
                    <a 
                      href="https://github.com/aakashsatish" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="flex items-center space-x-2 text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      <span>GitHub</span>
                    </a>
                  </div>
                </div>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Privacy & Security</h2>
                <p className="text-gray-300 leading-relaxed">
                  Your health data is precious, and we treat it with the utmost care. We implement industry-standard 
                  security measures and never share your personal information with third parties. Our AI analysis is 
                  performed locally when possible, ensuring your data remains private and secure.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-white mb-4">Medical Disclaimer</h2>
                <p className="text-gray-300 leading-relaxed">
                  HealthPilot provides informational analysis only and is not a substitute for professional medical advice. 
                  Always consult with qualified healthcare providers for medical decisions and treatment plans.
                </p>
              </section>

              <div className="text-sm text-gray-400 mt-8 pt-6 border-t border-gray-700">
                <p>Version 1.0.0 • August 2025</p>
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