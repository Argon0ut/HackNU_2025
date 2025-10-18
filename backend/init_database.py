#!/usr/bin/env python3
"""
Database initialization script for Travel Places Parser API
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.db.database import Base, engine
from app.core.config import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_connection():
    """Check if database connection is working"""
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        print("🔧 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def check_tables():
    """Check if tables exist"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"📋 Existing tables: {tables}")
            return "places" in tables
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 Initializing Travel Places Parser Database...")
    print("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    # Check if tables already exist
    if check_tables():
        print("✅ Database tables already exist!")
        response = input("Do you want to recreate them? (y/N): ")
        if response.lower() != 'y':
            print("✅ Database initialization complete!")
            return True
    
    # Create tables
    if create_tables():
        print("✅ Database initialization complete!")
        print("\n📋 Next steps:")
        print("1. Start the API server: uvicorn app.main:app --reload")
        print("2. Test the API endpoints")
        print("3. Check the database for stored places")
        return True
    else:
        print("❌ Database initialization failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
