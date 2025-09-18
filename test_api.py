#!/usr/bin/env python
"""
Test script for the Nigerian City Distance Calculator API.
This script tests the main functionality of the API.
"""
import requests
import json
import time

# API base URLs
DJANGO_API_BASE = "http://localhost:8000/api"
FASTAPI_BASE = "http://localhost:8001"

def test_django_api():
    """Test Django REST Framework endpoints."""
    print("🧪 Testing Django REST Framework API...")
    
    # Test health check
    try:
        response = requests.get(f"{DJANGO_API_BASE}/health/")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Django server not running. Please start it first.")
        return False
    
    # Test cities endpoint
    try:
        response = requests.get(f"{DJANGO_API_BASE}/cities/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cities endpoint: Found {data.get('count', 0)} cities")
        else:
            print(f"❌ Cities endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cities endpoint error: {e}")
    
    # Test route calculation
    test_routes = [
        ("Lagos", "Abuja"),
        ("Kano", "Port Harcourt"),
        ("Ibadan", "Kaduna"),
        ("Benin City", "Maiduguri")
    ]
    
    for from_city, to_city in test_routes:
        try:
            payload = {"from_city": from_city, "to_city": to_city}
            response = requests.post(
                f"{DJANGO_API_BASE}/calculate-route/",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    distance = data.get('total_distance', 0)
                    print(f"✅ Route {from_city} → {to_city}: {distance}km")
                else:
                    print(f"⚠️  Route {from_city} → {to_city}: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ Route {from_city} → {to_city}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Route {from_city} → {to_city}: {e}")
    
    return True

def test_fastapi():
    """Test FastAPI endpoints."""
    print("\n🧪 Testing FastAPI...")
    
    try:
        response = requests.get(f"{FASTAPI_BASE}/health")
        if response.status_code == 200:
            print("✅ FastAPI health check passed")
        else:
            print(f"❌ FastAPI health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ FastAPI server not running. Please start it first.")
        return False
    
    # Test cities endpoint
    try:
        response = requests.get(f"{FASTAPI_BASE}/cities")
        if response.status_code == 200:
            cities = response.json()
            print(f"✅ FastAPI cities: Found {len(cities)} cities")
        else:
            print(f"❌ FastAPI cities failed: {response.status_code}")
    except Exception as e:
        print(f"❌ FastAPI cities error: {e}")
    
    # Test route calculation
    try:
        payload = {"from_city": "Lagos", "to_city": "Abuja"}
        response = requests.post(f"{FASTAPI_BASE}/calculate-route", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                distance = data.get('total_distance', 0)
                print(f"✅ FastAPI route Lagos → Abuja: {distance}km")
            else:
                print(f"⚠️  FastAPI route failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ FastAPI route failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ FastAPI route error: {e}")
    
    return True

def main():
    """Main test function."""
    print("🇳🇬 Nigerian City Distance Calculator API Test")
    print("=" * 50)
    
    print("⏳ Waiting for servers to start...")
    time.sleep(3)
    
    # Test Django API
    django_success = test_django_api()
    
    # Test FastAPI
    fastapi_success = test_fastapi()
    
    print("\n" + "=" * 50)
    if django_success and fastapi_success:
        print("🎉 All tests completed!")
        print("\n📚 Available endpoints:")
        print("   Django REST API: http://localhost:8000/api/")
        print("   FastAPI Docs:    http://localhost:8001/docs")
        print("   Django Admin:    http://localhost:8000/admin/")
    else:
        print("❌ Some tests failed. Please check the server logs.")
    
    print("\n💡 Tip: Visit http://localhost:8001/docs for interactive API testing!")

if __name__ == "__main__":
    main()
