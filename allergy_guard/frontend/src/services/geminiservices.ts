import { DishReport, Allergen } from '../types';

// Simulated Gemini AI analysis
// In production, replace with actual Google Gemini API calls
export async function analyzeDish(dishName: string): Promise<DishReport> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Mock analysis data based on dish name
  const mockData: Record<string, DishReport> = {
    'pad thai': {
      dishName: 'Pad Thai',
      restaurant: 'Thai Street Kitchen',
      allergens: [
        { name: 'Peanuts', severity: 'high', description: 'Contains crushed peanuts as topping' },
        { name: 'Shellfish', severity: 'medium', description: 'Shrimp in sauce' },
        { name: 'Eggs', severity: 'low', description: 'Used in noodle preparation' },
      ],
      safeAllergens: ['Dairy', 'Gluten', 'Soy', 'Tree Nuts'],
      ingredients: [
        'Rice noodles',
        'Shrimp',
        'Eggs',
        'Peanuts',
        'Tamarind sauce',
        'Fish sauce',
        'Bean sprouts',
        'Green onions',
        'Lime',
      ],
      riskLevel: 'HIGH',
      isDairyFree: true,
      isGlutenFree: false,
      isNutFree: false,
      isVegan: false,
      isVegetarian: false,
      recommendations: [
        'Request no peanuts if allergic',
        'Ask for vegetarian version without shrimp',
        'Check if sauce contains gluten',
      ],
      scanTime: new Date().toISOString(),
    },
    'burger': {
      dishName: 'Classic Burger',
      restaurant: 'Burger House',
      allergens: [
        { name: 'Gluten', severity: 'high', description: 'Wheat bun' },
        { name: 'Dairy', severity: 'medium', description: 'Cheese and mayo' },
        { name: 'Eggs', severity: 'low', description: 'In bun and sauce' },
      ],
      safeAllergens: ['Nuts', 'Shellfish', 'Soy'],
      ingredients: [
        'Beef patty',
        'Wheat bun',
        'Cheddar cheese',
        'Lettuce',
        'Tomato',
        'Onion',
        'Pickles',
        'Mayo',
        'Ketchup',
      ],
      riskLevel: 'MEDIUM',
      isDairyFree: false,
      isGlutenFree: false,
      isNutFree: true,
      isVegan: false,
      isVegetarian: false,
      recommendations: [
        'Request lettuce wrap instead of bun for gluten-free',
        'Ask for no cheese if dairy-free',
        'Plant-based patty available',
      ],
      scanTime: new Date().toISOString(),
    },
  };

  const normalizedName = dishName.toLowerCase().trim();
  
  // Return mock data or default
  return mockData[normalizedName] || {
    dishName: dishName,
    restaurant: 'Unknown Restaurant',
    allergens: [
      { name: 'Gluten', severity: 'medium', description: 'May contain wheat' },
    ],
    safeAllergens: ['Nuts', 'Dairy', 'Shellfish'],
    ingredients: ['Unknown ingredients - please verify with staff'],
    riskLevel: 'MEDIUM',
    isDairyFree: false,
    isGlutenFree: false,
    isNutFree: true,
    isVegan: false,
    isVegetarian: false,
    recommendations: ['Please verify ingredients with restaurant staff'],
    scanTime: new Date().toISOString(),
  };
}

// Alternative: Real backend API integration
export async function analyzeDishFromBackend(token: string): Promise<DishReport> {
  const response = await fetch(`http://localhost:8000/scan/${token}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch dish information');
  }

  const data = await response.json();
  
  // Transform backend response to DishReport format
  const allergens: Allergen[] = data.safety_report.allergens.allergens_detected.map(
    (name: string) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      severity: 'high' as const,
      description: `Contains ${name}`,
    })
  );

  return {
    dishName: data.dish.name,
    restaurant: data.restaurant.name,
    allergens: allergens,
    safeAllergens: [],
    ingredients: data.ingredients,
    riskLevel: data.safety_report.risk_level,
    isDairyFree: data.dietary_flags.dairy_free,
    isGlutenFree: data.dietary_flags.gluten_free,
    isNutFree: allergens.every(a => !a.name.toLowerCase().includes('nut')),
    isVegan: data.dietary_flags.vegan,
    isVegetarian: data.dietary_flags.vegetarian,
    recommendations: data.safety_report.recommendations,
    scanTime: new Date().toISOString(),
  };
}