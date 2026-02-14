from sqlalchemy.orm import Session
from database.models import Dish, Restaurant, QRCode, ScanLog
from services.allergen_engine import allergen_engine
from scanner.qr_scanner import qr_service
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DishService:
    """Business logic for dish management"""
    
    async def create_dish(
        self, 
        db: Session, 
        restaurant_id: int,
        dish_data: Dict
    ) -> Dish:
        """
        Create a new dish with allergen analysis
        
        Args:
            db: Database session
            restaurant_id: Restaurant ID
            dish_data: Dish information including ingredients
            
        Returns:
            Created dish object
        """
        # Validate restaurant exists
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise ValueError(f"Restaurant with ID {restaurant_id} not found")
        
        # Get ingredients
        ingredients = dish_data.get("ingredients", [])
        if not ingredients:
            raise ValueError("Ingredients list is required")
        
        # Analyze allergens and dietary compatibility
        safety_report = await allergen_engine.generate_safety_report(ingredients)
        diet_compatibility = safety_report["dietary_compatibility"]
        
        # Create dish
        dish = Dish(
            restaurant_id=restaurant_id,
            name=dish_data.get("name"),
            description=dish_data.get("description"),
            cuisine_type=dish_data.get("cuisine_type"),
            category=dish_data.get("category"),
            price=dish_data.get("price"),
            ingredients=ingredients,
            allergens=safety_report["allergens"]["allergens_detected"],
            nutrition_info=safety_report["nutrition"],
            is_vegetarian=diet_compatibility["vegetarian"],
            is_vegan=diet_compatibility["vegan"],
            is_gluten_free=diet_compatibility["gluten_free"],
            is_dairy_free=diet_compatibility["dairy_free"],
        )
        
        db.add(dish)
        db.commit()
        db.refresh(dish)
        
        logger.info(f"Created dish: {dish.name} (ID: {dish.id})")
        return dish
    
    async def update_dish(
        self,
        db: Session,
        dish_id: int,
        update_data: Dict
    ) -> Dish:
        """
        Update dish information and re-analyze allergens if ingredients changed
        
        Args:
            db: Database session
            dish_id: Dish ID
            update_data: Updated dish information
            
        Returns:
            Updated dish object
        """
        dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not dish:
            raise ValueError(f"Dish with ID {dish_id} not found")
        
        # Check if ingredients changed
        ingredients_changed = "ingredients" in update_data and update_data["ingredients"] != dish.ingredients
        
        # Update basic fields
        for key, value in update_data.items():
            if hasattr(dish, key) and key not in ["id", "created_at", "restaurant_id"]:
                setattr(dish, key, value)
        
        # Re-analyze if ingredients changed
        if ingredients_changed:
            ingredients = update_data["ingredients"]
            safety_report = await allergen_engine.generate_safety_report(ingredients)
            diet_compatibility = safety_report["dietary_compatibility"]
            
            dish.allergens = safety_report["allergens"]["allergens_detected"]
            dish.nutrition_info = safety_report["nutrition"]
            dish.is_vegetarian = diet_compatibility["vegetarian"]
            dish.is_vegan = diet_compatibility["vegan"]
            dish.is_gluten_free = diet_compatibility["gluten_free"]
            dish.is_dairy_free = diet_compatibility["dairy_free"]
        
        dish.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(dish)
        
        logger.info(f"Updated dish: {dish.name} (ID: {dish.id})")
        return dish
    
    def get_dish(self, db: Session, dish_id: int) -> Optional[Dish]:
        """Get dish by ID"""
        return db.query(Dish).filter(Dish.id == dish_id).first()
    
    def get_dishes_by_restaurant(
        self, 
        db: Session, 
        restaurant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dish]:
        """Get all dishes for a restaurant"""
        return db.query(Dish).filter(
            Dish.restaurant_id == restaurant_id
        ).offset(skip).limit(limit).all()
    
    def delete_dish(self, db: Session, dish_id: int) -> bool:
        """Delete a dish"""
        dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if dish:
            # Delete associated QR codes
            qr_codes = db.query(QRCode).filter(QRCode.dish_id == dish_id).all()
            for qr_code in qr_codes:
                if qr_code.qr_code_image_path:
                    qr_service.delete_qr_code(qr_code.qr_code_image_path)
                db.delete(qr_code)
            
            db.delete(dish)
            db.commit()
            logger.info(f"Deleted dish ID: {dish_id}")
            return True
        return False
    
    def generate_qr_code_for_dish(
        self,
        db: Session,
        dish_id: int
    ) -> QRCode:
        """
        Generate QR code for a dish
        
        Args:
            db: Database session
            dish_id: Dish ID
            
        Returns:
            QRCode object
        """
        dish = self.get_dish(db, dish_id)
        if not dish:
            raise ValueError(f"Dish with ID {dish_id} not found")
        
        # Check if QR code already exists
        existing_qr = db.query(QRCode).filter(
            QRCode.dish_id == dish_id,
            QRCode.is_active == True
        ).first()
        
        if existing_qr:
            logger.info(f"QR code already exists for dish {dish_id}")
            return existing_qr
        
        # Generate new QR code
        token = qr_service.generate_unique_token()
        qr_info = qr_service.generate_qr_code(
            token=token,
            dish_id=dish_id,
            restaurant_id=dish.restaurant_id
        )
        
        # Save to database
        qr_code = QRCode(
            restaurant_id=dish.restaurant_id,
            dish_id=dish_id,
            qr_code_token=token,
            qr_code_image_path=qr_info.get("image_path"),
            qr_code_url=qr_info.get("scan_url"),
            is_active=True
        )
        
        db.add(qr_code)
        db.commit()
        db.refresh(qr_code)
        
        logger.info(f"Generated QR code for dish {dish_id}")
        return qr_code
    
    async def get_dish_by_qr_token(
        self,
        db: Session,
        token: str,
        log_scan: bool = True,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict:
        """
        Get dish information by QR code token
        
        Args:
            db: Database session
            token: QR code token
            log_scan: Whether to log the scan
            ip_address: IP address of scanner
            user_agent: User agent of scanner
            
        Returns:
            Comprehensive dish safety information
        """
        # Find QR code
        qr_code = db.query(QRCode).filter(
            QRCode.qr_code_token == token,
            QRCode.is_active == True
        ).first()
        
        if not qr_code:
            raise ValueError("Invalid or inactive QR code")
        
        # Get dish
        dish = self.get_dish(db, qr_code.dish_id)
        if not dish:
            raise ValueError("Dish not found")
        
        # Log scan
        if log_scan:
            qr_code.scan_count += 1
            qr_code.last_scanned_at = datetime.utcnow()
            
            scan_log = ScanLog(
                qr_code_id=qr_code.id,
                scanned_at=datetime.utcnow(),
                ip_address=ip_address,
                user_agent=user_agent
            )
            db.add(scan_log)
            db.commit()
        
        # Generate fresh safety report
        safety_report = await allergen_engine.generate_safety_report(dish.ingredients)
        
        return {
            "dish": {
                "id": dish.id,
                "name": dish.name,
                "description": dish.description,
                "cuisine_type": dish.cuisine_type,
                "category": dish.category,
                "price": dish.price
            },
            "restaurant": {
                "id": dish.restaurant.id,
                "name": dish.restaurant.name
            },
            "ingredients": dish.ingredients,
            "safety_report": safety_report,
            "dietary_flags": {
                "vegetarian": dish.is_vegetarian,
                "vegan": dish.is_vegan,
                "gluten_free": dish.is_gluten_free,
                "dairy_free": dish.is_dairy_free
            },
            "scan_count": qr_code.scan_count
        }


# Singleton instance
dish_service = DishService()