import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Keys
    google_places_api_key: Optional[str] = None
    two_gis_api_key: Optional[str] = None
    
    # Database settings
    database_url: str = "sqlite:///./travel_places.db"
    
    # Redis settings (for caching)
    redis_url: str = "redis://localhost:6379"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Search settings
    default_search_radius: int = 50000  # meters
    max_results_per_source: int = 20
    
    # Classification settings
    classification_threshold: float = 0.5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Load API keys from environment variables
settings.google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
settings.two_gis_api_key = os.getenv("TWO_GIS_API_KEY")
