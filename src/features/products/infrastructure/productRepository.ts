import axios from 'axios';
import { Product, ProductRepository, ProductFilters } from '../domain/types';

export class ApiProductRepository implements ProductRepository {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
  }

  async getProducts(filters?: ProductFilters): Promise<Product[]> {
    const response = await axios.get<Product[]>(`${this.baseUrl}/products`, {
      params: filters
    });
    return response.data;
  }

  async getProductById(id: number): Promise<Product> {
    const response = await axios.get<Product>(`${this.baseUrl}/products/${id}`);
    return response.data;
  }

  async getFeaturedProducts(limit: number): Promise<Product[]> {
    const products = await this.getProducts();
    return products.slice(0, limit);
  }

  async getCategories(): Promise<string[]> {
    const response = await axios.get<string[]>(`${this.baseUrl}/categories`);
    return response.data;
  }
}
