import math
from typing import Tuple, List


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        Distance in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r


def is_within_radius(
    center_lat: float, 
    center_lon: float, 
    point_lat: float, 
    point_lon: float, 
    radius_km: float
) -> bool:
    """
    Check if a point is within a given radius of a center point
    
    Args:
        center_lat, center_lon: Center coordinates
        point_lat, point_lon: Point coordinates to check
        radius_km: Radius in kilometers
        
    Returns:
        True if point is within radius
    """
    distance = calculate_distance(center_lat, center_lon, point_lat, point_lon)
    return distance <= radius_km


def filter_places_by_radius(
    places: List[dict], 
    center_lat: float, 
    center_lon: float, 
    radius_km: float
) -> List[dict]:
    """
    Filter places within a given radius
    
    Args:
        places: List of place dictionaries with 'coordinates' field
        center_lat, center_lon: Center coordinates
        radius_km: Radius in kilometers
        
    Returns:
        Filtered list of places
    """
    filtered_places = []
    
    for place in places:
        if 'coordinates' in place and len(place['coordinates']) == 2:
            lat, lon = place['coordinates']
            if is_within_radius(center_lat, center_lon, lat, lon, radius_km):
                filtered_places.append(place)
                
    return filtered_places


def get_bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    """
    Get bounding box coordinates for a given center point and radius
    
    Args:
        lat, lon: Center coordinates
        radius_km: Radius in kilometers
        
    Returns:
        Tuple of (min_lat, min_lon, max_lat, max_lon)
    """
    # Approximate conversion from km to degrees
    # 1 degree latitude ≈ 111 km
    # 1 degree longitude ≈ 111 km * cos(latitude)
    
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
    
    min_lat = lat - lat_delta
    max_lat = lat + lat_delta
    min_lon = lon - lon_delta
    max_lon = lon + lon_delta
    
    return min_lat, min_lon, max_lat, max_lon


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate that coordinates are within valid ranges
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        True if coordinates are valid
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180


def format_coordinates(lat: float, lon: float, precision: int = 6) -> str:
    """
    Format coordinates as a string
    
    Args:
        lat: Latitude
        lon: Longitude
        precision: Number of decimal places
        
    Returns:
        Formatted coordinate string
    """
    return f"{lat:.{precision}f},{lon:.{precision}f}"
