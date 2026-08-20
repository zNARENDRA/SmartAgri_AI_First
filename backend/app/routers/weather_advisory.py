from typing import Optional
from fastapi import APIRouter, Query
from app.schemas import WeatherAdvisoryResponse
from app.services.weather_service import weather_service

router = APIRouter(prefix="/weather", tags=["Weather & Agro-Advisory"])

@router.get("/advisory", response_model=WeatherAdvisoryResponse)
def get_weather_advisory(
    location: str = Query("Nashik, Maharashtra", description="City, District, or State name"),
    crop: str = Query("General", description="Crop context for tailored recommendations"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude")
):
    return weather_service.get_weather_and_advisory(location_query=location, crop_context=crop, lat=lat, lon=lon)

@router.get("/current")
def get_current_realtime_weather(
    location: str = Query("", description="City, District, or Village name"),
    lat: Optional[float] = Query(None, description="GPS Latitude"),
    lon: Optional[float] = Query(None, description="GPS Longitude")
):
    """
    Dedicated Real-Time Weather & Temperature API endpoint.
    Queries live Open-Meteo API for real-time temperature, humidity, wind, precipitation, and condition.
    """
    return weather_service.get_realtime_temperature_and_weather(location_query=location, lat=lat, lon=lon)

@router.get("/geocoding")
def resolve_geocoding(
    query: str = Query(..., description="Location search query (e.g. Niphad, Ludhiana, Pune)")
):
    lat, lon, display_name = weather_service.resolve_location(location_query=query)
    return {
        "query": query,
        "location_name": display_name,
        "latitude": lat,
        "longitude": lon
    }
