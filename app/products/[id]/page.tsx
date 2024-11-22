'use client';

import { getProduct } from '@/services/api';
import ProductDetails from './ProductDetails';
import { notFound } from 'next/navigation';
import { Suspense } from 'react';
import ErrorBoundary from '@/components/ErrorBoundary';

interface PageProps {
  params: {
    id: string;
  };
}

async function getProductData(id: string) {
  const productId = parseInt(id);
  if (isNaN(productId)) {
    return null;
  }

  try {
    const product = await getProduct(productId);
    return product;
  } catch (error) {
    console.error('Error fetching product:', error);
    return null;
  }
}

export default async function ProductPage({ params }: PageProps) {
  const product = await getProductData(params.id);

  if (!product) {
    return notFound();
  }

  return (
    <ErrorBoundary fallback={<div>Something went wrong</div>}>
      <Suspense fallback={<div>Loading...</div>}>
        <ProductDetails product={product} />
      </Suspense>
    </ErrorBoundary>
  );
}
