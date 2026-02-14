from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Restaurant(Base):
    """Restaurant/Business model"""
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    business_type = Column(String(100))  # restaurant, cloud_kitchen, cafeteria, etc.
    api_key = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    dishes = relationship("Dish", back_populates="restaurant")
    qr_codes = relationship("QRCode", back_populates="restaurant")


class Dish(Base):
    """Dish/Menu Item model"""
    __tablename__ = "dishes"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    cuisine_type = Column(String(100))
    category = Column(String(100))  # appetizer, main, dessert, beverage
    price = Column(String(50))
    
    # Ingredients (stored as JSON array)
    ingredients = Column(JSON, nullable=False)
    
    # Allergen Information (derived from ingredients)
    allergens = Column(JSON)  # List of allergens
    
    # Nutritional Information (optional)
    nutrition_info = Column(JSON)
    
    # Dietary Flags
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_dairy_free = Column(Boolean, default=False)
    
    # Status
    is_available = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="dishes")
    qr_codes = relationship("QRCode", back_populates="dish")


class QRCode(Base):
    """QR Code model for dishes"""
    __tablename__ = "qr_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False)
    
    # QR Code Data
    qr_code_token = Column(String(255), unique=True, index=True, nullable=False)
    qr_code_image_path = Column(String(500))
    qr_code_url = Column(String(500))
    
    # Analytics
    scan_count = Column(Integer, default=0)
    last_scanned_at = Column(DateTime)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="qr_codes")
    dish = relationship("Dish", back_populates="qr_codes")
    scans = relationship("ScanLog", back_populates="qr_code")


class ScanLog(Base):
    """Log of QR code scans for analytics"""
    __tablename__ = "scan_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    qr_code_id = Column(Integer, ForeignKey("qr_codes.id"), nullable=False)
    
    # User Information (optional, anonymous by default)
    user_allergens = Column(JSON)  # User's allergen profile if provided
    
    # Scan Information
    scanned_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Relationships
    qr_code = relationship("QRCode", back_populates="scans")


class AllergenDatabase(Base):
    """Master allergen database"""
    __tablename__ = "allergen_database"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(255), unique=True, index=True, nullable=False)
    
    # Allergen Information
    allergens = Column(JSON)  # List of allergens present
    allergen_type = Column(String(100))  # primary, secondary, trace
    
    # Cross-contamination risks
    cross_contamination_risks = Column(JSON)
    
    # Alternative suggestions
    safe_substitutes = Column(JSON)
    
    # Source information
    data_source = Column(String(100))  # recipedb, flavordb, manual
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)