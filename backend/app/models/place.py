from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Place(BaseModel):
    """Pydantic model for travel-related places"""
    name: str = Field(..., description="Name of the place")
    coordinates: tuple[float, float] = Field(..., description="Latitude and longitude coordinates")
    address: str = Field(..., description="Full address of the place")
    category: str = Field(..., description="Classified category of the place")
    contact: Optional[str] = Field(None, description="Contact information")
    website: Optional[str] = Field(None, description="Website URL")
    description: Optional[str] = Field(None, description="Description of the place")
    rooms_count: Optional[int] = Field(None, description="Number of rooms available")
    price_range: Optional[str] = Field(None, description="Price range (e.g., '$$', '$$$')")
    photos: List[str] = Field(default_factory=list, description="List of photo URLs")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating from 0 to 5")
    infrastructure: List[str] = Field(default_factory=list, description="Available infrastructure")
    verification_status: str = Field(default="unverified", description="Verification status")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
