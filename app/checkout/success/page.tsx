'use client';

import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useCart } from '@/context/CartContext';

export default function CheckoutSuccessPage() {
  const router = useRouter();
  const { state } = useCart();

  useEffect(() => {
    // If someone tries to access this page directly without checking out
    if (state.items.length > 0) {
      router.push('/cart');
    }
  }, [state.items.length, router]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-16 text-center">
      <div className="mb-8">
        <svg
          className="mx-auto h-16 w-16 text-green-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 48 48"
        >
          <circle cx="24" cy="24" r="22" strokeWidth="2" />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M16 24l6 6 12-12"
          />
        </svg>
      </div>
      <h1 className="text-3xl font-bold mb-4">Order Confirmed!</h1>
      <p className="text-gray-600 mb-8">
        Thank you for your purchase. We'll send you an email with your order details shortly.
      </p>
      <Link
        href="/products"
        className="inline-block bg-blue-600 text-white px-8 py-3 rounded-md font-semibold hover:bg-blue-700 transition-colors"
      >
        Continue Shopping
      </Link>
    </div>
  );
}
