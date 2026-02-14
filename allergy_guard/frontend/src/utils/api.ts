const API_BASE = 'http://localhost:8000';

export const api = {
  async registerRestaurant(data: {
    name: string;
    email: string;
    phone?: string;
    address?: string;
    business_type?: string;
  }) {
    const res = await fetch(`${API_BASE}/restaurants`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Registration failed');
    return res.json();
  },

  async addDish(apiKey: string, dishData: {
    name: string;
    ingredients: string[];
    description?: string;
    cuisine_type?: string;
    category?: string;
    price?: string;
  }) {
    const res = await fetch(`${API_BASE}/dishes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify(dishData),
    });
    if (!res.ok) throw new Error('Failed to add dish');
    return res.json();
  },

  async getDishes(apiKey: string) {
    const res = await fetch(`${API_BASE}/dishes`, {
      headers: { 'X-API-Key': apiKey },
    });
    if (!res.ok) throw new Error('Failed to fetch dishes');
    return res.json();
  },

  async generateQR(apiKey: string, dishId: number) {
    const res = await fetch(`${API_BASE}/dishes/${dishId}/qr-code`, {
      method: 'POST',
      headers: { 'X-API-Key': apiKey },
    });
    if (!res.ok) throw new Error('Failed to generate QR code');
    return res.json();
  },

  async scanQR(token: string) {
    const res = await fetch(`${API_BASE}/scan/${token}`);
    if (!res.ok) throw new Error('Invalid QR code');
    return res.json();
  },

  async getAnalytics(apiKey: string) {
    const res = await fetch(`${API_BASE}/analytics/scans`, {
      headers: { 'X-API-Key': apiKey },
    });
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
  },
};