import httpx
from typing import Dict, List, Optional, Any
from config import settings
import logging

logger = logging.getLogger(__name__)


class RecipeDBService:
    """
    Service to interact with Foodoscope's RecipeDB API
    Provides standardized ingredient names, allergen mapping, and nutrition data
    """
    
    def __init__(self):
        self.base_url = settings.recipe_api_base_url
        self.api_key = settings.recipe_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make HTTP request to RecipeDB API"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                if method == "GET":
                    response = await client.get(url, headers=self.headers, timeout=30.0)
                elif method == "POST":
                    response = await client.post(url, headers=self.headers, json=data, timeout=30.0)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error occurred: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise
    
    async def get_recipe_of_day(self) -> Dict:
        """Get recipe of the day"""
        return await self._make_request("/recipe/recipeofday")
    
    async def search_recipes(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for recipes
        
        Args:
            query: Search query string
            limit: Maximum number of results
        """
        endpoint = f"/recipe/search?query={query}&limit={limit}"
        return await self._make_request(endpoint)
    
    async def get_recipe_by_id(self, recipe_id: str) -> Dict:
        """
        Get detailed recipe information by ID
        
        Args:
            recipe_id: Recipe identifier
        """
        endpoint = f"/recipe/{recipe_id}"
        return await self._make_request(endpoint)
    
    async def get_ingredient_info(self, ingredient_name: str) -> Dict:
        """
        Get detailed information about an ingredient
        
        Args:
            ingredient_name: Name of the ingredient
        """
        endpoint = f"/ingredient/search?name={ingredient_name}"
        return await self._make_request(endpoint)
    
    async def standardize_ingredient(self, ingredient_name: str) -> str:
        """
        Standardize ingredient name across cuisines
        
        Args:
            ingredient_name: Raw ingredient name
            
        Returns:
            Standardized ingredient name
        """
        try:
            result = await self.get_ingredient_info(ingredient_name)
            return result.get("standard_name", ingredient_name)
        except Exception as e:
            logger.warning(f"Could not standardize ingredient '{ingredient_name}': {e}")
            return ingredient_name
    
    async def get_nutrition_info(self, ingredients: List[str]) -> Dict:
        """
        Get nutritional information for a list of ingredients
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Aggregated nutrition information
        """
        endpoint = "/nutrition/calculate"
        data = {"ingredients": ingredients}
        return await self._make_request(endpoint, method="POST", data=data)
    
    async def get_recipe_categories(self) -> List[str]:
        """Get available recipe categories"""
        endpoint = "/categories"
        result = await self._make_request(endpoint)
        return result.get("categories", [])
    
    async def get_cuisines(self) -> List[str]:
        """Get available cuisine types"""
        endpoint = "/cuisines"
        result = await self._make_request(endpoint)
        return result.get("cuisines", [])
    
    async def batch_standardize_ingredients(self, ingredients: List[str]) -> Dict[str, str]:
        """
        Standardize multiple ingredients at once
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Dictionary mapping original to standardized names
        """
        standardized = {}
        for ingredient in ingredients:
            standardized[ingredient] = await self.standardize_ingredient(ingredient)
        return standardized


# Singleton instance
recipedb_service = RecipeDBService()