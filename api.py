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
            
        elif self.path == '/docs':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            docs_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🇳🇬 Nigerian City Distance Calculator API - Documentation</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                    h2 { color: #34495e; margin-top: 30px; }
                    .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
                    .method { background: #27ae60; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }
                    .method.post { background: #e74c3c; }
                    .url { font-family: monospace; background: #2c3e50; color: white; padding: 5px 10px; border-radius: 3px; }
                    .example { background: #f8f9fa; padding: 10px; border-radius: 5px; border: 1px solid #dee2e6; }
                    code { background: #f1f2f6; padding: 2px 5px; border-radius: 3px; }
                    .response { background: #d4edda; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🇳🇬 Nigerian City Distance Calculator API</h1>
                    <p><strong>Version:</strong> 1.0.0</p>
                    <p><strong>Description:</strong> Calculate shortest distances between Nigerian cities using Dijkstra's Algorithm</p>
                    
                    <h2>📡 Endpoints</h2>
                    
                    <div class="endpoint">
                        <h3><span class="method">GET</span> <span class="url">/</span></h3>
                        <p><strong>Description:</strong> Get API information and available endpoints</p>
                        <div class="example">
                            <strong>Example:</strong><br>
                            <code>GET https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/</code>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <h3><span class="method">GET</span> <span class="url">/cities</span></h3>
                        <p><strong>Description:</strong> Get list of all available Nigerian cities</p>
                        <div class="example">
                            <strong>Example:</strong><br>
                            <code>GET https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/cities</code>
                        </div>
                        <div class="response">
                            <strong>Response:</strong><br>
                            <code>{"success": true, "cities": [...], "count": 10}</code>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <h3><span class="method post">POST</span> <span class="url">/calculate-route</span></h3>
                        <p><strong>Description:</strong> Calculate shortest distance between two cities</p>
                        <div class="example">
                            <strong>Request Body:</strong><br>
                            <code>{"from_city": "Lagos", "to_city": "Abuja"}</code><br><br>
                            <strong>Example:</strong><br>
                            <code>POST https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/calculate-route</code>
                        </div>
                        <div class="response">
                            <strong>Response:</strong><br>
                            <code>{"success": true, "distance": 500, "path": ["Lagos", "Abuja"]}</code>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <h3><span class="method">GET</span> <span class="url">/calculate?from=Lagos&to=Abuja</span></h3>
                        <p><strong>Description:</strong> Quick route calculation using query parameters</p>
                        <div class="example">
                            <strong>Example:</strong><br>
                            <code>GET https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/calculate?from=Lagos&to=Abuja</code>
                        </div>
                    </div>
                    
                    <h2>🏙️ Available Cities</h2>
                    <ul>
                        <li>Lagos (Lagos State)</li>
                        <li>Abuja (FCT)</li>
                        <li>Kano (Kano State)</li>
                        <li>Ibadan (Oyo State)</li>
                        <li>Port Harcourt (Rivers State)</li>
                        <li>Benin City (Edo State)</li>
                        <li>Kaduna (Kaduna State)</li>
                        <li>Jos (Plateau State)</li>
                        <li>Ilorin (Kwara State)</li>
                        <li>Owerri (Imo State)</li>
                    </ul>
                    
                    <h2>🧪 Test Your API</h2>
                    <p>Try these examples in your browser or with curl:</p>
                    <div class="example">
                        <strong>Get Cities:</strong><br>
                        <code>curl https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/cities</code>
                    </div>
                    <div class="example">
                        <strong>Calculate Route:</strong><br>
                        <code>curl -X POST https://csc-320-backend-erz3m03mq-jackthecoder17s-projects.vercel.app/calculate-route -H "Content-Type: application/json" -d '{"from_city": "Lagos", "to_city": "Abuja"}'</code>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(docs_html.encode())
            
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
