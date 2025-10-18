from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from app.core.config import settings

# Database setup
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PlaceDB(Base):
    """Database model for places"""
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(Text)
    category = Column(String, index=True)
    contact = Column(String)
    website = Column(String)
    description = Column(Text)
    rooms_count = Column(Integer)
    price_range = Column(String)
    photos = Column(Text)  # JSON string
    rating = Column(Float)
    infrastructure = Column(Text)  # JSON string
    verification_status = Column(String)
    source = Column(String)  # 'google' or '2gis'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
