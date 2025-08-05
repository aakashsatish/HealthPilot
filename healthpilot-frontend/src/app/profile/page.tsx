'use client'

import { useState, useEffect } from 'react'
import { useUser } from '@/contexts/UserContext'
import AuthGuard from '@/components/auth/AuthGuard'
import Link from 'next/link'

// Custom CSS for range slider
const rangeSliderStyles = `
  .slider::-webkit-slider-thumb {
    appearance: none;
    height: 24px;
    width: 24px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    border: 3px solid #ffffff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  }
  
  .slider::-moz-range-thumb {
    height: 24px;
    width: 24px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    border: 3px solid #ffffff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  }
  
  .slider::-webkit-slider-track {
    background: #d1d5db;
    height: 10px;
    border-radius: 5px;
  }
  
  .slider::-moz-range-track {
    background: #d1d5db;
    height: 10px;
    border-radius: 5px;
  }
  
  /* Dark mode support */
  .dark .slider::-webkit-slider-track {
    background: #4b5563;
  }
  
  .dark .slider::-moz-range-track {
    background: #4b5563;
  }
  
  /* Remove number input spinners */
  input[type="number"]::-webkit-outer-spin-button,
  input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  
  input[type="number"] {
    -moz-appearance: textfield;
  }
`

interface ProfileData {
  age?: number
  sex?: string
  weight?: number
  height?: number
  weight_unit?: string
  height_unit?: string
  medical_conditions?: string[]
  medications?: string[]
  lifestyle_factors?: string[]
}

// Helper function to convert decimal feet to feet and inches
const formatFeetInches = (decimalFeet: number): string => {
  const feet = Math.floor(decimalFeet)
  const inches = Math.round((decimalFeet - feet) * 12)
  return `${feet} ft ${inches} in`
}

// Helper function to convert feet and inches to decimal feet
const parseFeetInches = (feet: number, inches: number): number => {
  return feet + (inches / 12)
}

export default function ProfilePage() {
  const { user } = useUser()
  const [profile, setProfile] = useState<ProfileData>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) {
      fetchProfile()
    }
  }, [user])

  const fetchProfile = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/auth/profile/${user?.id}`)
      const data = await response.json()
      
      if (data.success && data.profile) {
        setProfile(data.profile)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setMessage('')

    try {
      const response = await fetch('http://localhost:8000/auth/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user?.id,
          email: user?.email,
          ...profile
        }),
      })

      const data = await response.json()
      
      if (data.success) {
        setMessage('Profile updated successfully!')
      } else {
        setMessage('Failed to update profile. Please try again.')
      }
    } catch (error) {
      console.error('Error updating profile:', error)
      setMessage('Error updating profile. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const handleInputChange = (field: keyof ProfileData, value: string | number | string[] | number[] | undefined) => {
    setProfile(prev => ({ ...prev, [field]: value }))
  }

  const handleArrayInputChange = (field: keyof ProfileData, value: string) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item)
    setProfile(prev => ({ ...prev, [field]: items }))
  }

  if (loading) {
    return (
      <AuthGuard>
        <div className="min-h-screen gradient-bg relative overflow-hidden">
          <div className="max-w-4xl mx-auto py-12 px-4">
            <div className="text-center">
              <div className="icon-container mx-auto mb-6 animate-pulse">
                <svg className="w-12 h-12 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <p className="text-xl text-gray-600 dark:text-gray-300 font-medium">Loading profile...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="min-h-screen gradient-bg relative overflow-hidden">
        {/* Organic background shapes */}
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        <div className="organic-shape"></div>
        

        <style jsx>{rangeSliderStyles}</style>
        <div className="max-w-5xl mx-auto py-12 px-4">
          {/* Header with personality */}
                      <div className="hero-text flex justify-between items-center mb-12">
              <div>
                <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
                  Profile Settings
                </h1>
                <p className="text-xl text-white leading-relaxed">
                  Update your personal information for better health insights
                </p>
              </div>
            <Link
              href="/dashboard"
              className="btn-secondary bg-gray-100 dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 px-6 py-3 rounded-xl font-semibold hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-105"
            >
              Back to Dashboard
            </Link>
          </div>

          {/* Profile Form with personality */}
          <div className="feature-card gradient-card rounded-3xl p-10">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Basic Information */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Basic Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-bold text-white mb-2">
                      Age
                    </label>
                    <input
                      type="number"
                      value={profile.age || ''}
                      onChange={(e) => handleInputChange('age', e.target.value ? parseInt(e.target.value) : undefined)}
                      className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-white bg-gray-700 placeholder-gray-300"
                      placeholder="Enter your age"
                    />
                  </div>
                  <div>
                                        <label className="block text-sm font-bold text-white mb-2">
                      Sex
                    </label>
                    <select
                      value={profile.sex || ''}
                      onChange={(e) => handleInputChange('sex', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-white bg-gray-700"
                    >
                        <option value="">Select sex</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Physical Measurements */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Physical Measurements</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-bold text-white mb-2">
                      Weight
                    </label>
                    <div className="space-y-3">
                      <div className="flex gap-2">
                        <div className="flex-1">
                          <input
                            type="range"
                            min={profile.weight_unit === 'lbs' ? "80" : "30"}
                            max={profile.weight_unit === 'lbs' ? "300" : "150"}
                            step={profile.weight_unit === 'lbs' ? "1" : "0.5"}
                            value={profile.weight || (profile.weight_unit === 'lbs' ? "150" : "70")}
                            onChange={(e) => handleInputChange('weight', parseFloat(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                          />
                        </div>
                        <select
                          value={profile.weight_unit || 'kg'}
                          onChange={(e) => {
                            handleInputChange('weight_unit', e.target.value)
                            // Reset weight when unit changes
                            handleInputChange('weight', e.target.value === 'lbs' ? 150 : 70)
                          }}
                          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white bg-white dark:bg-gray-800 font-medium"
                        >
                          <option value="kg">kg</option>
                          <option value="lbs">lbs</option>
                        </select>
                      </div>
                      <div className="flex justify-between text-sm text-black dark:text-white font-medium">
                        <span>
                          {profile.weight_unit === 'lbs' ? '80 lbs' : '30 kg'}
                        </span>
                        <span className="font-bold text-xl text-white">
                          {profile.weight || (profile.weight_unit === 'lbs' ? '150' : '70')} {profile.weight_unit || 'kg'}{((profile.weight || (profile.weight_unit === 'lbs' ? 150 : 70)) >= (profile.weight_unit === 'lbs' ? 300 : 150)) ? ' +' : ''}
                        </span>
                        <span>
                          {profile.weight_unit === 'lbs' ? '300 lbs +' : '150 kg +'}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-white mb-2">
                      Height
                    </label>
                    <div className="space-y-3">
                      <div className="flex gap-2">
                        <div className="flex-1">
                          <input
                            type="range"
                            min={profile.height_unit === 'ft' ? "4" : "120"}
                            max={profile.height_unit === 'ft' ? "7.5" : "220"}
                            step={profile.height_unit === 'ft' ? "0.1" : "1"}
                            value={profile.height || (profile.height_unit === 'ft' ? "5.5" : "170")}
                            onChange={(e) => handleInputChange('height', parseFloat(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                          />
                        </div>
                        <select
                          value={profile.height_unit || 'cm'}
                          onChange={(e) => {
                            handleInputChange('height_unit', e.target.value)
                            // Reset height when unit changes
                            handleInputChange('height', e.target.value === 'ft' ? 5.5 : 170)
                          }}
                          className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white bg-white dark:bg-gray-800 font-medium"
                        >
                          <option value="cm">cm</option>
                          <option value="ft">ft</option>
                        </select>
                      </div>
                      <div className="flex justify-between text-sm text-black dark:text-white font-medium">
                        <span>
                          {profile.height_unit === 'ft' ? '4 ft 0 in' : '120 cm'}
                        </span>
                        <span className="font-bold text-xl text-white">
                          {profile.height_unit === 'ft' && profile.height 
                            ? formatFeetInches(profile.height) + (profile.height >= 7.5 ? ' +' : '')
                            : `${profile.height || 170} ${profile.height_unit || 'cm'}${(profile.height || 170) >= 220 ? ' +' : ''}`
                          }
                        </span>
                        <span>
                          {profile.height_unit === 'ft' ? '7 ft 6 in +' : '220 cm +'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Medical Information */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Medical Information</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-bold text-white mb-2">
                      Medical Conditions
                    </label>
                    <input
                      type="text"
                      value={profile.medical_conditions?.join(', ') || ''}
                      onChange={(e) => handleArrayInputChange('medical_conditions', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white bg-white dark:bg-gray-700 placeholder-gray-700 dark:placeholder-gray-300"
                      placeholder="e.g., diabetes, hypertension (separate with commas)"
                    />
                    <p className="text-sm text-white mt-1 font-medium">Separate multiple conditions with commas</p>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-white mb-2">
                      Current Medications
                    </label>
                    <input
                      type="text"
                      value={profile.medications?.join(', ') || ''}
                      onChange={(e) => handleArrayInputChange('medications', e.target.value)}
                                                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white bg-white dark:bg-gray-700 placeholder-gray-700 dark:placeholder-gray-300"
                      placeholder="e.g., metformin, lisinopril (separate with commas)"
                    />
                    <p className="text-sm text-white mt-1 font-medium">Separate multiple medications with commas</p>
                  </div>
                </div>
              </div>

              {/* Lifestyle Factors */}
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Lifestyle Factors</h2>
                <div>
                                                        <label className="block text-sm font-bold text-white mb-2">
                    Lifestyle Factors
                  </label>
                  <input
                    type="text"
                    value={profile.lifestyle_factors?.join(', ') || ''}
                    onChange={(e) => handleArrayInputChange('lifestyle_factors', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black dark:text-white bg-white dark:bg-gray-700 placeholder-gray-700 dark:placeholder-gray-300"
                    placeholder="e.g., smoking, sedentary lifestyle, regular exercise (separate with commas)"
                  />
                  <p className="text-sm text-white mt-1 font-medium">Separate multiple factors with commas</p>
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={saving}
                  className="bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-6 py-3 rounded-xl hover:bg-gray-800 dark:hover:bg-gray-200 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? 'Saving...' : 'Save Profile'}
                </button>
              </div>

              {/* Message */}
              {message && (
                <div className={`p-4 rounded-md ${
                  message.includes('successfully') 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {message}
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
} 