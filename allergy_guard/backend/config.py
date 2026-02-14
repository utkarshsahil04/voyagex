from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Configuration
    app_name: str = "AllergyGuard API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Foodoscope API
    recipe_api_base_url: str
    recipe_api_key: str
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS - Will be converted from comma-separated string to list
    allowed_origins: List[str]

    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    
    # QR Codes
    qr_code_storage_path: str = "./static/qr_codes"
    qr_code_base_url: str = "http://localhost:8000"
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator('allowed_origins', mode='before')
    @classmethod
    def split_origins(cls, v):
        """Convert comma-separated string to list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Initialize settings
settings = Settings()

# Create necessary directories
os.makedirs(settings.qr_code_storage_path, exist_ok=True)