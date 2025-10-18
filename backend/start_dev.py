#!/usr/bin/env python3
"""
Development startup script for Travel Places Parser API
"""

import os
import sys
import subprocess
from pathlib import Path


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("📝 Please create .env file:")
        print("   cp env.example .env")
        print("   # Then edit .env with your API keys")
        return False
    
    # Check if API keys are set
    with open(env_path) as f:
        content = f.read()
        
    if "your_google_places_api_key_here" in content:
        print("⚠️  Please update your Google Places API key in .env file")
        return False
        
    if "your_2gis_api_key_here" in content:
        print("⚠️  Please update your 2GIS API key in .env file")
        return False
    
    print("✅ .env file looks good!")
    return True


def start_server():
    """Start the FastAPI development server"""
    print("🚀 Starting Travel Places Parser API...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def main():
    """Main function"""
    print("🔧 Travel Places Parser API - Development Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the backend directory")
        print("   cd backend && python start_dev.py")
        return
    
    # Check environment setup
    if not check_env_file():
        return
    
    # Start the server
    start_server()


if __name__ == "__main__":
    main()

