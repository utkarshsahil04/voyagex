// Page navigation enum
export enum Page {
  LANDING = 'LANDING',
  DASHBOARD = 'DASHBOARD',
  SCAN = 'SCAN',
  RESULT = 'RESULT',
}

// Allergen severity levels
export type AllergenSeverity = 'high' | 'medium' | 'low';

// Individual allergen information
export interface Allergen {
  name: string;
  severity: AllergenSeverity;
  description?: string;
}

// Dish report from analysis
export interface DishReport {
  dishName: string;
  restaurant?: string;
  allergens: Allergen[];
  safeAllergens: string[];
  ingredients: string[];
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  isDairyFree: boolean;
  isGlutenFree: boolean;
  isNutFree: boolean;
  isVegan: boolean;
  isVegetarian: boolean;
  recommendations?: string[];
  scanTime?: string;
}

// QR Code data
export interface QRCodeData {
  token: string;
  dishId: number;
  imageUrl?: string;
  scanUrl: string;
}

// Restaurant data
export interface Restaurant {
  id: number;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  apiKey: string;
}

// Dish data from backend
export interface Dish {
  id: number;
  name: string;
  description?: string;
  cuisine_type?: string;
  category?: string;
  price?: string;
  ingredients: string[];
  allergens: string[];
  is_vegetarian: boolean;
  is_vegan: boolean;
  is_gluten_free: boolean;
  is_dairy_free: boolean;
  is_available: boolean;
}