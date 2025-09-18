from django.contrib import admin
from .models import City, RoadConnection


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'latitude', 'longitude', 'population', 'is_capital']
    list_filter = ['state', 'is_capital']
    search_fields = ['name', 'state']
    ordering = ['name']


@admin.register(RoadConnection)
class RoadConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_city', 'to_city', 'distance_km', 'road_type', 'is_bidirectional']
    list_filter = ['road_type', 'is_bidirectional']
    search_fields = ['from_city__name', 'to_city__name']
    ordering = ['from_city__name']
