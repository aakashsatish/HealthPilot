import Link from 'next/link'
import LoginForm from '@/components/auth/LoginForm'

export default function LoginPage() {
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
            Welcome back
          </h2>
          <p className="text-lg text-muted-foreground">
            Sign in to continue your health journey
          </p>
          <p className="mt-4 text-sm text-muted-foreground">
            Or{' '}
            <Link href="/auth/signup" className="font-semibold text-primary hover:text-accent transition-colors underline">
              create a new account
            </Link>
          </p>
        </div>
        
        <div className="feature-card gradient-card rounded-3xl p-10 transform rotate-1">
          <LoginForm />
        </div>
      </div>
    </div>
  )
}
