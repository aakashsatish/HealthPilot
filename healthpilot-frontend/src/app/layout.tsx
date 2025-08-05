import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { UserProvider } from '@/contexts/UserContext'
import Footer from '@/components/ui/Footer'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'HealthPilot - Lab Report Analysis',
  description: 'Upload your lab reports and get plain-English analysis with personalized recommendations.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans flex flex-col min-h-screen`}>
        <UserProvider>
          <div className="flex-1">
            {children}
          </div>
          <Footer />
        </UserProvider>
      </body>
    </html>
  )
}