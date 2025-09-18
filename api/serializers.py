from rest_framework import serializers
from cities.models import City, RoadConnection


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model."""
    
    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'latitude', 'longitude', 'population', 'is_capital']


class RoadConnectionSerializer(serializers.ModelSerializer):
    """Serializer for RoadConnection model."""
    from_city_name = serializers.CharField(source='from_city.name', read_only=True)
    to_city_name = serializers.CharField(source='to_city.name', read_only=True)
    
    class Meta:
        model = RoadConnection
        fields = ['id', 'from_city', 'to_city', 'from_city_name', 'to_city_name', 
                 'distance_km', 'road_type', 'is_bidirectional']


class RouteCalculationSerializer(serializers.Serializer):
    """Serializer for route calculation requests."""
    from_city = serializers.CharField(max_length=100, help_text="Name of the starting city")
    to_city = serializers.CharField(max_length=100, help_text="Name of the destination city")
    
    def validate_from_city(self, value):
        """Validate that the from_city exists."""
        if not City.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f"City '{value}' not found in database")
        return value
    
    def validate_to_city(self, value):
        """Validate that the to_city exists."""
        if not City.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f"City '{value}' not found in database")
        return value


class RouteResultSerializer(serializers.Serializer):
    """Serializer for route calculation results."""
    success = serializers.BooleanField()
    total_distance = serializers.FloatField(allow_null=True)
    path = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    cities = serializers.ListField(child=serializers.DictField(), allow_empty=True)
    from_city = serializers.DictField(allow_null=True)
    to_city = serializers.DictField(allow_null=True)
    error = serializers.CharField(allow_null=True, required=False)
