from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from cities.models import City, RoadConnection
from .serializers import (
    CitySerializer, 
    RoadConnectionSerializer, 
    RouteCalculationSerializer,
    RouteResultSerializer
)
from .dijkstra import calculate_shortest_route
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def root_view(request):
    """Root endpoint with API information."""
    return JsonResponse({
        'message': '🇳🇬 Nigerian City Distance Calculator API',
        'version': '1.0.0',
        'description': 'Calculate shortest distances between Nigerian cities using Dijkstra\'s Algorithm',
        'endpoints': {
            'api_docs': 'http://localhost:8001/docs',
            'health_check': '/api/health/',
            'cities': '/api/cities/',
            'calculate_route': '/api/calculate-route/',
            'search_cities': '/api/cities/search/?q=city_name'
        },
        'example_usage': {
            'calculate_route': {
                'method': 'POST',
                'url': '/api/calculate-route/',
                'body': {
                    'from_city': 'Lagos',
                    'to_city': 'Abuja'
                }
            }
        }
    })


@api_view(['GET'])
def city_list(request):
    """Get list of all cities."""
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response({
        'success': True,
        'cities': serializer.data,
        'count': cities.count()
    })


@api_view(['GET'])
def city_detail(request, city_id):
    """Get details of a specific city."""
    city = get_object_or_404(City, id=city_id)
    serializer = CitySerializer(city)
    return Response({
        'success': True,
        'city': serializer.data
    })


@api_view(['GET'])
def search_cities(request):
    """Search cities by name or state."""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({
            'success': False,
            'error': 'Query parameter "q" is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cities = City.objects.filter(
        name__icontains=query
    ).union(
        City.objects.filter(state__icontains=query)
    ).distinct()
    
    serializer = CitySerializer(cities, many=True)
    return Response({
        'success': True,
        'cities': serializer.data,
        'count': cities.count(),
        'query': query
    })


@api_view(['GET'])
def road_connections(request):
    """Get all road connections."""
    connections = RoadConnection.objects.select_related('from_city', 'to_city').all()
    serializer = RoadConnectionSerializer(connections, many=True)
    return Response({
        'success': True,
        'connections': serializer.data,
        'count': connections.count()
    })


@api_view(['POST'])
def calculate_route(request):
    """
    Calculate shortest route between two cities using Dijkstra's algorithm.
    
    Expected JSON payload:
    {
        "from_city": "Lagos",
        "to_city": "Abuja"
    }
    """
    serializer = RouteCalculationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Invalid input data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    from_city = serializer.validated_data['from_city']
    to_city = serializer.validated_data['to_city']
    
    try:
        # Calculate route using Dijkstra's algorithm
        result = calculate_shortest_route(from_city, to_city)
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error calculating route: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error occurred while calculating route',
            'total_distance': None,
            'path': [],
            'cities': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def route_info(request):
    """Get information about available routes and cities."""
    total_cities = City.objects.count()
    total_connections = RoadConnection.objects.count()
    
    # Get some sample cities
    sample_cities = City.objects.filter(is_capital=True)[:5]
    sample_serializer = CitySerializer(sample_cities, many=True)
    
    return Response({
        'success': True,
        'info': {
            'total_cities': total_cities,
            'total_road_connections': total_connections,
            'description': 'Nigerian City Distance Calculator using Dijkstra\'s Algorithm',
            'sample_cities': sample_serializer.data
        }
    })


@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'service': 'Nigerian City Distance Calculator API',
        'version': '1.0.0'
    })