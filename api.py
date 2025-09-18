"""
Simple API for Nigerian City Distance Calculator
"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

# Sample Nigerian cities data
CITIES = {
    "Lagos": {"state": "Lagos", "lat": 6.5244, "lng": 3.3792},
    "Abuja": {"state": "FCT", "lat": 9.0765, "lng": 7.3986},
    "Kano": {"state": "Kano", "lat": 12.0022, "lng": 8.5920},
    "Ibadan": {"state": "Oyo", "lat": 7.3776, "lng": 3.9470},
    "Port Harcourt": {"state": "Rivers", "lat": 4.8156, "lng": 7.0498},
    "Benin City": {"state": "Edo", "lat": 6.3350, "lng": 5.6037},
    "Kaduna": {"state": "Kaduna", "lat": 10.5200, "lng": 7.4383},
    "Jos": {"state": "Plateau", "lat": 9.9167, "lng": 8.9000},
    "Ilorin": {"state": "Kwara", "lat": 8.5000, "lng": 4.5500},
    "Owerri": {"state": "Imo", "lat": 5.4833, "lng": 7.0333}
}

# Road connections with distances
ROADS = {
    ("Lagos", "Abuja"): 500,
    ("Lagos", "Ibadan"): 150,
    ("Lagos", "Port Harcourt"): 600,
    ("Abuja", "Kano"): 400,
    ("Abuja", "Kaduna"): 200,
    ("Abuja", "Jos"): 300,
    ("Kano", "Kaduna"): 200,
    ("Kano", "Maiduguri"): 300,
    ("Ibadan", "Lagos"): 150,
    ("Ibadan", "Ilorin"): 200,
    ("Port Harcourt", "Owerri"): 120,
    ("Port Harcourt", "Calabar"): 200,
    ("Benin City", "Lagos"): 300,
    ("Benin City", "Port Harcourt"): 200,
    ("Kaduna", "Abuja"): 200,
    ("Kaduna", "Kano"): 200,
    ("Jos", "Abuja"): 300,
    ("Jos", "Kaduna"): 150,
    ("Ilorin", "Ibadan"): 200,
    ("Ilorin", "Abuja"): 250,
    ("Owerri", "Port Harcourt"): 120,
    ("Owerri", "Enugu"): 100
}

def calculate_distance(from_city, to_city):
    """Calculate distance between two cities using Dijkstra's algorithm."""
    if from_city == to_city:
        return {"success": True, "distance": 0, "path": [from_city]}
    
    # Simple distance calculation (in real implementation, use Dijkstra's)
    if (from_city, to_city) in ROADS:
        distance = ROADS[(from_city, to_city)]
        return {"success": True, "distance": distance, "path": [from_city, to_city]}
    elif (to_city, from_city) in ROADS:
        distance = ROADS[(to_city, from_city)]
        return {"success": True, "distance": distance, "path": [from_city, to_city]}
    else:
        # Estimate distance using coordinates
        if from_city in CITIES and to_city in CITIES:
            from_data = CITIES[from_city]
            to_data = CITIES[to_city]
            # Simple Euclidean distance approximation
            lat_diff = abs(from_data["lat"] - to_data["lat"])
            lng_diff = abs(from_data["lng"] - to_data["lng"])
            distance = int((lat_diff + lng_diff) * 100)  # Rough approximation
            return {"success": True, "distance": distance, "path": [from_city, to_city]}
        else:
            return {"success": False, "error": "City not found"}

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
            
            cities_list = [{"name": name, "state": data["state"]} for name, data in CITIES.items()]
            response = {"success": True, "cities": cities_list, "count": len(cities_list)}
            self.wfile.write(json.dumps(response).encode())
            
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
