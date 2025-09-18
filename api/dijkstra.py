"""
Dijkstra's Algorithm implementation for finding shortest paths between Nigerian cities.
"""
import heapq
from typing import Dict, List, Tuple, Optional
from cities.models import City, RoadConnection


class DijkstraGraph:
    """Graph representation for Dijkstra's algorithm."""
    
    def __init__(self):
        self.graph = {}
        self._build_graph()
    
    def _build_graph(self):
        """Build the graph from database connections."""
        # Initialize all cities
        cities = City.objects.all()
        for city in cities:
            self.graph[city.id] = []
        
        # Add connections
        connections = RoadConnection.objects.select_related('from_city', 'to_city').all()
        for connection in connections:
            from_id = connection.from_city.id
            to_id = connection.to_city.id
            distance = float(connection.distance_km)
            
            # Add forward connection
            self.graph[from_id].append((to_id, distance))
            
            # Add backward connection if bidirectional
            if connection.is_bidirectional:
                self.graph[to_id].append((from_id, distance))
    
    def dijkstra(self, start_city_id: int, end_city_id: int) -> Tuple[float, List[int]]:
        """
        Find shortest path between two cities using Dijkstra's algorithm.
        
        Args:
            start_city_id: ID of the starting city
            end_city_id: ID of the destination city
            
        Returns:
            Tuple of (total_distance, path_city_ids)
        """
        if start_city_id not in self.graph or end_city_id not in self.graph:
            raise ValueError("Invalid city IDs")
        
        if start_city_id == end_city_id:
            return 0.0, [start_city_id]
        
        # Initialize distances and previous nodes
        distances = {city_id: float('inf') for city_id in self.graph}
        previous = {city_id: None for city_id in self.graph}
        distances[start_city_id] = 0
        
        # Priority queue: (distance, city_id)
        pq = [(0, start_city_id)]
        visited = set()
        
        while pq:
            current_distance, current_city = heapq.heappop(pq)
            
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # If we reached the destination, we can stop
            if current_city == end_city_id:
                break
            
            # Check all neighbors
            for neighbor_id, edge_distance in self.graph[current_city]:
                if neighbor_id in visited:
                    continue
                
                new_distance = current_distance + edge_distance
                
                if new_distance < distances[neighbor_id]:
                    distances[neighbor_id] = new_distance
                    previous[neighbor_id] = current_city
                    heapq.heappush(pq, (new_distance, neighbor_id))
        
        # Reconstruct path
        if distances[end_city_id] == float('inf'):
            return float('inf'), []  # No path found
        
        path = []
        current = end_city_id
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return distances[end_city_id], path
    
    def get_city_details(self, city_ids: List[int]) -> List[Dict]:
        """Get city details for a list of city IDs."""
        cities = City.objects.filter(id__in=city_ids)
        city_dict = {city.id: city for city in cities}
        
        return [
            {
                'id': city_id,
                'name': city_dict[city_id].name,
                'state': city_dict[city_id].state,
                'latitude': float(city_dict[city_id].latitude),
                'longitude': float(city_dict[city_id].longitude),
            }
            for city_id in city_ids
        ]


def calculate_shortest_route(from_city_name: str, to_city_name: str) -> Dict:
    """
    Calculate shortest route between two cities.
    
    Args:
        from_city_name: Name of the starting city
        to_city_name: Name of the destination city
        
    Returns:
        Dictionary containing route information
    """
    try:
        # Get city objects
        from_city = City.objects.get(name__iexact=from_city_name)
        to_city = City.objects.get(name__iexact=to_city_name)
        
        # Create graph and find shortest path
        graph = DijkstraGraph()
        total_distance, path_city_ids = graph.dijkstra(from_city.id, to_city.id)
        
        if total_distance == float('inf'):
            return {
                'success': False,
                'error': 'No route found between the specified cities',
                'total_distance': None,
                'path': [],
                'cities': []
            }
        
        # Get city details for the path
        path_cities = graph.get_city_details(path_city_ids)
        
        return {
            'success': True,
            'total_distance': round(total_distance, 2),
            'path': path_city_ids,
            'cities': path_cities,
            'from_city': {
                'id': from_city.id,
                'name': from_city.name,
                'state': from_city.state,
                'latitude': float(from_city.latitude),
                'longitude': float(from_city.longitude),
            },
            'to_city': {
                'id': to_city.id,
                'name': to_city.name,
                'state': to_city.state,
                'latitude': float(to_city.latitude),
                'longitude': float(to_city.longitude),
            }
        }
        
    except City.DoesNotExist as e:
        city_name = str(e).split("'")[1] if "'" in str(e) else "Unknown"
        return {
            'success': False,
            'error': f'City "{city_name}" not found in database',
            'total_distance': None,
            'path': [],
            'cities': []
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'An error occurred: {str(e)}',
            'total_distance': None,
            'path': [],
            'cities': []
        }
