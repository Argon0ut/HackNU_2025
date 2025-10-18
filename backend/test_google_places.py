#!/usr/bin/env python3
"""
Test script for Google Places API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_google_places_api():
    """Test Google Places API with current key"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    print(f"Testing Google Places API with key: {api_key[:10]}...")
    
    # Test with a simple request
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": "glamping",
        "location": "43.2389,76.8897",
        "radius": 50000,
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            if data.get('status') != 'OK':
                print(f"Error: {data.get('error_message')}")
            else:
                print(f"Found {len(data.get('results', []))} results")
        else:
            print(f"HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_google_places_api()
