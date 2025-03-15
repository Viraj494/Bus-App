from fastapi import FastAPI, HTTPException, Query
import requests
import os

app = FastAPI()

# Google Places API Key
GOOGLE_PLACES_API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"

@app.get("/recommend-places/")
def recommend_places(latitude: float, longitude: float, category: str = "bus_station"):
    """Fetch recommended places near the user's location."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": 5000,  # Search within 5km
        "type": category,  # Can be "restaurant", "hotel", "bus_station", etc.
        "key": GOOGLE_PLACES_API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "results" not in data:
        raise HTTPException(status_code=400, detail="Failed to get places")

    places = [
        {
            "name": place["name"],
            "address": place.get("vicinity", "Address not available"),
            "rating": place.get("rating", "No rating"),
            "location": place["geometry"]["location"]
        }
        for place in data["results"]
    ]

    return {"places": places}
