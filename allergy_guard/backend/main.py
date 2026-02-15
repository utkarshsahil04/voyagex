import logging
import os
from datetime import datetime
from contextlib import asynccontextmanager
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict

# Local Imports
from config import settings
from database.db import get_db, init_db
from database.models import Restaurant, Dish, QRCode
from core.dish_service import dish_service
from services.allergen_engine import allergen_engine
from services.recipedb_service import recipedb_service
from services.flavordb_service import flavordb_service
from utils.token_utils import generate_api_key

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Lifespan (Startup/Shutdown) ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and perform startup tasks"""
    logger.info("🛡️ AllergyGuard API starting up...")
    
    # Initialize DB
    init_db()
    
    # Ensure static directory exists for QR codes
    os.makedirs("static/qr_codes", exist_ok=True)
    
    logger.info("✓ AllergyGuard API started successfully")
    print("Server running on http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    yield
    logger.info("🛡️ AllergyGuard API shutting down...")

# ==================== App Initialization ====================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AllergyGuard API - Making Every Meal Safe & Transparent",
    lifespan=lifespan
)

# CORS middleware - Essential for React (localhost:3000) to talk to FastAPI (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for QR code access
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== Pydantic Models ====================

class RestaurantCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    business_type: Optional[str] = "restaurant"

class RestaurantResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    business_type: str
    api_key: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DishCreate(BaseModel):
    name: str
    description: Optional[str] = "No description"
    cuisine_type: Optional[str] = "General"
    category: Optional[str] = "Main"
    price: Optional[str] = "0"
    ingredients: List[str] = Field(..., min_length=1)

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    ingredients: Optional[List[str]] = None
    is_available: Optional[bool] = None

class DishResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    cuisine_type: Optional[str]
    category: Optional[str]
    price: Optional[str]
    ingredients: List[str]
    allergens: Optional[List[str]]
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool
    is_dairy_free: bool
    is_available: bool
    model_config = ConfigDict(from_attributes=True)

class QRCodeResponse(BaseModel):
    id: int
    qr_code_token: str
    qr_code_url: str
    image_url: Optional[str]
    dish_id: int
    restaurant_id: int
    scan_count: int
    is_active: bool
    # Metadata for frontend
    name: str
    allergens: Optional[List[str]]
    model_config = ConfigDict(from_attributes=True)

class AllergenAnalysisRequest(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)

# ==================== Dependencies ====================

async def verify_restaurant_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> Restaurant:
    restaurant = db.query(Restaurant).filter(
        Restaurant.api_key == x_api_key,
        Restaurant.is_active == True
    ).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key"
        )
    return restaurant

# ==================== Routes ====================

@app.get("/")
async def root():
    return {"message": "AllergyGuard API", "version": settings.app_version, "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {"database": "connected", "recipedb": "available"}
    }

# --- Restaurant Management ---

@app.post("/restaurants", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    existing = db.query(Restaurant).filter(Restaurant.email == restaurant.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant with this email already exists")
    
    db_restaurant = Restaurant(**restaurant.dict(), api_key=generate_api_key())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.get("/restaurants/me", response_model=RestaurantResponse)
async def get_current_restaurant(restaurant: Restaurant = Depends(verify_restaurant_api_key)):
    return restaurant

# --- Dish Management ---

@app.post("/dishes", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(dish_data: DishCreate, restaurant: Restaurant = Depends(verify_restaurant_api_key), db: Session = Depends(get_db)):
    try:
        return await dish_service.create_dish(db, restaurant.id, dish_data.dict())
    except Exception as e:
        logger.error(f"Error creating dish: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dishes", response_model=List[DishResponse])
async def get_dishes(restaurant: Restaurant = Depends(verify_restaurant_api_key), db: Session = Depends(get_db)):
    return dish_service.get_dishes_by_restaurant(db, restaurant.id)

@app.get("/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(dish_id: int, restaurant: Restaurant = Depends(verify_restaurant_api_key), db: Session = Depends(get_db)):
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

# --- QR Code Management ---

@app.post("/dishes/{dish_id}/qr-code", response_model=QRCodeResponse)
async def generate_qr_code(dish_id: int, restaurant: Restaurant = Depends(verify_restaurant_api_key), db: Session = Depends(get_db)):
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    try:
        qr_code = dish_service.generate_qr_code_for_dish(db, dish_id)
        file_name = qr_code.qr_code_image_path.split('/')[-1] if qr_code.qr_code_image_path else "default.png"
        image_url = f"{settings.qr_code_base_url}/static/qr_codes/{file_name}"
        
        return {
            **qr_code.__dict__,
            "image_url": image_url,
            "name": dish.name,
            "allergens": dish.allergens
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Public Scan Endpoint ---

# @app.get("/scan/{token}")
@app.get("/scan/{token}")
async def scan_qr_code(token: str, db: Session = Depends(get_db)):
    try:
        # Try searching by QR Token first
        dish_info = await dish_service.get_dish_by_qr_token(db, token)
        
        # Transform the nested response to match frontend expectations (flat structure)
        return {
            "dish_name": dish_info.get("dish", {}).get("name"),
            "name": dish_info.get("dish", {}).get("name"),
            "allergens": dish_info.get("safety_report", {}).get("allergens", {}).get("allergens_detected", []),
            "ingredients": dish_info.get("ingredients", []),
            "dietary_flags": dish_info.get("dietary_flags", {}),
            "description": dish_info.get("dish", {}).get("description"),
            "restaurant_name": dish_info.get("restaurant", {}).get("name"),
            "scan_count": dish_info.get("scan_count", 0)
        }
    except ValueError as e:
        # If QR token not found, try searching directly by Dish ID as a fallback
        error_message = str(e)
        if "Invalid or inactive QR code" in error_message and token.isdigit():
            dish = dish_service.get_dish(db, int(token))
            if dish:
                return {
                    "dish_name": dish.name,
                    "name": dish.name,
                    "allergens": dish.allergens,
                    "ingredients": dish.ingredients,
                    "dietary_flags": {
                        "vegetarian": dish.is_vegetarian,
                        "vegan": dish.is_vegan,
                        "gluten_free": dish.is_gluten_free,
                        "dairy_free": dish.is_dairy_free
                    },
                    "description": dish.description,
                    "scan_count": 0
                }
        
        # If still not found, return 404
        raise HTTPException(status_code=404, detail="Token or Dish ID not found")
    except Exception as e:
        # Log other unexpected errors
        logger.error(f"Error scanning QR code: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# --- External Service Integration ---

@app.get("/recipedb/recipe-of-day")
async def get_recipe_of_day(restaurant: Restaurant = Depends(verify_restaurant_api_key)):
    return await recipedb_service.get_recipe_of_day()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)