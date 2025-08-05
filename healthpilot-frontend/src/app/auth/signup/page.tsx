import Link from 'next/link'
import SignupForm from '@/components/auth/SignupForm'

export default function SignupPage() {
  return (
    <div className="min-h-screen gradient-bg relative overflow-hidden flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Organic background shapes */}
      <div className="organic-shape"></div>
      <div className="organic-shape"></div>
      

      
      <div className="max-w-md w-full space-y-8">
        <div className="hero-text text-center">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-700 to-gray-900 bg-clip-text text-transparent mb-6 leading-tight">
            HealthPilot
          </h1>
          <h2 className="text-3xl font-bold text-foreground mb-4">
            Join the journey
          </h2>
          <p className="text-lg text-muted-foreground">
            Start your personalized health intelligence experience
          </p>
          <p className="mt-4 text-sm text-muted-foreground">
            Or{' '}
            <Link href="/auth/login" className="font-semibold text-primary hover:text-accent transition-colors underline">
              sign in to your existing account
            </Link>
          </p>
        </div>
        
        <div className="feature-card gradient-card rounded-3xl p-10 transform -rotate-1">
          <SignupForm />
        </div>
      </div>
    </div>
  )
}