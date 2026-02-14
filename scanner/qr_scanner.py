import qrcode
from io import BytesIO
import uuid
from pathlib import Path
from typing import Optional
from config import settings
import logging

logger = logging.getLogger(__name__)


class QRCodeService:
    """
    Service for generating and managing QR codes for dishes
    """
    
    def __init__(self):
        self.storage_path = Path(settings.qr_code_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.base_url = settings.qr_code_base_url
    
    def generate_unique_token(self) -> str:
        """Generate a unique token for QR code"""
        return str(uuid.uuid4())
    
    def generate_qr_code(
        self, 
        token: str, 
        dish_id: int,
        restaurant_id: int,
        save_to_disk: bool = True
    ) -> dict:
        """
        Generate QR code for a dish
        
        Args:
            token: Unique token for the QR code
            dish_id: ID of the dish
            restaurant_id: ID of the restaurant
            save_to_disk: Whether to save the image to disk
            
        Returns:
            Dictionary with QR code information
        """
        # Create URL that will be encoded in QR code
        scan_url = f"{self.base_url}/scan/{token}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(scan_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        qr_info = {
            "token": token,
            "scan_url": scan_url,
            "dish_id": dish_id,
            "restaurant_id": restaurant_id
        }
        
        if save_to_disk:
            # Save to file
            filename = f"{restaurant_id}_{dish_id}_{token}.png"
            filepath = self.storage_path / filename
            img.save(str(filepath))
            
            qr_info["image_path"] = str(filepath)
            qr_info["image_url"] = f"{self.base_url}/static/qr_codes/{filename}"
            logger.info(f"QR code saved to {filepath}")
        else:
            # Return as bytes
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_info["image_bytes"] = buffer.getvalue()
        
        return qr_info
    
    def generate_qr_code_batch(
        self, 
        dishes: list,
        restaurant_id: int
    ) -> list:
        """
        Generate QR codes for multiple dishes
        
        Args:
            dishes: List of dish IDs
            restaurant_id: ID of the restaurant
            
        Returns:
            List of QR code information dictionaries
        """
        qr_codes = []
        for dish_id in dishes:
            token = self.generate_unique_token()
            qr_info = self.generate_qr_code(token, dish_id, restaurant_id)
            qr_codes.append(qr_info)
        
        logger.info(f"Generated {len(qr_codes)} QR codes for restaurant {restaurant_id}")
        return qr_codes
    
    def delete_qr_code(self, image_path: str) -> bool:
        """
        Delete QR code image from disk
        
        Args:
            image_path: Path to the QR code image
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            filepath = Path(image_path)
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Deleted QR code: {image_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting QR code {image_path}: {e}")
            return False
    
    def validate_token(self, token: str) -> bool:
        """
        Validate QR code token format
        
        Args:
            token: Token to validate
            
        Returns:
            True if valid UUID format
        """
        try:
            uuid.UUID(token)
            return True
        except ValueError:
            return False
    
    def get_scan_url(self, token: str) -> str:
        """
        Get the scan URL for a token
        
        Args:
            token: QR code token
            
        Returns:
            Full scan URL
        """
        return f"{self.base_url}/scan/{token}"


# Singleton instance
qr_service = QRCodeService()