from fastapi import FastAPI, Depends, HTTPException, status, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field,ConfigDict
import logging
from datetime import datetime
from contextlib import asynccontextmanager
# from fastapi import FastAPI

from config import settings
from database.db import get_db, init_db
from database.models import Restaurant, Dish, QRCode
from core.dish_service import dish_service
from services.allergen_engine import allergen_engine
from services.recipedb_service import recipedb_service
from services.flavordb_service import flavordb_service
from utils.token_utils import generate_api_key, verify_api_key

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AllergyGuard API - Making Every Meal Safe & Transparent"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic models for request/response
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
    
    # class Config:
        # from_attributes=True
    model_config = ConfigDict(from_attributes=True)


class DishCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
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
    
    # class Config:
    model_config = ConfigDict(from_attributes=True)



# class QRCodeResponse(BaseModel):
#     id: int
#     qr_code_token: str
#     qr_code_url: str
#     image_url: Optional[str]
#     dish_id: int
#     restaurant_id: int
#     scan_count: int
#     is_active: bool
    
#     class Config:
#         from_attributes = True
class QRCodeResponse(BaseModel):
    id: int
    qr_code_token: str
    qr_code_url: str
    image_url: Optional[str]
    dish_id: int
    restaurant_id: int
    scan_count: int
    is_active: bool
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


class AllergenAnalysisRequest(BaseModel):
    ingredients: List[str] = Field(..., min_length=1)


# Dependency to verify API key
async def verify_restaurant_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> Restaurant:
    """Verify restaurant API key and return restaurant object"""
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


# Initialize database on startup
# @app.on_event("startup")
@asynccontextmanager
async def startup_event(app: FastAPI):
    """Initialize database and perform startup tasks"""
    print("Starting up")

    init_db()
    

    logger.info("✓ AllergyGuard API started successfully")
    print("Server running on http://localhost:8000")
    print("Server running on http://localhost:8000/docs")
    print("Server running on http://localhost:8000/redoc")
    yield
    
    print("Shutting down")
app = FastAPI(lifespan=startup_event)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "AllergyGuard API",
        "version": settings.app_version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected",
            "recipedb": "available",
            "flavordb": "available"
        }
    }


# ==================== Restaurant Management ====================

@app.post("/restaurants", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new restaurant
    
    Returns API key for authentication
    """
    # Check if email already exists
    existing = db.query(Restaurant).filter(Restaurant.email == restaurant.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant with this email already exists"
        )
    
    # Generate API key
    api_key = generate_api_key()
    
    # Create restaurant
    db_restaurant = Restaurant(
        name=restaurant.name,
        email=restaurant.email,
        phone=restaurant.phone,
        address=restaurant.address,
        business_type=restaurant.business_type,
        api_key=api_key
    )
    
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    logger.info(f"Created restaurant: {restaurant.name} (ID: {db_restaurant.id})")
    
    return db_restaurant


@app.get("/restaurants/me", response_model=RestaurantResponse)
async def get_current_restaurant(
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """Get current restaurant information"""
    return restaurant


@app.put("/restaurants/me")
async def update_restaurant(
    update_data: dict,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Update restaurant information"""
    for key, value in update_data.items():
        if hasattr(restaurant, key) and key not in ["id", "api_key", "created_at"]:
            setattr(restaurant, key, value)
    
    restaurant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(restaurant)
    
    return {"message": "Restaurant updated successfully", "restaurant": restaurant}


# ==================== Dish Management ====================

@app.post("/dishes", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish_data: DishCreate,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """
    Create a new dish with automatic allergen analysis
    
    Requires:
    - name: Dish name
    - ingredients: List of ingredients (minimum 1)
    
    Optional:
    - description, cuisine_type, category, price
    """
    try:
        dish = await dish_service.create_dish(
            db=db,
            restaurant_id=restaurant.id,
            dish_data=dish_data.dict()
        )
        return dish
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating dish: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create dish")


@app.get("/dishes", response_model=List[DishResponse])
async def get_dishes(
    skip: int = 0,
    limit: int = 100,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Get all dishes for the authenticated restaurant"""
    dishes = dish_service.get_dishes_by_restaurant(db, restaurant.id, skip, limit)
    return dishes


@app.get("/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(
    dish_id: int,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Get a specific dish"""
    dish = dish_service.get_dish(db, dish_id)
    
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    
    return dish


@app.put("/dishes/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish_id: int,
    dish_data: DishUpdate,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Update a dish (re-analyzes allergens if ingredients changed)"""
    # Verify ownership
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    
    try:
        # Filter out None values
        update_data = {k: v for k, v in dish_data.dict().items() if v is not None}
        updated_dish = await dish_service.update_dish(db, dish_id, update_data)
        return updated_dish
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/dishes/{dish_id}")
async def delete_dish(
    dish_id: int,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Delete a dish"""
    # Verify ownership
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    
    success = dish_service.delete_dish(db, dish_id)
    
    if success:
        return {"message": "Dish deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete dish")


# ==================== QR Code Management ====================

@app.post("/dishes/{dish_id}/qr-code", response_model=QRCodeResponse)
async def generate_qr_code(
    dish_id: int,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Generate QR code for a dish"""
    # Verify ownership
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    
    try:
        qr_code = dish_service.generate_qr_code_for_dish(db, dish_id)
        
        return QRCodeResponse(
            id=qr_code.id,
            qr_code_token=qr_code.qr_code_token,
            qr_code_url=qr_code.qr_code_url,
            image_url=f"{settings.qr_code_base_url}/static/qr_codes/{qr_code.qr_code_image_path.split('/')[-1]}",
            dish_id=qr_code.dish_id,
            restaurant_id=qr_code.restaurant_id,
            scan_count=qr_code.scan_count,
            is_active=qr_code.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/dishes/{dish_id}/qr-codes", response_model=List[QRCodeResponse])
async def get_dish_qr_codes(
    dish_id: int,
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Get all QR codes for a dish"""
    # Verify ownership
    dish = dish_service.get_dish(db, dish_id)
    if not dish or dish.restaurant_id != restaurant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    
    qr_codes = db.query(QRCode).filter(QRCode.dish_id == dish_id).all()
    
    return [
        QRCodeResponse(
            id=qr.id,
            qr_code_token=qr.qr_code_token,
            qr_code_url=qr.qr_code_url,
            image_url=f"{settings.qr_code_base_url}/static/qr_codes/{qr.qr_code_image_path.split('/')[-1]}" if qr.qr_code_image_path else None,
            dish_id=qr.dish_id,
            restaurant_id=qr.restaurant_id,
            scan_count=qr.scan_count,
            is_active=qr.is_active
        )
        for qr in qr_codes
    ]


# ==================== Public Scan Endpoint ====================

@app.get("/scan/{token}")
async def scan_qr_code(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    PUBLIC ENDPOINT: Scan QR code and get dish allergen information
    
    This is the endpoint that customers access when they scan a QR code
    No authentication required
    """
    try:
        # Get client info for logging
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")
        
        # Get dish information
        dish_info = await dish_service.get_dish_by_qr_token(
            db=db,
            token=token,
            log_scan=True,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return dish_info
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error scanning QR code: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve dish information")


# ==================== Allergen Analysis ====================

@app.post("/analyze/allergens")
async def analyze_allergens(
    request: AllergenAnalysisRequest,
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """
    Analyze ingredients for allergens (without creating a dish)
    
    Useful for testing ingredients before adding to menu
    """
    try:
        analysis = await allergen_engine.analyze_ingredients(request.ingredients)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing allergens: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to analyze allergens")


@app.post("/analyze/safety-report")
async def generate_safety_report(
    request: AllergenAnalysisRequest,
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """
    Generate comprehensive safety report for ingredients
    
    Includes allergens, dietary compatibility, and nutrition info
    """
    try:
        report = await allergen_engine.generate_safety_report(request.ingredients)
        return report
    except Exception as e:
        logger.error(f"Error generating safety report: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate safety report")


# ==================== Recipe DB Integration ====================

@app.get("/recipedb/recipe-of-day")
async def get_recipe_of_day(
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """Get recipe of the day from Foodoscope's RecipeDB"""
    try:
        return await recipedb_service.get_recipe_of_day()
    except Exception as e:
        logger.error(f"Error fetching recipe of day: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch recipe")


@app.get("/recipedb/search")
async def search_recipes(
    query: str,
    limit: int = 10,
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """Search recipes in RecipeDB"""
    try:
        return await recipedb_service.search_recipes(query, limit)
    except Exception as e:
        logger.error(f"Error searching recipes: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to search recipes")


@app.get("/recipedb/ingredient/{ingredient_name}")
async def get_ingredient_info(
    ingredient_name: str,
    restaurant: Restaurant = Depends(verify_restaurant_api_key)
):
    """Get ingredient information from RecipeDB"""
    try:
        return await recipedb_service.get_ingredient_info(ingredient_name)
    except Exception as e:
        logger.error(f"Error fetching ingredient info: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch ingredient info")


# ==================== Analytics ====================

@app.get("/analytics/scans")
async def get_scan_analytics(
    restaurant: Restaurant = Depends(verify_restaurant_api_key),
    db: Session = Depends(get_db)
):
    """Get QR code scan analytics for restaurant"""
    qr_codes = db.query(QRCode).filter(QRCode.restaurant_id == restaurant.id).all()
    
    total_scans = sum(qr.scan_count for qr in qr_codes)
    total_qr_codes = len(qr_codes)
    
    # Get top scanned dishes
    top_scans = sorted(qr_codes, key=lambda x: x.scan_count, reverse=True)[:10]
    
    return {
        "total_scans": total_scans,
        "total_qr_codes": total_qr_codes,
        "average_scans_per_qr": total_scans / total_qr_codes if total_qr_codes > 0 else 0,
        "top_scanned_dishes": [
            {
                "dish_id": qr.dish_id,
                "dish_name": qr.dish.name,
                "scan_count": qr.scan_count,
                "last_scanned": qr.last_scanned_at.isoformat() if qr.last_scanned_at else None
            }
            for qr in top_scans
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)