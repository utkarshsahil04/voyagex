# AllergyGuard

<p align="center">
  <img src="https://img.shields.io/badge/AllergyGuard-Making%20Every%20Meal%20Safe%20&%20Transparent-green?style=for-the-badge" alt="AllergyGuard">
  <img src="https://img.shields.io/badge/FastAPI-0.104.1-blue?style=flat-square" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18.2.0-blue?style=flat-square" alt="React">
  <img src="https://img.shields.io/badge/Python-3.9+-green?style=flat-square" alt="Python">
</p>

AllergyGuard is a comprehensive food safety platform that helps restaurants manage allergen information and provides customers with transparent ingredient details through QR code scanning. Making Every Meal Safe & Transparent.

---

## 🌟 Features

### For Restaurants
- **Restaurant Management**: Register and manage restaurant profiles with API key authentication
- **Dish Management**: Create and manage menu items with detailed ingredient lists
- **Automatic Allergen Detection**: Automatically identify 14 major allergens from ingredients
- **QR Code Generation**: Generate unique QR codes for each dish
- **Dietary Flags**: Automatic detection of vegetarian, vegan, gluten-free, and dairy-free options
- **Scan Analytics**: Track how many times each dish QR code has been scanned

### For Customers
- **Easy Scanning**: Scan dish QR codes to instantly view ingredient and allergen information
- **Allergen Alerts**: Clear display of detected allergens
- **Dietary Information**: View vegetarian, vegan, gluten-free, and dairy-free status
- **Transparent Information**: Full ingredient list for every dish

### Technical Features
- **RESTful API**: Well-documented FastAPI backend
- **Real-time Analysis**: Instant allergen detection from ingredient lists
- **External Integrations**: RecipeDB and FlavorDB for comprehensive ingredient data
- **QR Code System**: Unique, scannable codes for each dish
- **Analytics Dashboard**: Track scan counts and customer engagement

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: API Key-based authentication
- **QR Codes**: qrcode library with PIL
- **External APIs**: RecipeDB, FlavorDB integration

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **Build Tool**: React Scripts (Create React App)
- **Styling**: CSS with custom dark theme

### Development Tools
- **Server**: Uvicorn
- **Python**: 3.9+
- **Package Manager**: pip, npm

---

## 📁 Project Structure

```
allergy_guard/
├── backend/
│   ├── main.py                 # FastAPI application & routes
│   ├── config.py               # Application configuration
│   ├── requirements.txt        # Python dependencies
│   ├── core/
│   │   └── dish_service.py     # Business logic for dishes
│   ├── database/
│   │   ├── db.py               # Database initialization
│   │   └── models.py           # SQLAlchemy models
│   ├── scanner/
│   │   └── qr_scanner.py       # QR code scanning utilities
│   ├── services/
│   │   ├── allergen_engine.py  # Allergen detection engine
│   │   ├── flavordb_service.py # FlavorDB integration
│   │   └── recipedb_service.py # RecipeDB integration
│   ├── static/
│   │   └── qr_codes/           # Generated QR code images
│   └── utils/
│       └── token_utils.py      # API key generation
├── frontend/
│   ├── package.json            # Node.js dependencies
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── index.js           # React entry point
│   │   ├── components/
│   │   │   └── Navbar.js      # Navigation component
│   │   └── pages/
│   │       ├── Home.js        # Home page
│   │       ├── Menu.js        # Menu management
│   │       ├── Register.js    # Restaurant registration
│   │       ├── Scanner.js     # QR code scanner
│   │       └── Settings.js    # Settings page
│   └── build/                 # Production build
├── static/
│   └── qr_codes/              # Static QR code storage
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   
   
```
bash
   cd allergy_guard/backend
   
```

2. Create a virtual environment (recommended):
   
   
```
bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
```

3. Install Python dependencies:
   
   
```
bash
   pip install -r requirements.txt
   
```

4. Create a `.env` file in the backend directory:
   
   
```
   # API Configuration
   APP_NAME=AllergyGuard API
   APP_VERSION=1.0.0
   DEBUG=False
   
   # Foodoscope API
   RECIPE_API_BASE_URL=https://api.example.com
   RECIPE_API_KEY=your_api_key_here
   
   # Database
   DATABASE_URL=sqlite:///allergyguard.db
   
   # Security
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # CORS
   ALLOWED_ORIGINS=http://localhost:3000
   
   # Redis (optional)
   REDIS_URL=redis://localhost:6379/0
   CACHE_TTL=3600
   
   # QR Codes
   QR_CODE_STORAGE_PATH=./static/qr_codes
   QR_CODE_BASE_URL=http://localhost:8000
   
   # Logging
   LOG_LEVEL=INFO
   
```

5. Start the backend server:
   
   
```
bash
   python main.py
   
```

   The API will be available at:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Frontend Setup

1. Navigate to the frontend directory:
   
   
```
bash
   cd allergy_guard/frontend
   
```

2. Install dependencies:
   
   
```
bash
   npm install
   
```

3. Start the development server:
   
   
```
bash
   npm start
   
```

   The frontend will be available at: http://localhost:3000

4. For production build:
   
   
```
bash
   npm run build
   
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Most endpoints require an API key passed in the header:
```
X-API-Key: your_restaurant_api_key
```

### Endpoints

#### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

#### Restaurant Management
- `POST /restaurants` - Register a new restaurant
- `GET /restaurants/me` - Get current restaurant info

#### Dish Management
- `POST /dishes` - Create a new dish
- `GET /dishes` - List all dishes for the restaurant
- `GET /dishes/{dish_id}` - Get dish details
- `PUT /dishes/{dish_id}` - Update dish information

#### QR Code Management
- `POST /dishes/{dish_id}/qr-code` - Generate QR code for a dish

#### Public Endpoints
- `GET /scan/{token}` - Scan QR code (public, no auth required)

#### External Services
- `GET /recipedb/recipe-of-day` - Get recipe of the day

---

## 🧪 Testing the API

### Using curl

1. Register a restaurant:
```
bash
curl -X POST http://localhost:8000/restaurants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Restaurant",
    "email": "restaurant@example.com",
    "phone": "+1234567890",
    "address": "123 Main St"
  }'
```

2. Create a dish (with API key):
```
bash
curl -X POST http://localhost:8000/dishes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "name": "Margherita Pizza",
    "description": "Classic Italian pizza",
    "cuisine_type": "Italian",
    "category": "Main",
    "price": "12.99",
    "ingredients": ["tomato sauce", "mozzarella", "basil", "olive oil", "pizza dough"]
  }'
```

3. Generate QR code:
```
bash
curl -X POST http://localhost:8000/dishes/1/qr-code \
  -H "X-API-Key: your_api_key"
```

### Using Swagger UI

Open http://localhost:8000/docs in your browser for an interactive API documentation.

---

## 🍔 Major Allergens Detected

AllergyGuard automatically detects the following 14 major allergens:

1. **Celery**
2. **Cereals containing Gluten**
3. **Crustaceans**
4. **Eggs**
5. **Fish**
6. **Lupin**
7. **Milk**
8. **Molluscs**
9. **Mustard**
10. **Nuts**
11. **Peanuts**
12. **Sesame**
13. **Soya**
14. **Sulphur Dioxide**

---

## 📱 Application Screens

### Customer Flow
1. **Scan QR Code** → View dish details with allergens
2. **View Ingredients** → See full ingredient list
3. **Check Dietary Flags** → Vegetarian, Vegan, Gluten-Free, Dairy-Free

### Restaurant Flow
1. **Register** → Create restaurant account
2. **Add Dishes** → Input dish name, description, ingredients
3. **Auto-Detection** → System identifies allergens and dietary flags
4. **Generate QR** → Create QR code for each dish
5. **Print & Place** → Put QR codes on tables or menu

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | AllergyGuard API |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | False |
| `DATABASE_URL` | Database connection string | sqlite:///allergyguard.db |
| `SECRET_KEY` | JWT secret key | - |
| `ALLOWED_ORIGINS` | CORS allowed origins | http://localhost:3000 |
| `QR_CODE_BASE_URL` | Base URL for QR codes | http://localhost:8000 |
| `LOG_LEVEL` | Logging level | INFO |

---

## 📄 License

This project is proprietary and confidential. Unauthorized copying, distribution, or use of this project, via any medium, is strictly prohibited.

---

## 🙏 Acknowledgments

- RecipeDB for ingredient data
- FlavorDB for flavor profiles
- FastAPI team for the amazing framework
- React team for the frontend library

---

<p align="center">
  Made with ❤️ for safer food experiences
</p>
