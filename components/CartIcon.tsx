'use client';

import { useCart } from '@/context/CartContext';
import Link from 'next/link';

export default function CartIcon() {
  const { state } = useCart();
  const itemCount = state.items.reduce((total, item) => total + item.quantity, 0);

  return (
    <Link href="/cart" className="relative text-gray-600 hover:text-gray-900">
      <span>Cart</span>
      {itemCount > 0 && (
        <span className="absolute -top-2 -right-2 bg-blue-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
          {itemCount}
        </span>
      )}
    </Link>
  );
}
