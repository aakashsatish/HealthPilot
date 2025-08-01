'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function SignupForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [email, setEmail] = useState('example@gmail.com')
  const [password, setPassword] = useState('••••••••')
  const [confirmPassword, setConfirmPassword] = useState('••••••••')
  const [isEmailFocused, setIsEmailFocused] = useState(false)
  const [isPasswordFocused, setIsPasswordFocused] = useState(false)
  const [isConfirmPasswordFocused, setIsConfirmPasswordFocused] = useState(false)
  
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setIsLoading(false)
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      setIsLoading(false)
      return
    }

    try {
      // Call your backend API to create user
      const response = await fetch('http://localhost:8000/auth/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: email, // Using email as user_id for now
          email: email,
          age: null,
          sex: null
        }),
      })

      if (response.ok) {
        // Redirect to dashboard
        router.push('/dashboard')
      } else {
        const data = await response.json()
        setError(data.detail || 'Signup failed')
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

  const handleConfirmPasswordFocus = () => {
    setIsConfirmPasswordFocused(true)
    if (confirmPassword === '••••••••') {
      setConfirmPassword('')
    }
  }

  const handleConfirmPasswordBlur = () => {
    setIsConfirmPasswordFocused(false)
    if (confirmPassword === '') {
      setConfirmPassword('••••••••')
    }
  }

  // Determine text colors
  const emailTextColor = email === 'example@gmail.com' ? 'text-gray-400' : 'text-gray-900'
  const passwordTextColor = password === '••••••••' ? 'text-gray-400' : 'text-gray-900'
  const confirmPasswordTextColor = confirmPassword === '••••••••' ? 'text-gray-400' : 'text-gray-900'

  return (
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onFocus={handleEmailFocus}
            onBlur={handleEmailBlur}
            className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${emailTextColor} placeholder-gray-500`}
            placeholder="Enter your email"
            required
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onFocus={handlePasswordFocus}
            onBlur={handlePasswordBlur}
            className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${passwordTextColor} placeholder-gray-500`}
            placeholder="Enter your password"
            required
          />
        </div>

        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            onFocus={handleConfirmPasswordFocus}
            onBlur={handleConfirmPasswordBlur}
            className={`mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${confirmPasswordTextColor} placeholder-gray-500`}
            placeholder="Confirm your password"
            required
          />
        </div>

        {error && (
          <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isLoading ? 'Creating account...' : 'Create Account'}
        </button>
      </form>
    </div>
  )
}