#!/usr/bin/env python3
"""
Simple test script for the Travel Places Parser API
"""

import requests
import json
from typing import Dict, Any


def test_api_endpoint(base_url: str = "http://localhost:8000") -> None:
    """Test the API endpoints"""
    
    print("Testing Travel Places Parser API...")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test parse_places endpoint (Almaty coordinates)
    test_params = {
        "lat": 43.2389,
        "lng": 76.8897,
        "query": "glamping",
        "radius": 50000
    }
    
    try:
        response = requests.get(f"{base_url}/api/parse_places", params=test_params)
        print(f"✓ Parse places endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {len(data)} places")
            
            # Show first place if available
            if data:
                first_place = data[0]
                print(f"  First place: {first_place.get('name', 'Unknown')}")
                print(f"  Category: {first_place.get('category', 'Unknown')}")
                print(f"  Address: {first_place.get('address', 'Unknown')}")
        else:
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Parse places endpoint failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test classification stats endpoint
    try:
        response = requests.get(f"{base_url}/api/classify", params=test_params)
        print(f"✓ Classification stats endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total places: {data.get('total_places', 0)}")
            print(f"  Classification stats: {json.dumps(data.get('classification_stats', {}), indent=2)}")
        else:
            print(f"  Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Classification stats endpoint failed: {e}")


if __name__ == "__main__":
    print("Make sure the API server is running on http://localhost:8000")
    print("You can start it with: uvicorn app.main:app --reload")
    print()
    
    test_api_endpoint()
