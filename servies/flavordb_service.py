import httpx
from typing import Dict, List, Optional, Set
from config import settings
import logging

logger = logging.getLogger(__name__)


class FlavorDBService:
    """
    Service to interact with Foodoscope's FlavorDB
    Provides ingredient chemistry analysis, compound identification, and safe substitutions
    """
    
    def __init__(self):
        self.base_url = settings.recipe_api_base_url.replace("recipe2-api", "flavor-api")
        self.api_key = settings.recipe_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make HTTP request to FlavorDB API"""
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
                logger.error(f"HTTP error occurred: {e.response.status_code}")
                # Return empty result instead of failing
                return {}
            except Exception as e:
                logger.error(f"FlavorDB request error: {str(e)}")
                return {}
    
    async def get_ingredient_compounds(self, ingredient_name: str) -> List[Dict]:
        """
        Get chemical compounds present in an ingredient
        
        Args:
            ingredient_name: Name of the ingredient
            
        Returns:
            List of chemical compounds with their properties
        """
        endpoint = f"/ingredient/{ingredient_name}/compounds"
        result = await self._make_request(endpoint)
        return result.get("compounds", [])
    
    async def find_similar_ingredients(self, ingredient_name: str, limit: int = 5) -> List[str]:
        """
        Find ingredients with similar flavor profiles
        
        Args:
            ingredient_name: Source ingredient
            limit: Maximum number of similar ingredients
            
        Returns:
            List of similar ingredient names
        """
        endpoint = f"/ingredient/{ingredient_name}/similar?limit={limit}"
        result = await self._make_request(endpoint)
        return result.get("similar", [])
    
    async def get_safe_substitutes(self, ingredient_name: str, allergen: str) -> List[Dict]:
        """
        Get safe substitutes for an allergenic ingredient
        
        Args:
            ingredient_name: Name of the allergenic ingredient
            allergen: Specific allergen to avoid
            
        Returns:
            List of substitute ingredients with similarity scores
        """
        endpoint = f"/substitutes"
        data = {
            "ingredient": ingredient_name,
            "avoid_allergen": allergen
        }
        result = await self._make_request(endpoint, method="POST", data=data)
        return result.get("substitutes", [])
    
    async def analyze_ingredient_relationships(self, ingredients: List[str]) -> Dict:
        """
        Analyze flavor relationships between multiple ingredients
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Analysis of how ingredients complement each other
        """
        endpoint = "/analyze/relationships"
        data = {"ingredients": ingredients}
        result = await self._make_request(endpoint, method="POST", data=data)
        return result.get("analysis", {})
    
    async def get_compound_allergens(self, compound_name: str) -> List[str]:
        """
        Identify allergens associated with a chemical compound
        
        Args:
            compound_name: Name of the chemical compound
            
        Returns:
            List of associated allergens
        """
        endpoint = f"/compound/{compound_name}/allergens"
        result = await self._make_request(endpoint)
        return result.get("allergens", [])
    
    async def predict_allergen_cross_reactivity(self, ingredient: str) -> Dict:
        """
        Predict potential cross-reactive allergens
        
        Args:
            ingredient: Ingredient name
            
        Returns:
            Dictionary of potential cross-reactive allergens and confidence scores
        """
        endpoint = f"/ingredient/{ingredient}/cross-reactivity"
        result = await self._make_request(endpoint)
        return result.get("cross_reactivity", {})
    
    async def get_flavor_profile(self, ingredient_name: str) -> Dict:
        """
        Get complete flavor profile of an ingredient
        
        Args:
            ingredient_name: Name of the ingredient
            
        Returns:
            Flavor profile including taste categories and intensity
        """
        endpoint = f"/ingredient/{ingredient_name}/profile"
        result = await self._make_request(endpoint)
        return result.get("profile", {})
    
    async def batch_find_substitutes(self, ingredients_allergens: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Find substitutes for multiple ingredients at once
        
        Args:
            ingredients_allergens: List of dicts with 'ingredient' and 'allergen' keys
            
        Returns:
            Dictionary mapping ingredient names to their substitutes
        """
        substitutes_map = {}
        for item in ingredients_allergens:
            ingredient = item.get("ingredient")
            allergen = item.get("allergen")
            if ingredient and allergen:
                subs = await self.get_safe_substitutes(ingredient, allergen)
                substitutes_map[ingredient] = subs
        return substitutes_map


# Singleton instance
flavordb_service = FlavorDBService()