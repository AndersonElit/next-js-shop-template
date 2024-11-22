const API_BASE_URL = 'http://localhost:8000/api';

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

export interface CartItem {
  product_id: number;
  quantity: number;
}

export interface Order {
  id: number;
  user_id: number;
  items: CartItem[];
  total: number;
  status: string;
  created_at: string;
}

export interface OrderItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
}

export interface OrderDetails {
  firstName: string;
  lastName: string;
  email: string;
  address: string;
  city: string;
  country: string;
  zipCode: string;
}

export interface OrderData {
  items: OrderItem[];
  details: OrderDetails;
}

export async function getProducts(params?: {
  category?: string;
  min_price?: number;
  max_price?: number;
}): Promise<Product[]> {
  const queryParams = new URLSearchParams();
  if (params?.category) queryParams.append('category', params.category);
  if (params?.min_price) queryParams.append('min_price', params.min_price.toString());
  if (params?.max_price) queryParams.append('max_price', params.max_price.toString());

  const response = await fetch(`${API_BASE_URL}/products?${queryParams}`);
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  return response.json();
}

export async function getProduct(id: number): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/products/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch product');
  }
  return response.json();
}

export async function getCategories(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/categories`);
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
}

export async function createOrder(orderData: OrderData): Promise<Order> {
  const response = await fetch(`${API_BASE_URL}/orders/new`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(orderData),
  });

  if (!response.ok) {
    throw new Error('Failed to create order');
  }

  return response.json();
}
