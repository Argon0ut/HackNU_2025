import os
import requests
from typing import List, Optional
from app.models.place import Place
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TwoGisService:
    """Service for parsing data from 2GIS API"""
    
    def __init__(self):
        self.api_key = os.getenv("TWO_GIS_API_KEY")
        self.base_url = "https://catalog.api.2gis.com"
        
    async def parse_2gis(
        self, 
        query: str = "глэмпинг",
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: int = 50000
    ) -> List[Place]:
        """
        Parse places from 2GIS Catalog API
        
        Args:
            query: Search query in Russian (default: "глэмпинг")
            lat: Latitude coordinate (optional)
            lng: Longitude coordinate (optional)
            radius: Search radius in meters (default: 50000)
            
        Returns:
            List of Place objects
        """
        if not self.api_key:
            raise ValueError("2GIS API key not found in environment variables")
            
        places = []
        
        try:
            # Use 2GIS Catalog API
            url = f"{self.base_url}/3.0/items"
            params = {
                "q": query,
                "key": self.api_key,
                "fields": "items.point,items.name,items.address,items.rubrics,items.contact_groups,items.ads,items.region_id,items.reviews,items.rating,items.working_hours,items.description"
            }
            
            # Add location filter if coordinates provided
            if lat and lng:
                params["point"] = f"{lng},{lat}"
                params["radius"] = radius
                
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            
            if not data.get("result"):
                raise Exception("2GIS API returned no results")
                
            for item in data.get("result", {}).get("items", []):
                place = self._parse_2gis_item(item)
                if place:
                    places.append(place)
                    
        except requests.RequestException as e:
            print(f"Error fetching from 2GIS API: {e}")
        except Exception as e:
            print(f"Error parsing 2GIS data: {e}")
            
        return places
    
    async def _get_detailed_info(self, item_id: str) -> Optional[dict]:
        """Get detailed information for a specific place"""
        if not item_id:
            return None
            
        try:
            # Use 2GIS Profile API to get detailed information
            url = f"{self.base_url}/3.0/items/{item_id}"
            params = {
                "key": self.api_key,
                "fields": "item.point,item.name,item.address,item.rubrics,item.contact_groups,item.ads,item.rating,item.working_hours,item.description,item.reviews"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("result"):
                return data["result"]
                
        except Exception as e:
            print(f"Error getting detailed info for item {item_id}: {e}")
            
        return None
    
    def _parse_2gis_item(self, item: dict) -> Optional[Place]:
        """Parse 2GIS API item into Place model"""
        try:
            # Extract coordinates
            point = item.get("point", {})
            coordinates = (point.get("lat", 0), point.get("lon", 0))
            
            # Extract contact information
            contact_groups = item.get("contact_groups", [])
            phone = None
            website = None
            email = None
            
            for group in contact_groups:
                contacts = group.get("contacts", [])
                for contact in contacts:
                    contact_type = contact.get("type")
                    contact_value = contact.get("value")
                    if contact_type == "phone" and not phone:
                        phone = contact_value
                    elif contact_type == "website" and not website:
                        website = contact_value
                    elif contact_type == "email" and not email:
                        email = contact_value
                    elif contact_type == "mobile" and not phone:
                        phone = contact_value
                    elif contact_type == "url" and not website:
                        website = contact_value
            
            # Extract address
            address_parts = []
            address = item.get("address", {})
            
            # Try different address fields
            if address.get("comment"):
                address_parts.append(address["comment"])
            if address.get("street"):
                address_parts.append(address["street"])
            if address.get("house"):
                address_parts.append(address["house"])
            if address.get("building"):
                address_parts.append(address["building"])
            
            # If no structured address, try to get any address-like field
            if not address_parts:
                for key, value in address.items():
                    if value and isinstance(value, str) and len(value) > 3:
                        address_parts.append(value)
            
            full_address = ", ".join(address_parts) if address_parts else ""
            
            # Extract rating
            rating = None
            rating_data = item.get("rating", {})
            if rating_data:
                rating = rating_data.get("value")
            
            # Extract description
            description = item.get("description", "")
            if not description:
                ads = item.get("ads", {})
                description = ads.get("text", "")
            
            # Extract infrastructure from rubrics
            infrastructure = []
            rubrics = item.get("rubrics", [])
            for rubric in rubrics:
                rubric_name = rubric.get("name", "").lower()
                if "отель" in rubric_name or "гостиница" in rubric_name:
                    infrastructure.append("hotel")
                elif "кемпинг" in rubric_name or "лагерь" in rubric_name:
                    infrastructure.append("camping")
                elif "ресторан" in rubric_name or "кафе" in rubric_name:
                    infrastructure.append("restaurant")
                elif "парковка" in rubric_name:
                    infrastructure.append("parking")
                elif "спорт" in rubric_name:
                    infrastructure.append("sports")
                elif "бассейн" in rubric_name:
                    infrastructure.append("pool")
                elif "спа" in rubric_name:
                    infrastructure.append("spa")
                elif "фитнес" in rubric_name:
                    infrastructure.append("fitness")
            
            # Extract price range from description and name
            price_range = None
            name_lower = item.get("name", "").lower()
            desc_lower = description.lower()
            
            if any(word in name_lower + desc_lower for word in ["люкс", "премиум", "элит", "vip"]):
                price_range = "$$$$"
            elif any(word in name_lower + desc_lower for word in ["дорого", "высокий", "качественный"]):
                price_range = "$$$"
            elif any(word in name_lower + desc_lower for word in ["бюджет", "дешево", "эконом"]):
                price_range = "$"
            else:
                price_range = "$$"
                    
            # Combine contact information
            contact_info = []
            if phone:
                contact_info.append(f"Phone: {phone}")
            if email:
                contact_info.append(f"Email: {email}")
            combined_contact = "; ".join(contact_info) if contact_info else None
            
            return Place(
                name=item.get("name", ""),
                coordinates=coordinates,
                address=full_address,
                category="unclassified",  # Will be classified later
                contact=combined_contact,
                website=website,
                description=description,
                price_range=price_range,
                rating=rating,
                infrastructure=infrastructure,
                verification_status="2gis_verified"
            )
            
        except Exception as e:
            print(f"Error parsing 2GIS item: {e}")
            return None
