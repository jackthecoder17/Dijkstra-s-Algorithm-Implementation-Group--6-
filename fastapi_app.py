"""
FastAPI application for API documentation and testing.
This provides a modern API interface alongside Django REST Framework.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'city_distance_calculator.settings')
django.setup()

from api.dijkstra import calculate_shortest_route
from cities.models import City, RoadConnection

# Create FastAPI app
app = FastAPI(
    title="Nigerian City Distance Calculator API",
    description="A REST API for calculating shortest distances between Nigerian cities using Dijkstra's Algorithm",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CityResponse(BaseModel):
    id: int
    name: str
    state: str
    latitude: float
    longitude: float
    population: Optional[int] = None
    is_capital: bool = False

class RouteRequest(BaseModel):
    from_city: str
    to_city: str

class RouteResponse(BaseModel):
    success: bool
    total_distance: Optional[float] = None
    path: List[int] = []
    cities: List[Dict[str, Any]] = []
    from_city: Optional[Dict[str, Any]] = None
    to_city: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Nigerian City Distance Calculator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="Nigerian City Distance Calculator API",
        version="1.0.0"
    )

@app.get("/cities", response_model=List[CityResponse])
async def get_cities():
    """Get all cities in the database."""
    cities = City.objects.all()
    return [
        CityResponse(
            id=city.id,
            name=city.name,
            state=city.state,
            latitude=float(city.latitude),
            longitude=float(city.longitude),
            population=city.population,
            is_capital=city.is_capital
        )
        for city in cities
    ]

@app.get("/cities/{city_id}", response_model=CityResponse)
async def get_city(city_id: int):
    """Get a specific city by ID."""
    try:
        city = City.objects.get(id=city_id)
        return CityResponse(
            id=city.id,
            name=city.name,
            state=city.state,
            latitude=float(city.latitude),
            longitude=float(city.longitude),
            population=city.population,
            is_capital=city.is_capital
        )
    except City.DoesNotExist:
        raise HTTPException(status_code=404, detail="City not found")

@app.get("/cities/search/{query}", response_model=List[CityResponse])
async def search_cities(query: str):
    """Search cities by name or state."""
    cities = City.objects.filter(
        name__icontains=query
    ).union(
        City.objects.filter(state__icontains=query)
    ).distinct()
    
    return [
        CityResponse(
            id=city.id,
            name=city.name,
            state=city.state,
            latitude=float(city.latitude),
            longitude=float(city.longitude),
            population=city.population,
            is_capital=city.is_capital
        )
        for city in cities
    ]

@app.post("/calculate-route", response_model=RouteResponse)
async def calculate_route(request: RouteRequest):
    """
    Calculate the shortest route between two cities using Dijkstra's Algorithm.
    
    This endpoint finds the shortest path between two Nigerian cities using
    Dijkstra's algorithm, considering all available road connections.
    """
    result = calculate_shortest_route(request.from_city, request.to_city)
    return RouteResponse(**result)

@app.get("/info")
async def get_api_info():
    """Get information about the API and available data."""
    total_cities = City.objects.count()
    total_connections = RoadConnection.objects.count()
    
    sample_cities = City.objects.filter(is_capital=True)[:5]
    
    return {
        "total_cities": total_cities,
        "total_road_connections": total_connections,
        "description": "Nigerian City Distance Calculator using Dijkstra's Algorithm",
        "sample_cities": [
            {
                "id": city.id,
                "name": city.name,
                "state": city.state,
                "is_capital": city.is_capital
            }
            for city in sample_cities
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
