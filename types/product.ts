export interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
  description: string;
  features?: string[];
  specifications?: {
    [key: string]: string;
  };
}

export interface CartItem extends Product {
  quantity: number;
}
