import re
from typing import Dict, List
from app.models.place import Place


class ClassificationService:
    """Service for classifying travel-related places using rule-based approach"""
    
    def __init__(self):
        # Define classification rules
        self.classification_rules = {
            "Люкс глэмпинг": {
                "keywords": [
                    "глэмпинг", "glamping", "люкс", "luxury", "премиум", "premium",
                    "комфорт", "комфортный", "роскошный", "элитный"
                ],
                "infrastructure": ["luxury", "premium", "glamping"],
                "price_indicators": ["$$$", "$$$$", "дорого", "премиум"]
            },
            "Семейный гостевой дом": {
                "keywords": [
                    "семейный", "family", "гостевой дом", "guest house", "дом", "house",
                    "семья", "дети", "детский", "family-friendly"
                ],
                "infrastructure": ["family", "guest_house", "home"],
                "price_indicators": ["$", "$$", "недорого", "бюджетный"]
            },
            "Экотуризм": {
                "keywords": [
                    "эко", "eco", "экологический", "экологичный", "природа", "nature",
                    "зеленый", "green", "устойчивый", "sustainable", "био", "bio"
                ],
                "infrastructure": ["eco", "nature", "sustainable"],
                "price_indicators": ["$$", "$$$"]
            },
            "Этно-туризм": {
                "keywords": [
                    "этно", "этнический", "традиционный", "традиция", "культура",
                    "культурный", "национальный", "фольклор", "обычаи"
                ],
                "infrastructure": ["cultural", "traditional", "ethnic"],
                "price_indicators": ["$", "$$"]
            },
            "Горный домик": {
                "keywords": [
                    "горный", "mountain", "гора", "горы", "альпийский", "alpine",
                    "домик", "cabin", "хижина", "lodge", "шале", "chalet"
                ],
                "infrastructure": ["mountain", "cabin", "lodge"],
                "price_indicators": ["$$", "$$$"]
            }
        }
    
    def classify_place(self, place: Place) -> str:
        """
        Classify a place based on its attributes using rule-based approach
        
        Args:
            place: Place object to classify
            
        Returns:
            Classification category string
        """
        if not place:
            return "Неопределено"
            
        # Combine all text fields for analysis
        text_fields = [
            place.name or "",
            place.description or "",
            place.address or "",
            " ".join(place.infrastructure or [])
        ]
        combined_text = " ".join(text_fields).lower()
        
        # Score each category
        category_scores = {}
        
        for category, rules in self.classification_rules.items():
            score = 0
            
            # Check keywords
            for keyword in rules["keywords"]:
                if keyword.lower() in combined_text:
                    score += 2
                    
            # Check infrastructure
            for infra in rules["infrastructure"]:
                if infra in place.infrastructure:
                    score += 1
                    
            # Check price indicators
            if place.price_range:
                for price_indicator in rules["price_indicators"]:
                    if price_indicator.lower() in place.price_range.lower():
                        score += 1
                        
            category_scores[category] = score
        
        # Find the category with highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                return best_category
                
        return "Неопределено"
    
    def classify_places_batch(self, places: List[Place]) -> List[Place]:
        """
        Classify multiple places in batch
        
        Args:
            places: List of Place objects to classify
            
        Returns:
            List of classified Place objects
        """
        classified_places = []
        
        for place in places:
            if place:
                place.category = self.classify_place(place)
                classified_places.append(place)
                
        return classified_places
    
    def get_classification_stats(self, places: List[Place]) -> Dict[str, int]:
        """
        Get classification statistics for a list of places
        
        Args:
            places: List of classified Place objects
            
        Returns:
            Dictionary with category counts
        """
        stats = {}
        
        for place in places:
            if place and place.category:
                stats[place.category] = stats.get(place.category, 0) + 1
                
        return stats
