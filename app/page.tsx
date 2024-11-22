'use client';

import { useState, useEffect } from "react";
import Link from "next/link";
import { ProductGrid } from "@/src/features/products/presentation/components/ProductGrid";
import { ProductService } from "@/src/features/products/application/productService";
import { Product } from "@/src/features/products/domain/types";

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const productService = new ProductService();

  useEffect(() => {
    async function loadProducts() {
      try {
        const products = await productService.getFeaturedProducts(3);
        setFeaturedProducts(products);
      } catch (error) {
        console.error('Failed to load products:', error);
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50 rounded-xl">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to NextShop
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Discover our amazing collection of products
        </p>
        <Link
          href="/products"
          className="inline-block bg-blue-600 text-white px-8 py-3 rounded-md font-semibold hover:bg-blue-700 transition-colors"
        >
          Shop Now
        </Link>
      </section>

      {/* Featured Products Section */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Products</h2>
        <ProductGrid products={featuredProducts} loading={loading} />
      </section>

      {/* Categories Section */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Shop by Category</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {['Electronics', 'Accessories'].map((category) => (
            <Link
              key={category}
              href={`/products?category=${category.toLowerCase()}`}
              className="group block bg-gray-100 rounded-lg p-6 text-center hover:bg-gray-200 transition-colors"
            >
              <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                {category}
              </h3>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
