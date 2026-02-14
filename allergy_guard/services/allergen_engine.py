from typing import Dict, List, Set, Optional
from services.recipedb_service import recipedb_service
from services.flavordb_service import flavordb_service
import logging

logger = logging.getLogger(__name__)


class AllergenEngine:
    """
    Core allergen detection engine combining RecipeDB and FlavorDB
    Identifies allergens, suggests substitutes, and provides safety information
    """
    
    # Common allergen categories (based on FDA's major food allergens)
    MAJOR_ALLERGENS = {
        "milk": ["milk", "dairy", "cheese", "butter", "cream", "yogurt", "whey", "casein", "lactose"],
        "eggs": ["egg", "eggs", "egg white", "egg yolk", "albumin", "mayonnaise"],
        "fish": ["fish", "salmon", "tuna", "cod", "anchovy", "bass", "trout"],
        "shellfish": ["shrimp", "crab", "lobster", "prawns", "crayfish", "shellfish"],
        "tree_nuts": ["almond", "walnut", "cashew", "pistachio", "pecan", "hazelnut", "macadamia"],
        "peanuts": ["peanut", "peanuts", "groundnut", "peanut butter"],
        "wheat": ["wheat", "flour", "bread", "pasta", "semolina", "bulgur", "gluten"],
        "soy": ["soy", "soya", "tofu", "soy sauce", "edamame", "miso", "tempeh"],
        "sesame": ["sesame", "tahini", "sesame oil", "sesame seeds"],
        "mustard": ["mustard", "mustard seed", "mustard oil"],
        "celery": ["celery", "celeriac", "celery salt"],
        "lupin": ["lupin", "lupine flour"],
        "molluscs": ["clam", "mussel", "oyster", "squid", "octopus", "snail"],
        "sulfites": ["sulfur dioxide", "sulfite", "sulphite"]
    }
    
    def __init__(self):
        self.allergen_cache = {}
    
    def _normalize_ingredient(self, ingredient: str) -> str:
        """Normalize ingredient name for matching"""
        return ingredient.lower().strip()
    
    def _detect_allergen_in_ingredient(self, ingredient: str) -> Set[str]:
        """
        Detect allergens in a single ingredient using pattern matching
        
        Args:
            ingredient: Ingredient name
            
        Returns:
            Set of detected allergen categories
        """
        detected = set()
        normalized = self._normalize_ingredient(ingredient)
        
        for allergen_category, keywords in self.MAJOR_ALLERGENS.items():
            for keyword in keywords:
                if keyword.lower() in normalized:
                    detected.add(allergen_category)
                    break
        
        return detected
    
    async def analyze_ingredients(self, ingredients: List[str]) -> Dict:
        """
        Comprehensive allergen analysis of ingredients list
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Detailed allergen analysis including substitutes
        """
        # Standardize ingredients using RecipeDB
        standardized_ingredients = await recipedb_service.batch_standardize_ingredients(ingredients)
        
        # Detect allergens
        allergen_details = []
        all_allergens = set()
        
        for original, standardized in standardized_ingredients.items():
            # Basic allergen detection
            detected_allergens = self._detect_allergen_in_ingredient(standardized)
            
            if detected_allergens:
                all_allergens.update(detected_allergens)
                
                # Get safe substitutes from FlavorDB
                substitutes = []
                for allergen in detected_allergens:
                    subs = await flavordb_service.get_safe_substitutes(standardized, allergen)
                    substitutes.extend(subs)
                
                allergen_details.append({
                    "ingredient": original,
                    "standardized_name": standardized,
                    "allergens": list(detected_allergens),
                    "safe_substitutes": substitutes[:3]  # Top 3 substitutes
                })
        
        # Get cross-reactivity information
        cross_reactivity = {}
        for ingredient in standardized_ingredients.values():
            if ingredient in [item["standardized_name"] for item in allergen_details]:
                cross = await flavordb_service.predict_allergen_cross_reactivity(ingredient)
                if cross:
                    cross_reactivity[ingredient] = cross
        
        return {
            "allergens_detected": list(all_allergens),
            "allergen_count": len(all_allergens),
            "detailed_analysis": allergen_details,
            "cross_reactivity_warnings": cross_reactivity,
            "is_safe": len(all_allergens) == 0
        }
    
    async def check_diet_compatibility(self, ingredients: List[str]) -> Dict:
        """
        Check if ingredients are compatible with various dietary restrictions
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Dietary compatibility flags
        """
        allergen_analysis = await self.analyze_ingredients(ingredients)
        allergens = set(allergen_analysis["allergens_detected"])
        
        return {
            "vegetarian": "fish" not in allergens and "shellfish" not in allergens and "molluscs" not in allergens,
            "vegan": not any(a in allergens for a in ["milk", "eggs", "fish", "shellfish", "molluscs"]),
            "gluten_free": "wheat" not in allergens,
            "dairy_free": "milk" not in allergens,
            "nut_free": not any(a in allergens for a in ["tree_nuts", "peanuts"]),
            "shellfish_free": "shellfish" not in allergens and "molluscs" not in allergens,
            "soy_free": "soy" not in allergens,
            "egg_free": "eggs" not in allergens
        }
    
    async def get_nutrition_analysis(self, ingredients: List[str]) -> Dict:
        """
        Get nutritional analysis from RecipeDB
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Nutritional information
        """
        try:
            return await recipedb_service.get_nutrition_info(ingredients)
        except Exception as e:
            logger.error(f"Error getting nutrition info: {e}")
            return {
                "error": "Nutrition analysis unavailable",
                "message": str(e)
            }
    
    async def generate_safety_report(self, ingredients: List[str]) -> Dict:
        """
        Generate comprehensive safety report for a dish
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Complete safety report with allergens, diet info, and nutrition
        """
        # Parallel analysis
        allergen_analysis = await self.analyze_ingredients(ingredients)
        diet_compatibility = await self.check_diet_compatibility(ingredients)
        nutrition_info = await self.get_nutrition_analysis(ingredients)
        
        # Calculate risk level
        allergen_count = allergen_analysis["allergen_count"]
        if allergen_count == 0:
            risk_level = "LOW"
        elif allergen_count <= 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return {
            "risk_level": risk_level,
            "allergens": allergen_analysis,
            "dietary_compatibility": diet_compatibility,
            "nutrition": nutrition_info,
            "safety_score": max(0, 100 - (allergen_count * 15)),  # Simple scoring
            "recommendations": self._generate_recommendations(allergen_analysis)
        }
    
    def _generate_recommendations(self, allergen_analysis: Dict) -> List[str]:
        """Generate safety recommendations based on allergen analysis"""
        recommendations = []
        
        allergen_count = allergen_analysis["allergen_count"]
        
        if allergen_count == 0:
            recommendations.append("This dish appears safe for most people with common food allergies.")
        else:
            recommendations.append(f"This dish contains {allergen_count} major allergen(s). Please review carefully.")
            
        if allergen_analysis.get("cross_reactivity_warnings"):
            recommendations.append("Cross-reactivity warnings detected. People with related allergies should exercise caution.")
        
        if allergen_analysis["detailed_analysis"]:
            recommendations.append("Safe substitutes are available for allergenic ingredients.")
        
        return recommendations


# Singleton instance
allergen_engine = AllergenEngine()