import { Product, ProductRepository, ProductFilters } from '../domain/types';
import { ApiProductRepository } from '../infrastructure/productRepository';

export class ProductService {
  private repository: ProductRepository;

  constructor(repository?: ProductRepository) {
    this.repository = repository || new ApiProductRepository();
  }

  async getFeaturedProducts(limit: number = 3): Promise<Product[]> {
    return this.repository.getFeaturedProducts(limit);
  }

  async getAllProducts(filters?: ProductFilters): Promise<Product[]> {
    return this.repository.getProducts(filters);
  }

  async getProduct(id: number): Promise<Product> {
    return this.repository.getProductById(id);
  }

  async getCategories(): Promise<string[]> {
    return this.repository.getCategories();
  }
}
