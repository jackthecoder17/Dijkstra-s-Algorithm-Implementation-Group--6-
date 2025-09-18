# Nigerian City Distance Calculator

A Django REST API that calculates the shortest distance between Nigerian cities using Dijkstra's Algorithm. This project provides both Django REST Framework endpoints and FastAPI documentation for easy integration with frontend applications.

## 🚀 Features

- **Dijkstra's Algorithm Implementation**: Efficient shortest path calculation between cities
- **Nigerian Cities Database**: Pre-populated with major Nigerian cities and their coordinates
- **Road Network**: Realistic road connections between cities with actual distances
- **REST API**: Django REST Framework endpoints for easy integration
- **FastAPI Documentation**: Modern API documentation with interactive testing
- **CORS Support**: Ready for frontend integration
- **Vercel Ready**: Configured for easy deployment on Vercel

## 🏗️ Project Structure

```
CSC320BACKEND/
├── city_distance_calculator/     # Django project settings
├── cities/                       # Cities app with models
│   ├── models.py                # City and RoadConnection models
│   ├── admin.py                 # Django admin configuration
│   └── management/commands/     # Database population commands
├── api/                         # API endpoints
│   ├── dijkstra.py             # Dijkstra's algorithm implementation
│   ├── views.py                # Django REST Framework views
│   ├── serializers.py          # Data serializers
│   └── urls.py                 # API URL patterns
├── fastapi_app.py              # FastAPI application for documentation
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CSC320BACKEND
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate database with Nigerian cities
python manage.py populate_nigerian_cities
```

### 5. Run the Development Server

```bash
# Django REST Framework server
python manage.py runserver

# FastAPI server (for documentation)
python fastapi_app.py
```

## 📚 API Documentation

### Django REST Framework Endpoints

Base URL: `http://localhost:8000/api/`

#### 1. Health Check
```http
GET /api/health/
```

#### 2. Get All Cities
```http
GET /api/cities/
```

#### 3. Search Cities
```http
GET /api/cities/search/?q=Lagos
```

#### 4. Calculate Route (Main Endpoint)
```http
POST /api/calculate-route/
Content-Type: application/json

{
    "from_city": "Lagos",
    "to_city": "Abuja"
}
```

#### 5. Get Route Information
```http
GET /api/info/
```

### FastAPI Documentation

FastAPI provides interactive documentation at:
- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

## 🔧 API Usage Examples

### Calculate Distance Between Cities

```bash
curl -X POST "http://localhost:8000/api/calculate-route/" \
     -H "Content-Type: application/json" \
     -d '{
       "from_city": "Lagos",
       "to_city": "Abuja"
     }'
```

**Response:**
```json
{
    "success": true,
    "total_distance": 500.0,
    "path": [1, 2, 3],
    "cities": [
        {
            "id": 1,
            "name": "Lagos",
            "state": "Lagos",
            "latitude": 6.5244,
            "longitude": 3.3792
        },
        {
            "id": 2,
            "name": "Ibadan",
            "state": "Oyo",
            "latitude": 7.3776,
            "longitude": 3.9470
        },
        {
            "id": 3,
            "name": "Abuja",
            "state": "FCT",
            "latitude": 9.0765,
            "longitude": 7.3986
        }
    ],
    "from_city": {
        "id": 1,
        "name": "Lagos",
        "state": "Lagos",
        "latitude": 6.5244,
        "longitude": 3.3792
    },
    "to_city": {
        "id": 3,
        "name": "Abuja",
        "state": "FCT",
        "latitude": 9.0765,
        "longitude": 7.3986
    }
}
```

### Search for Cities

```bash
curl "http://localhost:8000/api/cities/search/?q=Lagos"
```

### Get All Cities

```bash
curl "http://localhost:8000/api/cities/"
```

## 🗺️ Available Cities

The database includes major Nigerian cities:

- **Lagos** (Lagos State)
- **Abuja** (FCT)
- **Kano** (Kano State)
- **Ibadan** (Oyo State)
- **Port Harcourt** (Rivers State)
- **Benin City** (Edo State)
- **Kaduna** (Kaduna State)
- **Jos** (Plateau State)
- **Ilorin** (Kwara State)
- **Owerri** (Imo State)
- And many more...

## 🚀 Deployment on Vercel

### 1. Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Create vercel.json

```json
{
  "builds": [
    {
      "src": "manage.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "manage.py"
    }
  ]
}
```

### 3. Deploy

```bash
vercel --prod
```

### Environment Variables

Set these in your Vercel dashboard:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app
```

## 🧮 Dijkstra's Algorithm Implementation

The algorithm is implemented in `api/dijkstra.py` with the following features:

- **Graph Representation**: Cities as nodes, road connections as weighted edges
- **Priority Queue**: Efficient shortest path calculation using heapq
- **Bidirectional Roads**: Support for two-way road connections
- **Path Reconstruction**: Returns both distance and actual route

### Algorithm Complexity

- **Time Complexity**: O((V + E) log V) where V is vertices (cities) and E is edges (roads)
- **Space Complexity**: O(V) for storing distances and previous nodes

## 🧪 Testing

### Manual Testing

1. Start the development server:
```bash
python manage.py runserver
```

2. Test the main endpoint:
```bash
curl -X POST "http://localhost:8000/api/calculate-route/" \
     -H "Content-Type: application/json" \
     -d '{"from_city": "Lagos", "to_city": "Abuja"}'
```

### Using FastAPI Documentation

1. Start FastAPI server:
```bash
python fastapi_app.py
```

2. Visit `http://localhost:8001/docs` for interactive testing

## 📊 Database Schema

### City Model
- `id`: Primary key
- `name`: City name
- `state`: State name
- `latitude`: GPS latitude
- `longitude`: GPS longitude
- `population`: City population
- `is_capital`: Boolean flag for state capitals

### RoadConnection Model
- `id`: Primary key
- `from_city`: Foreign key to City
- `to_city`: Foreign key to City
- `distance_km`: Distance in kilometers
- `road_type`: Type of road (highway, federal, state, local)
- `is_bidirectional`: Boolean for two-way roads

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings

Key settings in `city_distance_calculator/settings.py`:

- CORS enabled for frontend integration
- SQLite database (easily configurable for PostgreSQL)
- WhiteNoise for static file serving
- REST Framework configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the API documentation at `/docs`
2. Review the Django admin at `/admin/`
3. Check the logs for error details

## 🎯 Future Enhancements

- [ ] Add more Nigerian cities and roads
- [ ] Implement traffic conditions
- [ ] Add route optimization for multiple stops
- [ ] Include public transportation options
- [ ] Add real-time traffic data integration
- [ ] Implement caching for better performance

---

**Built with ❤️ for Nigerian cities using Dijkstra's Algorithm**
