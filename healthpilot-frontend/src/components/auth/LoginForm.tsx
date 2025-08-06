'use client'

import { useState } from 'react'
import { signIn } from '@/lib/auth'
import { useRouter } from 'next/navigation'

export default function LoginForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [email, setEmail] = useState('example@gmail.com')
  const [password, setPassword] = useState('••••••••')
  const [isEmailFocused, setIsEmailFocused] = useState(false)
  const [isPasswordFocused, setIsPasswordFocused] = useState(false)
  const router = useRouter()

  
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsLoading(true)
  setError('')

  try {
    const { data, error } = await signIn(email, password)
    
    if (error) {
      setError(error.message)
    } else {
      // Redirect to dashboard on successful login
      router.push('/dashboard')
    }
  } catch (err) {
    setError('An unexpected error occurred')
  } finally {
    setIsLoading(false)
  }
}

  const handleEmailFocus = () => {
    setIsEmailFocused(true)
    if (email === 'example@gmail.com') {
      setEmail('')
    }
  }

  const handleEmailBlur = () => {
    setIsEmailFocused(false)
    if (email === '') {
      setEmail('example@gmail.com')
    }
  }

  const handlePasswordFocus = () => {
    setIsPasswordFocused(true)
    if (password === '••••••••') {
      setPassword('')
    }
  }

  const handlePasswordBlur = () => {
    setIsPasswordFocused(false)
    if (password === '') {
      setPassword('••••••••')
    }
  }

  // Determine text color based on whether it's the example text
  const emailTextColor = email === 'example@gmail.com' ? 'text-muted-foreground' : 'text-foreground'
  const passwordTextColor = password === '••••••••' ? 'text-muted-foreground' : 'text-foreground'

  return (
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onFocus={handleEmailFocus}
            onBlur={handleEmailBlur}
            className={`w-full px-4 py-3 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring bg-input ${emailTextColor} placeholder-muted-foreground transition-colors`}
            placeholder="Enter your email"
            required
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onFocus={handlePasswordFocus}
            onBlur={handlePasswordBlur}
            className={`w-full px-4 py-3 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring bg-input ${passwordTextColor} placeholder-muted-foreground transition-colors`}
            placeholder="Enter your password"
            required
          />
        </div>

        {error && (
          <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-4 rounded-lg border border-red-200 dark:border-red-800">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center items-center space-x-2 py-3 px-4 border border-transparent rounded-lg text-sm font-medium bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ring disabled:opacity-50 transition-all duration-200"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 !text-black dark:!text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Signing in...</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5 !text-black dark:!text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              <span>Sign In</span>
            </>
          )}
        </button>
      </form>
    </div>
  )
}
