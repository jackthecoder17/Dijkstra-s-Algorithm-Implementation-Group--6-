from django.core.management.base import BaseCommand
from cities.models import City, RoadConnection
import math


class Command(BaseCommand):
    help = 'Populate database with Nigerian cities and road connections'

    def handle(self, *args, **options):
        # Major Nigerian cities with coordinates
        cities_data = [
            # Major cities and capitals
            {'name': 'Lagos', 'state': 'Lagos', 'lat': 6.5244, 'lng': 3.3792, 'pop': 15388000, 'capital': True},
            {'name': 'Abuja', 'state': 'FCT', 'lat': 9.0765, 'lng': 7.3986, 'pop': 356412, 'capital': True},
            {'name': 'Kano', 'state': 'Kano', 'lat': 12.0022, 'lng': 8.5920, 'pop': 2828861, 'capital': True},
            {'name': 'Ibadan', 'state': 'Oyo', 'lat': 7.3776, 'lng': 3.9470, 'pop': 3160000, 'capital': True},
            {'name': 'Port Harcourt', 'state': 'Rivers', 'lat': 4.8156, 'lng': 7.0498, 'pop': 1000000, 'capital': True},
            {'name': 'Benin City', 'state': 'Edo', 'lat': 6.3350, 'lng': 5.6037, 'pop': 1495000, 'capital': True},
            {'name': 'Kaduna', 'state': 'Kaduna', 'lat': 10.5200, 'lng': 7.4383, 'pop': 760084, 'capital': True},
            {'name': 'Jos', 'state': 'Plateau', 'lat': 9.9167, 'lng': 8.9000, 'pop': 622802, 'capital': True},
            {'name': 'Ilorin', 'state': 'Kwara', 'lat': 8.5000, 'lng': 4.5500, 'pop': 777667, 'capital': True},
            {'name': 'Owerri', 'state': 'Imo', 'lat': 5.4833, 'lng': 7.0333, 'pop': 908109, 'capital': True},
            {'name': 'Aba', 'state': 'Abia', 'lat': 5.1167, 'lng': 7.3667, 'pop': 897560, 'capital': False},
            {'name': 'Maiduguri', 'state': 'Borno', 'lat': 11.8333, 'lng': 13.1500, 'pop': 1197497, 'capital': True},
            {'name': 'Zaria', 'state': 'Kaduna', 'lat': 11.0833, 'lng': 7.7000, 'pop': 408198, 'capital': False},
            {'name': 'Abeokuta', 'state': 'Ogun', 'lat': 7.1500, 'lng': 3.3500, 'pop': 593140, 'capital': True},
            {'name': 'Enugu', 'state': 'Enugu', 'lat': 6.4500, 'lng': 7.5000, 'pop': 722664, 'capital': True},
            {'name': 'Sokoto', 'state': 'Sokoto', 'lat': 13.0667, 'lng': 5.2333, 'pop': 427760, 'capital': True},
            {'name': 'Calabar', 'state': 'Cross River', 'lat': 4.9500, 'lng': 8.3167, 'pop': 461796, 'capital': True},
            {'name': 'Uyo', 'state': 'Akwa Ibom', 'lat': 5.0333, 'lng': 7.9167, 'pop': 436606, 'capital': True},
            {'name': 'Akure', 'state': 'Ondo', 'lat': 7.2500, 'lng': 5.2000, 'pop': 420594, 'capital': True},
            {'name': 'Bauchi', 'state': 'Bauchi', 'lat': 10.3167, 'lng': 9.8333, 'pop': 316149, 'capital': True},
        ]

        # Create cities
        created_cities = {}
        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                defaults={
                    'state': city_data['state'],
                    'latitude': city_data['lat'],
                    'longitude': city_data['lng'],
                    'population': city_data['pop'],
                    'is_capital': city_data['capital']
                }
            )
            created_cities[city_data['name']] = city
            if created:
                self.stdout.write(f"Created city: {city.name}")

        # Create road connections based on major highways
        road_connections = [
            # Lagos connections
            ('Lagos', 'Ibadan', 150, 'expressway'),
            ('Lagos', 'Abeokuta', 100, 'federal'),
            ('Lagos', 'Port Harcourt', 600, 'highway'),
            
            # Abuja connections
            ('Abuja', 'Kaduna', 200, 'highway'),
            ('Abuja', 'Jos', 300, 'federal'),
            ('Abuja', 'Lagos', 500, 'highway'),
            ('Abuja', 'Kano', 400, 'highway'),
            
            # Kano connections
            ('Kano', 'Kaduna', 200, 'highway'),
            ('Kano', 'Maiduguri', 300, 'federal'),
            ('Kano', 'Sokoto', 250, 'federal'),
            
            # Ibadan connections
            ('Ibadan', 'Lagos', 150, 'expressway'),
            ('Ibadan', 'Ilorin', 200, 'federal'),
            ('Ibadan', 'Abeokuta', 80, 'federal'),
            
            # Port Harcourt connections
            ('Port Harcourt', 'Aba', 50, 'federal'),
            ('Port Harcourt', 'Uyo', 100, 'federal'),
            ('Port Harcourt', 'Calabar', 200, 'federal'),
            ('Port Harcourt', 'Owerri', 120, 'federal'),
            
            # Benin City connections
            ('Benin City', 'Lagos', 300, 'federal'),
            ('Benin City', 'Port Harcourt', 200, 'federal'),
            ('Benin City', 'Aba', 150, 'federal'),
            
            # Kaduna connections
            ('Kaduna', 'Abuja', 200, 'highway'),
            ('Kaduna', 'Kano', 200, 'highway'),
            ('Kaduna', 'Jos', 150, 'federal'),
            ('Kaduna', 'Zaria', 30, 'federal'),
            
            # Jos connections
            ('Jos', 'Abuja', 300, 'federal'),
            ('Jos', 'Kaduna', 150, 'federal'),
            ('Jos', 'Bauchi', 100, 'federal'),
            
            # Ilorin connections
            ('Ilorin', 'Ibadan', 200, 'federal'),
            ('Ilorin', 'Abuja', 250, 'federal'),
            
            # Owerri connections
            ('Owerri', 'Port Harcourt', 120, 'federal'),
            ('Owerri', 'Aba', 50, 'federal'),
            ('Owerri', 'Enugu', 100, 'federal'),
            
            # Aba connections
            ('Aba', 'Port Harcourt', 50, 'federal'),
            ('Aba', 'Benin City', 150, 'federal'),
            ('Aba', 'Owerri', 50, 'federal'),
            
            # Maiduguri connections
            ('Maiduguri', 'Kano', 300, 'federal'),
            ('Maiduguri', 'Bauchi', 200, 'federal'),
            
            # Zaria connections
            ('Zaria', 'Kaduna', 30, 'federal'),
            ('Zaria', 'Sokoto', 200, 'federal'),
            
            # Abeokuta connections
            ('Abeokuta', 'Lagos', 100, 'federal'),
            ('Abeokuta', 'Ibadan', 80, 'federal'),
            
            # Enugu connections
            ('Enugu', 'Owerri', 100, 'federal'),
            ('Enugu', 'Aba', 100, 'federal'),
            
            # Sokoto connections
            ('Sokoto', 'Kano', 250, 'federal'),
            ('Sokoto', 'Zaria', 200, 'federal'),
            
            # Calabar connections
            ('Calabar', 'Port Harcourt', 200, 'federal'),
            ('Calabar', 'Uyo', 100, 'federal'),
            
            # Uyo connections
            ('Uyo', 'Port Harcourt', 100, 'federal'),
            ('Uyo', 'Calabar', 100, 'federal'),
            
            # Akure connections
            ('Akure', 'Ibadan', 150, 'federal'),
            ('Akure', 'Abeokuta', 100, 'federal'),
            
            # Bauchi connections
            ('Bauchi', 'Jos', 100, 'federal'),
            ('Bauchi', 'Maiduguri', 200, 'federal'),
        ]

        # Create road connections
        for from_city_name, to_city_name, distance, road_type in road_connections:
            if from_city_name in created_cities and to_city_name in created_cities:
                from_city = created_cities[from_city_name]
                to_city = created_cities[to_city_name]
                
                # Create bidirectional connection
                connection, created = RoadConnection.objects.get_or_create(
                    from_city=from_city,
                    to_city=to_city,
                    defaults={
                        'distance_km': distance,
                        'road_type': road_type,
                        'is_bidirectional': True
                    }
                )
                
                if created:
                    self.stdout.write(f"Created road: {from_city.name} → {to_city.name} ({distance}km)")

        self.stdout.write(
            self.style.SUCCESS('Successfully populated Nigerian cities and road connections!')
        )
