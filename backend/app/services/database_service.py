import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.database import get_db, PlaceDB
from app.models.place import Place


class DatabaseService:
    """Service for database operations with places"""
    
    def save_places(self, places: List[Place], source: str = "api") -> List[PlaceDB]:
        """
        Save places to database
        
        Args:
            places: List of Place objects to save
            source: Source of the data (e.g., 'api', 'google', '2gis')
            
        Returns:
            List of saved PlaceDB objects
        """
        saved_places = []
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            for place in places:
                # Check if place already exists (by name and coordinates)
                existing = db.query(PlaceDB).filter(
                    PlaceDB.name == place.name,
                    PlaceDB.latitude == place.coordinates[0],
                    PlaceDB.longitude == place.coordinates[1]
                ).first()
                
                if existing:
                    # Update existing place
                    existing.address = place.address
                    existing.category = place.category
                    existing.contact = place.contact
                    existing.website = place.website
                    existing.description = place.description
                    existing.rooms_count = place.rooms_count
                    existing.price_range = place.price_range
                    existing.rating = place.rating
                    existing.infrastructure = json.dumps(place.infrastructure)
                    existing.verification_status = place.verification_status
                    existing.source = source
                    saved_places.append(existing)
                else:
                    # Create new place
                    new_place = PlaceDB(
                        name=place.name,
                        latitude=place.coordinates[0],
                        longitude=place.coordinates[1],
                        address=place.address,
                        category=place.category,
                        contact=place.contact,
                        website=place.website,
                        description=place.description,
                        rooms_count=place.rooms_count,
                        price_range=place.price_range,
                        photos=json.dumps(place.photos),
                        rating=place.rating,
                        infrastructure=json.dumps(place.infrastructure),
                        verification_status=place.verification_status,
                        source=source
                    )
                    db.add(new_place)
                    saved_places.append(new_place)
            
            # Commit all changes
            db.commit()
            print(f"✅ Saved {len(saved_places)} places to database")
            
        except Exception as e:
            db.rollback()
            print(f"❌ Error saving places to database: {e}")
            raise e
        finally:
            db.close()
            
        return saved_places
    
    def get_places_by_category(self, category: str) -> List[PlaceDB]:
        """Get places by category"""
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            places = db.query(PlaceDB).filter(PlaceDB.category == category).all()
            return places
        finally:
            db.close()
    
    def get_places_by_source(self, source: str) -> List[PlaceDB]:
        """Get places by source"""
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            places = db.query(PlaceDB).filter(PlaceDB.source == source).all()
            return places
        finally:
            db.close()
    
    def get_all_places(self) -> List[PlaceDB]:
        """Get all places from database"""
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            places = db.query(PlaceDB).all()
            return places
        finally:
            db.close()
    
    def get_places_nearby(self, lat: float, lng: float, radius_km: float = 50) -> List[PlaceDB]:
        """Get places within radius of coordinates"""
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Simple bounding box query (for SQLite compatibility)
            # For production, use PostGIS for proper distance calculations
            lat_min = lat - (radius_km / 111.0)  # Approximate km to degrees
            lat_max = lat + (radius_km / 111.0)
            lng_min = lng - (radius_km / (111.0 * 0.7))  # Adjust for longitude
            lng_max = lng + (radius_km / (111.0 * 0.7))
            
            places = db.query(PlaceDB).filter(
                PlaceDB.latitude.between(lat_min, lat_max),
                PlaceDB.longitude.between(lng_min, lng_max)
            ).all()
            
            return places
        finally:
            db.close()
    
    def get_database_stats(self) -> dict:
        """Get database statistics"""
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            total_places = db.query(PlaceDB).count()
            
            # Count by source
            google_count = db.query(PlaceDB).filter(PlaceDB.source == "google").count()
            two_gis_count = db.query(PlaceDB).filter(PlaceDB.source == "2gis").count()
            
            # Count by category
            from sqlalchemy import func
            categories = db.query(PlaceDB.category, func.count(PlaceDB.id)).group_by(PlaceDB.category).all()
            category_stats = {cat: count for cat, count in categories}
            
            return {
                "total_places": total_places,
                "by_source": {
                    "google": google_count,
                    "2gis": two_gis_count
                },
                "by_category": category_stats
            }
        finally:
            db.close()
