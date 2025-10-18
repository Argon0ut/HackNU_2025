from fastapi import FastAPI
from app.api.routes.parser import router as parser_router
from dotenv import load_dotenv
from app.core.config import settings

import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Travel Places Parser API",
    description="API for parsing and classifying travel-related places from Google Places and 2GIS",
    version="1.0.0"
)

# Include routers
app.include_router(parser_router)

@app.get("/")
async def root():
    return {
        "message": "Travel Places Parser API",
        "version": "1.0.0",
        "endpoints": {
            "parse_places": "/api/parse_places",
            "parse_places_google": "/api/parse_places/google", 
            "parse_places_2gis": "/api/parse_places/2gis",
            "classification_stats": "/api/classify"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
