# Travel Places Parser API

A FastAPI backend that parses data from Google Places and 2GIS APIs for travel-related locations, classifies them by category, and returns structured results.

## Features

- Parse places from Google Places API
- Parse places from 2GIS API  
- Rule-based classification of travel places
- Duplicate removal and data normalization
- RESTful API with comprehensive endpoints

## Categories

The API classifies places into the following categories:
- **Люкс глэмпинг** - Luxury glamping
- **Семейный гостевой дом** - Family guest house
- **Экотуризм** - Eco-tourism
- **Этно-туризм** - Ethnic tourism
- **Горный домик** - Mountain cabin
- **Неопределено** - Undefined

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database (optional - can use SQLite for development):
```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Create database
createdb travel_places

# Or using psql
psql -c "CREATE DATABASE travel_places;"
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API keys and database credentials
```

5. Edit `.env` file with your actual values:
```bash
# For PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/travel_places

# For SQLite (simpler for development)
# DATABASE_URL=sqlite:///./travel_places.db

# API Keys
GOOGLE_PLACES_API_KEY=your_actual_google_places_api_key
TWO_GIS_API_KEY=your_actual_2gis_api_key
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Main Endpoint
- `GET /api/parse_places` - Parse places from both Google Places and 2GIS

### Individual Sources
- `GET /api/parse_places/google` - Parse places from Google Places only
- `GET /api/parse_places/2gis` - Parse places from 2GIS only

### Classification
- `GET /api/classify` - Get classification statistics

### Parameters
- `lat` (required): Latitude coordinate
- `lng` (required): Longitude coordinate  
- `query` (optional): Search query (default: "glamping")
- `include_google` (optional): Include Google Places results (default: true)
- `include_2gis` (optional): Include 2GIS results (default: true)
- `radius` (optional): Search radius in meters (default: 50000)

## Example Usage

```bash
# Parse glamping places near Almaty
curl "http://localhost:8000/api/parse_places?lat=43.2389&lng=76.8897&query=glamping"

# Parse only from Google Places
curl "http://localhost:8000/api/parse_places/google?lat=43.2389&lng=76.8897&query=glamping"

# Get classification statistics
curl "http://localhost:8000/api/classify?lat=43.2389&lng=76.8897&query=glamping"
```

## Environment Variables

- `GOOGLE_PLACES_API_KEY`: Your Google Places API key
- `TWO_GIS_API_KEY`: Your 2GIS API key
- `DATABASE_URL`: Database connection string (optional)
- `REDIS_URL`: Redis connection string (optional)

## Quick Start (Local Development)

For quick local development with SQLite:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment file
cp env.example .env

# 3. Edit .env and add your API keys
# GOOGLE_PLACES_API_KEY=your_key_here
# TWO_GIS_API_KEY=your_key_here

# 4. Run the application
uvicorn app.main:app --reload
```

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/routes/parser.py    # API routes
│   ├── services/               # Service classes
│   │   ├── google_places_service.py
│   │   ├── two_gis_service.py
│   │   └── classification_service.py
│   ├── models/place.py         # Pydantic models
│   ├── db/database.py          # Database models
│   ├── utils/geoutils.py       # Geographic utilities
│   └── core/config.py          # Configuration
├── requirements.txt
└── Dockerfile
```
