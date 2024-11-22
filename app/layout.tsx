import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import "./globals.css";
import { CartProvider } from '@/context/CartContext'
import { AuthProvider } from '@/context/AuthContext';
import Navigation from '@/components/Navigation'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'NextJS Shop',
  description: 'Modern online shop built with Next.js',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CartProvider>
          <AuthProvider>
            <Navigation />
            <main className="max-w-6xl mx-auto px-4 py-8">
              {children}
            </main>
            <footer className="bg-gray-100 mt-8">
              <div className="max-w-6xl mx-auto px-4 py-8">
                <p className="text-center text-gray-600"> 2023 NextShop. All rights reserved.</p>
              </div>
            </footer>
          </AuthProvider>
        </CartProvider>
      </body>
    </html>
  )
}
