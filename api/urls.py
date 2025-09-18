from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Route information
    path('info/', views.route_info, name='route_info'),
    
    # Cities endpoints
    path('cities/', views.city_list, name='city_list'),
    path('cities/<int:city_id>/', views.city_detail, name='city_detail'),
    path('cities/search/', views.search_cities, name='search_cities'),
    
    # Road connections
    path('connections/', views.road_connections, name='road_connections'),
    
    # Route calculation (main endpoint)
    path('calculate-route/', views.calculate_route, name='calculate_route'),
]
