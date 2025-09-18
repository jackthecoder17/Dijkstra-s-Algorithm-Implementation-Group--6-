"""
Simple API for Nigerian City Distance Calculator
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

# All 36 Nigerian states and their capitals with coordinates
CITIES = {
    # State Capitals
    "Abuja": {"state": "FCT", "lat": 9.0765, "lng": 7.3986, "is_capital": True},
    "Lagos": {"state": "Lagos", "lat": 6.5244, "lng": 3.3792, "is_capital": True},
    "Kano": {"state": "Kano", "lat": 12.0022, "lng": 8.5920, "is_capital": True},
    "Ibadan": {"state": "Oyo", "lat": 7.3776, "lng": 3.9470, "is_capital": True},
    "Port Harcourt": {"state": "Rivers", "lat": 4.8156, "lng": 7.0498, "is_capital": True},
    "Benin City": {"state": "Edo", "lat": 6.3350, "lng": 5.6037, "is_capital": True},
    "Kaduna": {"state": "Kaduna", "lat": 10.5200, "lng": 7.4383, "is_capital": True},
    "Jos": {"state": "Plateau", "lat": 9.9167, "lng": 8.9000, "is_capital": True},
    "Ilorin": {"state": "Kwara", "lat": 8.5000, "lng": 4.5500, "is_capital": True},
    "Owerri": {"state": "Imo", "lat": 5.4833, "lng": 7.0333, "is_capital": True},
    "Aba": {"state": "Abia", "lat": 5.1167, "lng": 7.3667, "is_capital": False},
    "Umuahia": {"state": "Abia", "lat": 5.5333, "lng": 7.4833, "is_capital": True},
    "Yola": {"state": "Adamawa", "lat": 9.2000, "lng": 12.4833, "is_capital": True},
    "Uyo": {"state": "Akwa Ibom", "lat": 5.0333, "lng": 7.9167, "is_capital": True},
    "Awka": {"state": "Anambra", "lat": 6.2000, "lng": 7.0833, "is_capital": True},
    "Bauchi": {"state": "Bauchi", "lat": 10.3167, "lng": 9.8333, "is_capital": True},
    "Yenagoa": {"state": "Bayelsa", "lat": 4.9167, "lng": 6.2500, "is_capital": True},
    "Makurdi": {"state": "Benue", "lat": 7.7333, "lng": 8.5333, "is_capital": True},
    "Maiduguri": {"state": "Borno", "lat": 11.8333, "lng": 13.1500, "is_capital": True},
    "Calabar": {"state": "Cross River", "lat": 4.9500, "lng": 8.3167, "is_capital": True},
    "Asaba": {"state": "Delta", "lat": 6.2000, "lng": 6.7333, "is_capital": True},
    "Abakaliki": {"state": "Ebonyi", "lat": 6.3333, "lng": 8.1000, "is_capital": True},
    "Benin City": {"state": "Edo", "lat": 6.3350, "lng": 5.6037, "is_capital": True},
    "Ado Ekiti": {"state": "Ekiti", "lat": 7.6167, "lng": 5.2167, "is_capital": True},
    "Enugu": {"state": "Enugu", "lat": 6.4500, "lng": 7.5000, "is_capital": True},
    "Gombe": {"state": "Gombe", "lat": 10.2833, "lng": 11.1667, "is_capital": True},
    "Owerri": {"state": "Imo", "lat": 5.4833, "lng": 7.0333, "is_capital": True},
    "Dutse": {"state": "Jigawa", "lat": 11.7000, "lng": 9.3333, "is_capital": True},
    "Kaduna": {"state": "Kaduna", "lat": 10.5200, "lng": 7.4383, "is_capital": True},
    "Kano": {"state": "Kano", "lat": 12.0022, "lng": 8.5920, "is_capital": True},
    "Katsina": {"state": "Katsina", "lat": 12.9833, "lng": 7.6167, "is_capital": True},
    "Birnin Kebbi": {"state": "Kebbi", "lat": 12.4500, "lng": 4.2000, "is_capital": True},
    "Lokoja": {"state": "Kogi", "lat": 7.8000, "lng": 6.7333, "is_capital": True},
    "Ilorin": {"state": "Kwara", "lat": 8.5000, "lng": 4.5500, "is_capital": True},
    "Lagos": {"state": "Lagos", "lat": 6.5244, "lng": 3.3792, "is_capital": True},
    "Lafia": {"state": "Nasarawa", "lat": 8.5000, "lng": 8.5167, "is_capital": True},
    "Minna": {"state": "Niger", "lat": 9.6167, "lng": 6.5500, "is_capital": True},
    "Abeokuta": {"state": "Ogun", "lat": 7.1500, "lng": 3.3500, "is_capital": True},
    "Akure": {"state": "Ondo", "lat": 7.2500, "lng": 5.2000, "is_capital": True},
    "Osogbo": {"state": "Osun", "lat": 7.7667, "lng": 4.5667, "is_capital": True},
    "Ibadan": {"state": "Oyo", "lat": 7.3776, "lng": 3.9470, "is_capital": True},
    "Jos": {"state": "Plateau", "lat": 9.9167, "lng": 8.9000, "is_capital": True},
    "Port Harcourt": {"state": "Rivers", "lat": 4.8156, "lng": 7.0498, "is_capital": True},
    "Sokoto": {"state": "Sokoto", "lat": 13.0667, "lng": 5.2333, "is_capital": True},
    "Jalingo": {"state": "Taraba", "lat": 8.8833, "lng": 11.3667, "is_capital": True},
    "Damaturu": {"state": "Yobe", "lat": 11.7500, "lng": 11.9667, "is_capital": True},
    "Gusau": {"state": "Zamfara", "lat": 12.1667, "lng": 6.6667, "is_capital": True},
    
    # Major cities (non-capitals)
    "Abeokuta": {"state": "Ogun", "lat": 7.1500, "lng": 3.3500, "is_capital": True},
    "Akure": {"state": "Ondo", "lat": 7.2500, "lng": 5.2000, "is_capital": True},
    "Zaria": {"state": "Kaduna", "lat": 11.0833, "lng": 7.7000, "is_capital": False},
    "Warri": {"state": "Delta", "lat": 5.5167, "lng": 5.7500, "is_capital": False},
    "Onitsha": {"state": "Anambra", "lat": 6.1667, "lng": 6.7833, "is_capital": False},
    "Kaduna": {"state": "Kaduna", "lat": 10.5200, "lng": 7.4383, "is_capital": True}
}

# Comprehensive road connections between all 36 state capitals
ROADS = {
    # Abuja connections (Federal Capital)
    ("Abuja", "Lagos"): 500,
    ("Abuja", "Kano"): 400,
    ("Abuja", "Kaduna"): 200,
    ("Abuja", "Jos"): 300,
    ("Abuja", "Ilorin"): 250,
    ("Abuja", "Lokoja"): 150,
    ("Abuja", "Minna"): 100,
    ("Abuja", "Lafia"): 180,
    
    # Lagos connections (Commercial hub)
    ("Lagos", "Ibadan"): 150,
    ("Lagos", "Abeokuta"): 100,
    ("Lagos", "Port Harcourt"): 600,
    ("Lagos", "Benin City"): 300,
    ("Lagos", "Akure"): 200,
    ("Lagos", "Osogbo"): 180,
    
    # Kano connections (Northern hub)
    ("Kano", "Kaduna"): 200,
    ("Kano", "Katsina"): 150,
    ("Kano", "Dutse"): 100,
    ("Kano", "Maiduguri"): 300,
    ("Kano", "Sokoto"): 250,
    ("Kano", "Birnin Kebbi"): 200,
    ("Kano", "Gusau"): 180,
    
    # Kaduna connections (Central Northern hub)
    ("Kaduna", "Jos"): 150,
    ("Kaduna", "Zaria"): 30,
    ("Kaduna", "Katsina"): 100,
    ("Kaduna", "Birnin Kebbi"): 150,
    ("Kaduna", "Gusau"): 120,
    
    # Jos connections (Plateau)
    ("Jos", "Bauchi"): 100,
    ("Jos", "Lafia"): 120,
    ("Jos", "Abuja"): 300,
    ("Jos", "Kaduna"): 150,
    
    # Ibadan connections (Southwest hub)
    ("Ibadan", "Ilorin"): 200,
    ("Ibadan", "Abeokuta"): 80,
    ("Ibadan", "Osogbo"): 100,
    ("Ibadan", "Akure"): 150,
    ("Ibadan", "Ado Ekiti"): 120,
    
    # Port Harcourt connections (South-south hub)
    ("Port Harcourt", "Owerri"): 120,
    ("Port Harcourt", "Uyo"): 100,
    ("Port Harcourt", "Calabar"): 200,
    ("Port Harcourt", "Yenagoa"): 80,
    ("Port Harcourt", "Asaba"): 150,
    ("Port Harcourt", "Warri"): 100,
    
    # Owerri connections (Southeast)
    ("Owerri", "Enugu"): 100,
    ("Owerri", "Awka"): 80,
    ("Owerri", "Umuahia"): 60,
    ("Owerri", "Aba"): 50,
    
    # Enugu connections (Southeast hub)
    ("Enugu", "Awka"): 100,
    ("Enugu", "Abakaliki"): 80,
    ("Enugu", "Makurdi"): 200,
    ("Enugu", "Lafia"): 150,
    
    # Cross River connections
    ("Calabar", "Uyo"): 100,
    ("Calabar", "Yenagoa"): 120,
    ("Calabar", "Port Harcourt"): 200,
    
    # Delta connections
    ("Asaba", "Benin City"): 100,
    ("Asaba", "Awka"): 80,
    ("Asaba", "Warri"): 60,
    ("Asaba", "Lokoja"): 200,
    
    # Edo connections
    ("Benin City", "Asaba"): 100,
    ("Benin City", "Akure"): 120,
    ("Benin City", "Osogbo"): 150,
    ("Benin City", "Lokoja"): 180,
    
    # Northern connections
    ("Maiduguri", "Yola"): 200,
    ("Maiduguri", "Gombe"): 150,
    ("Maiduguri", "Bauchi"): 200,
    ("Maiduguri", "Damaturu"): 100,
    
    ("Yola", "Gombe"): 100,
    ("Yola", "Jalingo"): 150,
    ("Yola", "Makurdi"): 250,
    
    ("Gombe", "Bauchi"): 100,
    ("Gombe", "Jalingo"): 120,
    ("Gombe", "Damaturu"): 80,
    
    ("Bauchi", "Jalingo"): 150,
    ("Bauchi", "Jos"): 100,
    ("Bauchi", "Kaduna"): 200,
    
    # Northwest connections
    ("Sokoto", "Gusau"): 100,
    ("Sokoto", "Birnin Kebbi"): 80,
    ("Sokoto", "Katsina"): 150,
    
    ("Gusau", "Birnin Kebbi"): 60,
    ("Gusau", "Kaduna"): 120,
    ("Gusau", "Katsina"): 100,
    
    ("Birnin Kebbi", "Katsina"): 120,
    ("Birnin Kebbi", "Kaduna"): 150,
    
    # Central connections
    ("Lokoja", "Abuja"): 150,
    ("Lokoja", "Minna"): 100,
    ("Lokoja", "Makurdi"): 120,
    ("Lokoja", "Asaba"): 200,
    
    ("Minna", "Abuja"): 100,
    ("Minna", "Kaduna"): 150,
    ("Minna", "Lokoja"): 100,
    
    ("Lafia", "Abuja"): 180,
    ("Lafia", "Jos"): 120,
    ("Lafia", "Makurdi"): 80,
    ("Lafia", "Enugu"): 150,
    
    ("Makurdi", "Lafia"): 80,
    ("Makurdi", "Enugu"): 200,
    ("Makurdi", "Yola"): 250,
    ("Makurdi", "Lokoja"): 120,
    
    # Southwest connections
    ("Ilorin", "Abuja"): 250,
    ("Ilorin", "Lokoja"): 100,
    ("Ilorin", "Osogbo"): 80,
    ("Ilorin", "Ibadan"): 200,
    
    ("Abeokuta", "Lagos"): 100,
    ("Abeokuta", "Ibadan"): 80,
    ("Abeokuta", "Osogbo"): 120,
    
    ("Osogbo", "Ibadan"): 100,
    ("Osogbo", "Ilorin"): 80,
    ("Osogbo", "Abeokuta"): 120,
    ("Osogbo", "Ado Ekiti"): 60,
    
    ("Akure", "Ibadan"): 150,
    ("Akure", "Abeokuta"): 100,
    ("Akure", "Ado Ekiti"): 80,
    ("Akure", "Benin City"): 120,
    
    ("Ado Ekiti", "Osogbo"): 60,
    ("Ado Ekiti", "Akure"): 80,
    ("Ado Ekiti", "Ibadan"): 120,
    
    # Southeast connections
    ("Awka", "Enugu"): 100,
    ("Awka", "Asaba"): 80,
    ("Awka", "Owerri"): 80,
    ("Awka", "Onitsha"): 20,
    
    ("Umuahia", "Owerri"): 60,
    ("Umuahia", "Aba"): 40,
    ("Umuahia", "Enugu"): 100,
    
    ("Aba", "Owerri"): 50,
    ("Aba", "Umuahia"): 40,
    ("Aba", "Port Harcourt"): 50,
    ("Aba", "Onitsha"): 80,
    
    ("Abakaliki", "Enugu"): 80,
    ("Abakaliki", "Awka"): 100,
    ("Abakaliki", "Makurdi"): 200,
    
    # South-south connections
    ("Uyo", "Port Harcourt"): 100,
    ("Uyo", "Calabar"): 100,
    ("Uyo", "Yenagoa"): 80,
    
    ("Yenagoa", "Port Harcourt"): 80,
    ("Yenagoa", "Uyo"): 80,
    ("Yenagoa", "Warri"): 60,
    ("Yenagoa", "Asaba"): 100,
    
    ("Warri", "Asaba"): 60,
    ("Warri", "Yenagoa"): 60,
    ("Warri", "Benin City"): 80,
    ("Warri", "Port Harcourt"): 100,
    
    ("Onitsha", "Awka"): 20,
    ("Onitsha", "Asaba"): 40,
    ("Onitsha", "Aba"): 80,
    ("Onitsha", "Enugu"): 100,
    
    # Northeast connections
    ("Jalingo", "Yola"): 150,
    ("Jalingo", "Gombe"): 120,
    ("Jalingo", "Bauchi"): 150,
    ("Jalingo", "Makurdi"): 180,
    
    ("Damaturu", "Maiduguri"): 100,
    ("Damaturu", "Gombe"): 80,
    ("Damaturu", "Bauchi"): 120,
    ("Damaturu", "Jalingo"): 100
}

def dijkstra_algorithm(cities, roads, start, end):
    """Dijkstra's algorithm implementation for shortest path finding."""
    if start not in cities or end not in cities:
        return None, None
    
    if start == end:
        return 0, [start]
    
    # Initialize distances and previous nodes
    distances = {city: float('inf') for city in cities}
    previous = {city: None for city in cities}
    distances[start] = 0
    
    # Priority queue (using a simple list for this implementation)
    unvisited = set(cities.keys())
    
    while unvisited:
        # Find the unvisited city with the smallest distance
        current = min(unvisited, key=lambda city: distances[city])
        
        # If we've reached the end, we're done
        if current == end:
            break
            
        unvisited.remove(current)
        
        # Check all roads from current city
        for (city1, city2), distance in roads.items():
            if city1 == current and city2 in unvisited:
                alt = distances[current] + distance
                if alt < distances[city2]:
                    distances[city2] = alt
                    previous[city2] = current
            elif city2 == current and city1 in unvisited:
                alt = distances[current] + distance
                if alt < distances[city1]:
                    distances[city1] = alt
                    previous[city1] = current
    
    # If no path found
    if distances[end] == float('inf'):
        return None, None
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return distances[end], path

def calculate_distance(from_city, to_city):
    """Calculate distance between two cities using Dijkstra's algorithm."""
    # Validate input cities
    if not from_city or not to_city:
        return {
            "success": False, 
            "error": "Both from_city and to_city are required",
            "distance": None,
            "distance_unit": "km",
            "path": []
        }
    
    # Check if cities exist
    if from_city not in CITIES:
        return {
            "success": False, 
            "error": f"City '{from_city}' not found. Available cities: {', '.join(list(CITIES.keys())[:10])}...",
            "distance": None,
            "distance_unit": "km",
            "path": []
        }
    
    if to_city not in CITIES:
        return {
            "success": False, 
            "error": f"City '{to_city}' not found. Available cities: {', '.join(list(CITIES.keys())[:10])}...",
            "distance": None,
            "distance_unit": "km",
            "path": []
        }
    
    # Same city
    if from_city == to_city:
        return {
            "success": True, 
            "distance": 0, 
            "distance_unit": "km",
            "path": [from_city],
            "from_city": from_city,
            "to_city": to_city,
            "route_info": {
                "total_cities": 1,
                "direct_route": True,
                "same_city": True
            }
        }
    
    # Use Dijkstra's algorithm for optimal path
    distance, path = dijkstra_algorithm(CITIES, ROADS, from_city, to_city)
    
    if distance is None:
        return {
            "success": False, 
            "error": f"No route found between {from_city} and {to_city}",
            "distance": None,
            "distance_unit": "km",
            "path": [],
            "from_city": from_city,
            "to_city": to_city
        }
    
    return {
        "success": True, 
        "distance": distance, 
        "distance_unit": "km",
        "path": path,
        "from_city": from_city,
        "to_city": to_city,
        "route_info": {
            "total_cities": len(path),
            "direct_route": len(path) == 2,
            "total_distance_km": distance
        }
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "🇳🇬 Nigerian City Distance Calculator API",
                "version": "1.0.0",
                "description": "Calculate shortest distances between Nigerian cities",
                "endpoints": {
                    "cities": "/cities",
                    "calculate": "/calculate?from=Lagos&to=Abuja"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/cities':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            cities_list = [{"name": name, "state": data["state"], "is_capital": data["is_capital"]} for name, data in CITIES.items()]
            
            # Calculate statistics
            capitals = [city for city in cities_list if city["is_capital"]]
            major_cities = [city for city in cities_list if not city["is_capital"]]
            states = list(set([city["state"] for city in cities_list]))
            
            response = {
                "success": True, 
                "cities": cities_list, 
                "count": len(cities_list),
                "statistics": {
                    "total_cities": len(cities_list),
                    "state_capitals": len(capitals),
                    "major_cities": len(major_cities),
                    "total_states": len(states),
                    "states": sorted(states)
                },
                "metadata": {
                    "description": "All Nigerian cities with state capitals and major cities",
                    "distance_unit": "km",
                    "algorithm": "Dijkstra's Algorithm for shortest path calculation"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/docs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Swagger UI HTML
            swagger_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🇳🇬 Nigerian City Distance Calculator API - Swagger UI</title>
                <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
                <style>
                    .swagger-ui .topbar { display: none; }
                    .swagger-ui .info { margin: 20px 0; }
                    .swagger-ui .info .title { color: #2c3e50; }
                </style>
            </head>
            <body>
                <div id="swagger-ui"></div>
                <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
                <script>
                    const ui = SwaggerUIBundle({
                        url: '/openapi.json',
                        dom_id: '#swagger-ui',
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIBundle.presets.standalone
                        ],
                        layout: "BaseLayout",
                        deepLinking: true,
                        showExtensions: true,
                        showCommonExtensions: true
                    });
                </script>
            </body>
            </html>
            """
            self.wfile.write(swagger_html.encode())
            
        elif self.path == '/openapi.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # OpenAPI 3.0 specification
            openapi_spec = {
                "openapi": "3.0.0",
                "info": {
                    "title": "🇳🇬 Nigerian City Distance Calculator API",
                    "description": "Calculate shortest distances between Nigerian cities using Dijkstra's Algorithm",
                    "version": "1.0.0",
                    "contact": {
                        "name": "API Support",
                        "email": "support@example.com"
                    }
                },
                "servers": [
                    {
                        "url": "https://csc-320-backend-8dg58vzc8-jackthecoder17s-projects.vercel.app",
                        "description": "Production server"
                    }
                ],
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Get API information",
                            "description": "Returns API information and available endpoints",
                            "responses": {
                                "200": {
                                    "description": "Successful response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "message": {"type": "string"},
                                                    "version": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "endpoints": {"type": "object"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "/cities": {
                        "get": {
                            "summary": "Get all cities",
                            "description": "Returns a list of all available Nigerian cities",
                            "responses": {
                                "200": {
                                    "description": "Successful response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "success": {"type": "boolean"},
                                                    "cities": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "name": {"type": "string"},
                                                                "state": {"type": "string"},
                                                                "is_capital": {"type": "boolean"}
                                                            }
                                                        }
                                                    },
                                                    "count": {"type": "integer"},
                                                    "statistics": {
                                                        "type": "object",
                                                        "properties": {
                                                            "total_cities": {"type": "integer"},
                                                            "state_capitals": {"type": "integer"},
                                                            "major_cities": {"type": "integer"},
                                                            "total_states": {"type": "integer"},
                                                            "states": {"type": "array", "items": {"type": "string"}}
                                                        }
                                                    },
                                                    "metadata": {
                                                        "type": "object",
                                                        "properties": {
                                                            "description": {"type": "string"},
                                                            "distance_unit": {"type": "string"},
                                                            "algorithm": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "/calculate-route": {
                        "post": {
                            "summary": "Calculate route between cities",
                            "description": "Calculate the shortest distance between two Nigerian cities",
                            "requestBody": {
                                "required": True,
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "from_city": {"type": "string", "example": "Lagos"},
                                                "to_city": {"type": "string", "example": "Abuja"}
                                            },
                                            "required": ["from_city", "to_city"]
                                        }
                                    }
                                }
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful calculation",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "success": {"type": "boolean"},
                                                    "distance": {"type": "number"},
                                                    "path": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "/calculate": {
                        "get": {
                            "summary": "Quick route calculation",
                            "description": "Calculate route using query parameters",
                            "parameters": [
                                {
                                    "name": "from",
                                    "in": "query",
                                    "required": True,
                                    "schema": {"type": "string"},
                                    "example": "Lagos"
                                },
                                {
                                    "name": "to",
                                    "in": "query",
                                    "required": True,
                                    "schema": {"type": "string"},
                                    "example": "Abuja"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful calculation",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "success": {"type": "boolean"},
                                                    "distance": {"type": "number"},
                                                    "path": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "City": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "state": {"type": "string"}
                            }
                        },
                        "RouteResponse": {
                            "type": "object",
                            "properties": {
                                "success": {"type": "boolean"},
                                "distance": {"type": "number"},
                                "path": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
            self.wfile.write(json.dumps(openapi_spec).encode())
            
        elif self.path.startswith('/calculate'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Parse query parameters
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            from_city = query_params.get('from', [None])[0]
            to_city = query_params.get('to', [None])[0]
            
            if not from_city or not to_city:
                response = {"success": False, "error": "Missing from or to parameter"}
            else:
                result = calculate_distance(from_city, to_city)
                response = result
                
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/calculate-route':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                from_city = data.get('from_city')
                to_city = data.get('to_city')
                
                if not from_city or not to_city:
                    response = {"success": False, "error": "Missing from_city or to_city"}
                else:
                    result = calculate_distance(from_city, to_city)
                    response = result
                    
            except json.JSONDecodeError:
                response = {"success": False, "error": "Invalid JSON"}
                
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
