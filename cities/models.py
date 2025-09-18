from django.db import models


class City(models.Model):
    """Model representing a Nigerian city."""
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    population = models.IntegerField(null=True, blank=True)
    is_capital = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.state}"


class RoadConnection(models.Model):
    """Model representing road connections between cities."""
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='outgoing_roads')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='incoming_roads')
    distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    road_type = models.CharField(max_length=50, choices=[
        ('highway', 'Highway'),
        ('expressway', 'Expressway'),
        ('federal', 'Federal Road'),
        ('state', 'State Road'),
        ('local', 'Local Road'),
    ], default='federal')
    is_bidirectional = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['from_city', 'to_city']
        ordering = ['from_city__name', 'to_city__name']
    
    def __str__(self):
        return f"{self.from_city.name} → {self.to_city.name} ({self.distance_km}km)"
