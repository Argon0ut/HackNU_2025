from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.place import Place
from app.services.google_places_service import GooglePlacesService
from app.services.two_gis_service import TwoGisService
from app.services.classification_service import ClassificationService

router = APIRouter(prefix="/api", tags=["parser"])

# Initialize services
google_places_service = GooglePlacesService()
two_gis_service = TwoGisService()
classification_service = ClassificationService()


@router.get("/parse_places", response_model=List[Place])
async def parse_places(
    lat: float = Query(..., description="Latitude coordinate"),
    lng: float = Query(..., description="Longitude coordinate"),
    query: str = Query("glamping", description="Search query"),
    include_google: bool = Query(True, description="Include Google Places results"),
    include_2gis: bool = Query(True, description="Include 2GIS results"),
    radius: int = Query(50000, description="Search radius in meters")
) -> List[Place]:
    """
    Parse travel-related places from Google Places and 2GIS APIs
    
    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        query: Search query (default: "glamping")
        include_google: Whether to include Google Places results
        include_2gis: Whether to include 2GIS results
        radius: Search radius in meters
        
    Returns:
        List of classified Place objects
    """
    all_places = []
    
    try:
        # Fetch from Google Places API
        if include_google:
            try:
                google_places = await google_places_service.fetch_places_nearby(
                    lat=lat, lng=lng, query=query, radius=radius
                )
                all_places.extend(google_places)
            except Exception as e:
                print(f"Error fetching from Google Places: {e}")
                # Continue with other sources even if Google fails
        
        # Fetch from 2GIS API
        if include_2gis:
            try:
                two_gis_places = await two_gis_service.parse_2gis(
                    query=query, lat=lat, lng=lng, radius=radius
                )
                all_places.extend(two_gis_places)
            except Exception as e:
                print(f"Error fetching from 2GIS: {e}")
                # Continue with other sources even if 2GIS fails
        
        # Classify all places
        classified_places = classification_service.classify_places_batch(all_places)
        
        # Remove duplicates based on name and coordinates
        unique_places = _remove_duplicates(classified_places)
        
        return unique_places
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing places: {str(e)}")


@router.get("/parse_places/google", response_model=List[Place])
async def parse_places_google_only(
    lat: float = Query(..., description="Latitude coordinate"),
    lng: float = Query(..., description="Longitude coordinate"),
    query: str = Query("glamping", description="Search query"),
    radius: int = Query(50000, description="Search radius in meters")
) -> List[Place]:
    """
    Parse places from Google Places API only
    """
    try:
        places = await google_places_service.fetch_places_nearby(
            lat=lat, lng=lng, query=query, radius=radius
        )
        classified_places = classification_service.classify_places_batch(places)
        return classified_places
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Google Places: {str(e)}")


@router.get("/parse_places/2gis", response_model=List[Place])
async def parse_places_2gis_only(
    lat: float = Query(..., description="Latitude coordinate"),
    lng: float = Query(..., description="Longitude coordinate"),
    query: str = Query("глэмпинг", description="Search query in Russian"),
    radius: int = Query(50000, description="Search radius in meters")
) -> List[Place]:
    """
    Parse places from 2GIS API only
    """
    try:
        places = await two_gis_service.parse_2gis(
            query=query, lat=lat, lng=lng, radius=radius
        )
        classified_places = classification_service.classify_places_batch(places)
        return classified_places
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing 2GIS: {str(e)}")


@router.get("/classify", response_model=dict)
async def get_classification_stats(
    lat: float = Query(..., description="Latitude coordinate"),
    lng: float = Query(..., description="Longitude coordinate"),
    query: str = Query("glamping", description="Search query")
) -> dict:
    """
    Get classification statistics for places in the area
    """
    try:
        # Get places from both sources
        all_places = []
        
        google_places = await google_places_service.fetch_places_nearby(
            lat=lat, lng=lng, query=query
        )
        all_places.extend(google_places)
        
        two_gis_places = await two_gis_service.parse_2gis(
            query=query, lat=lat, lng=lng
        )
        all_places.extend(two_gis_places)
        
        # Classify and get stats
        classified_places = classification_service.classify_places_batch(all_places)
        stats = classification_service.get_classification_stats(classified_places)
        
        return {
            "total_places": len(classified_places),
            "classification_stats": stats,
            "categories": list(classification_service.classification_rules.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting classification stats: {str(e)}")


def _remove_duplicates(places: List[Place]) -> List[Place]:
    """
    Remove duplicate places based on name and coordinates similarity
    
    Args:
        places: List of Place objects
        
    Returns:
        List of unique Place objects
    """
    unique_places = []
    seen = set()
    
    for place in places:
        if not place:
            continue
            
        # Create a key based on name and coordinates
        name_key = place.name.lower().strip() if place.name else ""
        coord_key = f"{place.coordinates[0]:.4f},{place.coordinates[1]:.4f}"
        place_key = f"{name_key}|{coord_key}"
        
        if place_key not in seen:
            seen.add(place_key)
            unique_places.append(place)
            
    return unique_places
