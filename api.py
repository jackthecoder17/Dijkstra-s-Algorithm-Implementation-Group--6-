"""
Simple API for Nigerian City Distance Calculator - Frontend Optimized (v2.0)
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

# 10 Selected Nigerian states for frontend visualization
CITIES = {
    # Northern States
    "Kano": {"state": "Kano", "lat": 12.0022, "lng": 8.5920, "is_capital": True, "region": "north"},
    "Kaduna": {"state": "Kaduna", "lat": 10.5200, "lng": 7.4383, "is_capital": True, "region": "north"},
    
    # Central States
    "Abuja": {"state": "FCT", "lat": 9.0765, "lng": 7.3986, "is_capital": True, "region": "central"},
    "Plateau": {"state": "Plateau", "lat": 9.9167, "lng": 8.9000, "is_capital": True, "region": "central"},
    "Niger": {"state": "Niger", "lat": 9.6167, "lng": 6.5500, "is_capital": True, "region": "central"},
    
    # Western States
    "Lagos": {"state": "Lagos", "lat": 6.5244, "lng": 3.3792, "is_capital": True, "region": "south"},
    "Oyo": {"state": "Oyo", "lat": 7.3776, "lng": 3.9470, "is_capital": True, "region": "south"},
    
    # Eastern States
    "Enugu": {"state": "Enugu", "lat": 6.4500, "lng": 7.5000, "is_capital": True, "region": "east"},
    "Anambra": {"state": "Anambra", "lat": 6.1667, "lng": 6.7833, "is_capital": False, "region": "east"},
    
    # South-South
    "Rivers": {"state": "Rivers", "lat": 4.8156, "lng": 7.0498, "is_capital": True, "region": "south_south"}
}

# Road connections with exact weights from frontend
ROADS = {
    # Northern backbone
    ("Kaduna", "Kano"): 160,
    ("Kano", "Kaduna"): 160,
    
    # North to Central connections
    ("Kaduna", "Abuja"): 160,
    ("Abuja", "Kaduna"): 160,
    ("Kaduna", "Niger"): 180,
    ("Niger", "Kaduna"): 180,
    ("Abuja", "Plateau"): 200,
    ("Plateau", "Abuja"): 200,
    ("Kano", "Plateau"): 280,
    ("Plateau", "Kano"): 280,
    
    # Central hub connections
    ("Niger", "Abuja"): 120,
    ("Abuja", "Niger"): 120,
    ("Niger", "Oyo"): 180,
    ("Oyo", "Niger"): 180,
    
    # Western corridor
    ("Lagos", "Oyo"): 150,
    ("Oyo", "Lagos"): 150,
    ("Oyo", "Abuja"): 250,
    ("Abuja", "Oyo"): 250,
    
    # Eastern connections
    ("Abuja", "Enugu"): 290,
    ("Enugu", "Abuja"): 290,
    ("Plateau", "Enugu"): 250,
    ("Enugu", "Plateau"): 250,
    ("Enugu", "Anambra"): 110,
    ("Anambra", "Enugu"): 110,
    
    # Southern connections
    ("Anambra", "Rivers"): 120,
    ("Rivers", "Anambra"): 120,
    ("Oyo", "Rivers"): 280,
    ("Rivers", "Oyo"): 280,
    
    # Cross-regional links
    ("Lagos", "Rivers"): 340,
    ("Rivers", "Lagos"): 340,
    ("Oyo", "Anambra"): 220,
    ("Anambra", "Oyo"): 220
}

def dijkstra_algorithm(cities, roads, start, end):
    """Dijkstra's algorithm implementation for shortest path finding."""
    if start not in cities or end not in cities:
        return None, []
    
    if start == end:
        return 0, [start]
    
    # Initialize distances and previous nodes
    distances = {city: float('inf') for city in cities}
    previous = {city: None for city in cities}
    distances[start] = 0
    
    # Priority queue: (distance, city)
    unvisited = [(0, start)]
    visited = set()
    
    while unvisited:
        # Get the city with minimum distance
        current_distance, current_city = min(unvisited)
        unvisited.remove((current_distance, current_city))
        
        if current_city in visited:
            continue
            
        visited.add(current_city)
        
        # If we reached the destination, reconstruct path
        if current_city == end:
            path = []
            while current_city is not None:
                path.append(current_city)
                current_city = previous[current_city]
            path.reverse()
            return distances[end], path
        
        # Check all neighbors
        for (city1, city2), weight in roads.items():
            if city1 == current_city and city2 not in visited:
                new_distance = current_distance + weight
                if new_distance < distances[city2]:
                    distances[city2] = new_distance
                    previous[city2] = current_city
                    unvisited.append((new_distance, city2))
    
    return None, []

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
            "error": f"City '{from_city}' not found. Available cities: {', '.join(list(CITIES.keys()))}",
            "distance": None,
            "distance_unit": "km",
            "path": []
        }
    
    if to_city not in CITIES:
        return {
            "success": False, 
            "error": f"City '{to_city}' not found. Available cities: {', '.join(list(CITIES.keys()))}",
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
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if path == '/cities':
            # Return all cities
            cities_list = []
            for name, data in CITIES.items():
                cities_list.append({
                    "name": name,
                    "state": data["state"],
                    "lat": data["lat"],
                    "lng": data["lng"],
                    "is_capital": data["is_capital"],
                    "region": data["region"]
                })
            
            response = {
                "success": True,
                "cities": cities_list,
                "total": len(cities_list)
            }
            
        elif path == '/calculate':
            # Calculate route via GET
            from_city = query_params.get('from', [None])[0]
            to_city = query_params.get('to', [None])[0]
            
            response = calculate_distance(from_city, to_city)
            
        elif path == '/docs':
            # Serve Swagger UI
            swagger_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Nigerian City Distance Calculator API</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin:0; background: #fafafa; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>
            """
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(swagger_html.encode())
            return
            
        elif path == '/openapi.json':
            # OpenAPI specification
            openapi_spec = {
                "openapi": "3.0.0",
                "info": {
                    "title": "Nigerian City Distance Calculator API",
                    "description": "API for calculating shortest routes between Nigerian cities using Dijkstra's algorithm",
                    "version": "1.0.0"
                },
                "servers": [
                    {
                        "url": "https://csc-320-backend.vercel.app",
                        "description": "Production server"
                    }
                ],
                "paths": {
                    "/cities": {
                        "get": {
                            "summary": "Get all cities",
                            "description": "Retrieve list of all available Nigerian cities",
                            "responses": {
                                "200": {
                                    "description": "List of cities",
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
                                                                "lat": {"type": "number"},
                                                                "lng": {"type": "number"},
                                                                "is_capital": {"type": "boolean"},
                                                                "region": {"type": "string"}
                                                            }
                                                        }
                                                    },
                                                    "total": {"type": "integer"}
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
                            "summary": "Calculate route (GET)",
                            "description": "Calculate shortest route between two cities using GET method",
                            "parameters": [
                                {
                                    "name": "from",
                                    "in": "query",
                                    "required": True,
                                    "schema": {"type": "string"},
                                    "description": "Starting city"
                                },
                                {
                                    "name": "to",
                                    "in": "query",
                                    "required": True,
                                    "schema": {"type": "string"},
                                    "description": "Destination city"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Route calculation result",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "success": {"type": "boolean"},
                                                    "distance": {"type": "number"},
                                                    "distance_unit": {"type": "string"},
                                                    "path": {"type": "array", "items": {"type": "string"}},
                                                    "from_city": {"type": "string"},
                                                    "to_city": {"type": "string"},
                                                    "route_info": {"type": "object"}
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
                            "summary": "Calculate route (POST)",
                            "description": "Calculate shortest route between two cities using POST method",
                            "requestBody": {
                                "required": True,
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "from_city": {"type": "string"},
                                                "to_city": {"type": "string"}
                                            },
                                            "required": ["from_city", "to_city"]
                                        }
                                    }
                                }
                            },
                            "responses": {
                                "200": {
                                    "description": "Route calculation result",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "properties": {
                                                    "success": {"type": "boolean"},
                                                    "distance": {"type": "number"},
                                                    "distance_unit": {"type": "string"},
                                                    "path": {"type": "array", "items": {"type": "string"}},
                                                    "from_city": {"type": "string"},
                                                    "to_city": {"type": "string"},
                                                    "route_info": {"type": "object"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(openapi_spec, indent=2).encode())
            return
            
        else:
            # Root endpoint
            response = {
                "message": "Nigerian City Distance Calculator API",
                "version": "1.0.0",
                "endpoints": {
                    "GET /cities": "Get all available cities",
                    "GET /calculate?from=City1&to=City2": "Calculate route (GET method)",
                    "POST /calculate-route": "Calculate route (POST method)",
                    "GET /docs": "API documentation (Swagger UI)",
                    "GET /openapi.json": "OpenAPI specification"
                },
                "available_cities": list(CITIES.keys())
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/calculate-route':
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                from_city = data.get('from_city')
                to_city = data.get('to_city')
                
                response = calculate_distance(from_city, to_city)
                
            except json.JSONDecodeError:
                response = {
                    "success": False,
                    "error": "Invalid JSON in request body",
                    "distance": None,
                    "distance_unit": "km",
                    "path": []
                }
        else:
            response = {
                "success": False,
                "error": "Endpoint not found",
                "distance": None,
                "distance_unit": "km",
                "path": []
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()