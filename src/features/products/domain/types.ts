export interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
  description: string;
  image?: string;
  features?: string[];
  specifications?: {
    [key: string]: string;
  };
}

export interface ProductFilters {
  category?: string;
  min_price?: number;
  max_price?: number;
}

export interface ProductRepository {
  getProducts(filters?: ProductFilters): Promise<Product[]>;
  getProductById(id: number): Promise<Product>;
  getFeaturedProducts(limit: number): Promise<Product[]>;
  getCategories(): Promise<string[]>;
}
