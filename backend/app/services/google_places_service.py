import os
import requests
from typing import List, Optional
from app.models.place import Place
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GooglePlacesService:
    """Service for fetching places from Google Places API"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    async def fetch_places_nearby(
        self, 
        lat: float, 
        lng: float, 
        query: str = "glamping",
        radius: int = 50000
    ) -> List[Place]:
        """
        Fetch places near coordinates using Google Places Text Search API
        
        Args:
            lat: Latitude coordinate
            lng: Longitude coordinate  
            query: Search query (default: "glamping")
            radius: Search radius in meters (default: 50000)
            
        Returns:
            List of Place objects
        """
        if not self.api_key:
            raise ValueError("Google Places API key not found in environment variables")
            
        places = []
        
        try:
            # Use Text Search API for better query matching
            url = f"{self.base_url}/textsearch/json"
            params = {
                "query": query,
                "location": f"{lat},{lng}",
                "radius": radius,
                "key": self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "OK":
                raise Exception(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
                
            for result in data.get("results", []):
                place = self._parse_google_place(result)
                if place:
                    places.append(place)
                    
        except requests.RequestException as e:
            print(f"Error fetching from Google Places API: {e}")
        except Exception as e:
            print(f"Error parsing Google Places data: {e}")
            # If it's a billing error, return empty list instead of crashing
            if "billing" in str(e).lower():
                print("Google Places API requires billing to be enabled. Skipping Google Places results.")
                return []
            
        return places
    
    def _parse_google_place(self, result: dict) -> Optional[Place]:
        """Parse Google Places API result into Place model"""
        try:
            # Extract coordinates
            location = result.get("geometry", {}).get("location", {})
            coordinates = (location.get("lat", 0), location.get("lng", 0))
            
            # Extract photos
            photos = []
            for photo in result.get("photos", []):
                photo_url = f"{self.base_url}/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={self.api_key}"
                photos.append(photo_url)
            
            # Extract infrastructure from types
            infrastructure = []
            types = result.get("types", [])
            if "lodging" in types:
                infrastructure.append("lodging")
            if "campground" in types:
                infrastructure.append("camping")
            if "restaurant" in types:
                infrastructure.append("restaurant")
            if "parking" in types:
                infrastructure.append("parking")
                
            return Place(
                name=result.get("name", ""),
                coordinates=coordinates,
                address=result.get("formatted_address", ""),
                category="unclassified",  # Will be classified later
                contact=result.get("formatted_phone_number"),
                website=result.get("website"),
                description=result.get("editorial_summary", {}).get("overview"),
                rating=result.get("rating"),
                photos=photos,
                infrastructure=infrastructure,
                verification_status="google_verified"
            )
            
        except Exception as e:
            print(f"Error parsing place: {e}")
            return None
