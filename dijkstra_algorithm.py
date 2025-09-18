"""
Dijkstra's Algorithm Implementation for Nigerian City Distance Calculator
=======================================================================

This file contains a detailed implementation of Dijkstra's algorithm
with comprehensive comments explaining each step of the process.

Author: Group Project - Backend Implementation
Purpose: Find shortest path between Nigerian cities using graph theory
"""

import json
from typing import Dict, List, Tuple, Optional, Set


def dijkstra_algorithm(cities: Dict, roads: Dict, start: str, end: str) -> Tuple[Optional[int], Optional[List[str]]]:
    """
    Dijkstra's Algorithm Implementation for Shortest Path Finding
    
    This algorithm finds the shortest path between two cities in a weighted graph.
    It guarantees the optimal solution by always choosing the shortest path to
    unvisited cities.
    
    Args:
        cities: Dictionary of cities with their coordinates
        roads: Dictionary of road connections with distances
        start: Starting city name
        end: Destination city name
    
    Returns:
        Tuple of (total_distance, path_list) or (None, None) if no path exists
    """
    
    # STEP 1: VALIDATION - Check if start and end cities exist
    if start not in cities or end not in cities:
        print(f"❌ Error: City not found in the network")
        return None, None
    
    # If start and end are the same city
    if start == end:
        print(f"✅ Same city: {start} -> {end} (distance: 0)")
        return 0, [start]
    
    print(f"🚀 Starting Dijkstra's Algorithm: {start} -> {end}")
    print("=" * 50)
    
    # STEP 2: INITIALIZATION - Set up data structures
    print("📊 STEP 2: Initializing data structures...")
    
    # distances: Keep track of shortest distance to each city
    # Initially set all distances to infinity (∞)
    distances = {city: float('inf') for city in cities.keys()}
    
    # previous: Keep track of the previous city in the shortest path
    # This helps us reconstruct the path later
    previous = {city: None for city in cities.keys()}
    
    # Set distance to starting city as 0 (we're already there)
    distances[start] = 0
    
    # unvisited: Set of cities we haven't processed yet
    unvisited = set(cities.keys())
    
    print(f"   • Total cities in network: {len(cities)}")
    print(f"   • Starting distance: {distances[start]}")
    print(f"   • Unvisited cities: {len(unvisited)}")
    print()
    
    # STEP 3: MAIN ALGORITHM LOOP - Process each city
    print("🔄 STEP 3: Main algorithm loop...")
    iteration = 0
    
    while unvisited:
        iteration += 1
        print(f"   📍 Iteration {iteration}:")
        
        # STEP 3A: FIND CLOSEST UNVISITED CITY
        # This is the core of Dijkstra's algorithm - always choose the city
        # with the smallest known distance that we haven't visited yet
        current = min(unvisited, key=lambda city: distances[city])
        current_distance = distances[current]
        
        print(f"      • Current city: {current} (distance: {current_distance})")
        
        # STEP 3B: CHECK IF WE'VE REACHED THE DESTINATION
        # If we've found the shortest path to our destination, we can stop
        if current == end:
            print(f"      ✅ Destination reached: {end}")
            break
        
        # STEP 3C: MARK CURRENT CITY AS VISITED
        # Remove it from unvisited set so we don't process it again
        unvisited.remove(current)
        print(f"      • Marked {current} as visited")
        print(f"      • Remaining unvisited: {len(unvisited)}")
        
        # STEP 3D: EXPLORE NEIGHBORS - Check all roads from current city
        print(f"      🔍 Exploring roads from {current}:")
        neighbors_found = 0
        
        for (city1, city2), road_distance in roads.items():
            # Check if this road connects to our current city
            if city1 == current and city2 in unvisited:
                # Found a road from current city to an unvisited city
                neighbors_found += 1
                neighbor = city2
                
                # Calculate alternative distance: current distance + road distance
                alternative_distance = current_distance + road_distance
                current_neighbor_distance = distances[neighbor]
                
                print(f"         • Road: {current} -> {neighbor} (distance: {road_distance})")
                print(f"           - Current distance to {neighbor}: {current_neighbor_distance}")
                print(f"           - Alternative distance: {alternative_distance}")
                
                # STEP 3E: UPDATE DISTANCE IF WE FOUND A SHORTER PATH
                if alternative_distance < current_neighbor_distance:
                    distances[neighbor] = alternative_distance
                    previous[neighbor] = current
                    print(f"           ✅ Updated! New distance to {neighbor}: {alternative_distance}")
                else:
                    print(f"           ❌ No improvement (current path is shorter)")
                    
            elif city2 == current and city1 in unvisited:
                # Found a road from an unvisited city to current city
                # (roads are bidirectional, so we check both directions)
                neighbors_found += 1
                neighbor = city1
                
                alternative_distance = current_distance + road_distance
                current_neighbor_distance = distances[neighbor]
                
                print(f"         • Road: {neighbor} -> {current} (distance: {road_distance})")
                print(f"           - Current distance to {neighbor}: {current_neighbor_distance}")
                print(f"           - Alternative distance: {alternative_distance}")
                
                if alternative_distance < current_neighbor_distance:
                    distances[neighbor] = alternative_distance
                    previous[neighbor] = current
                    print(f"           ✅ Updated! New distance to {neighbor}: {alternative_distance}")
                else:
                    print(f"           ❌ No improvement (current path is shorter)")
        
        if neighbors_found == 0:
            print(f"         • No unvisited neighbors found from {current}")
        
        print()
    
    # STEP 4: CHECK IF PATH EXISTS
    print("🔍 STEP 4: Checking if path exists...")
    final_distance = distances[end]
    
    if final_distance == float('inf'):
        print(f"❌ No path found from {start} to {end}")
        print("   This could happen if cities are in disconnected parts of the network")
        return None, None
    
    print(f"✅ Path exists! Total distance: {final_distance} km")
    
    # STEP 5: RECONSTRUCT THE PATH
    print("🛤️  STEP 5: Reconstructing the shortest path...")
    
    # Start from the destination and work backwards using the 'previous' dictionary
    path = []
    current = end
    
    print(f"   • Starting from destination: {end}")
    
    while current is not None:
        path.append(current)
        current = previous[current]
        if current is not None:
            print(f"   • Previous city: {current}")
    
    # Reverse the path since we built it backwards
    path.reverse()
    
    print(f"   • Final path: {' -> '.join(path)}")
    print(f"   • Total cities in path: {len(path)}")
    print(f"   • Total distance: {final_distance} km")
    
    # STEP 6: ALGORITHM COMPLETION
    print("=" * 50)
    print("🎉 Dijkstra's Algorithm completed successfully!")
    print(f"📊 Results:")
    print(f"   • Start: {start}")
    print(f"   • End: {end}")
    print(f"   • Distance: {final_distance} km")
    print(f"   • Path: {' -> '.join(path)}")
    print(f"   • Cities visited: {len(path)}")
    
    return final_distance, path


def demonstrate_algorithm():
    """
    Demonstration function showing how Dijkstra's algorithm works
    with a simple example using Nigerian cities.
    """
    print("🇳🇬 DIJKSTRA'S ALGORITHM DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Sample cities data (simplified for demonstration)
    sample_cities = {
        "Lagos": {"lat": 6.5244, "lng": 3.3792},
        "Ibadan": {"lat": 7.3776, "lng": 3.9470},
        "Abuja": {"lat": 9.0765, "lng": 7.3986},
        "Kano": {"lat": 12.0022, "lng": 8.5920}
    }
    
    # Sample roads data (simplified for demonstration)
    sample_roads = {
        ("Lagos", "Ibadan"): 150,
        ("Ibadan", "Abuja"): 400,
        ("Abuja", "Kano"): 300,
        ("Lagos", "Abuja"): 500  # Direct route (longer)
    }
    
    print("🗺️  Sample Network:")
    print("   Cities:", list(sample_cities.keys()))
    print("   Roads:")
    for (city1, city2), distance in sample_roads.items():
        print(f"      {city1} <-> {city2}: {distance} km")
    print()
    
    # Test the algorithm
    start_city = "Lagos"
    end_city = "Kano"
    
    print(f"🎯 Finding shortest path: {start_city} -> {end_city}")
    print()
    
    distance, path = dijkstra_algorithm(sample_cities, sample_roads, start_city, end_city)
    
    if distance is not None:
        print()
        print("🏆 ALGORITHM SUCCESS!")
        print(f"   Shortest path: {' -> '.join(path)}")
        print(f"   Total distance: {distance} km")
    else:
        print("❌ No path found")


def explain_algorithm_concepts():
    """
    Educational function explaining the key concepts of Dijkstra's algorithm.
    """
    print("📚 DIJKSTRA'S ALGORITHM - KEY CONCEPTS")
    print("=" * 50)
    print()
    
    print("🎯 PURPOSE:")
    print("   Dijkstra's algorithm finds the shortest path between two nodes")
    print("   in a weighted graph. It's used in navigation, networking,")
    print("   and optimization problems.")
    print()
    
    print("🔑 KEY PRINCIPLES:")
    print("   1. GREEDY APPROACH: Always choose the closest unvisited node")
    print("   2. OPTIMAL SUBSTRUCTURE: Shortest path contains shortest subpaths")
    print("   3. NO NEGATIVE WEIGHTS: Algorithm assumes non-negative edge weights")
    print("   4. GUARANTEED OPTIMAL: Always finds the truly shortest path")
    print()
    
    print("⚡ TIME COMPLEXITY:")
    print("   • With binary heap: O((V + E) log V)")
    print("   • With simple array: O(V²)")
    print("   • Where V = vertices (cities), E = edges (roads)")
    print()
    
    print("💡 WHY IT WORKS:")
    print("   The algorithm maintains the invariant that for each visited node,")
    print("   the shortest path from the start has been found. This is proven")
    print("   by mathematical induction and the greedy choice property.")
    print()
    
    print("🌍 REAL-WORLD APPLICATIONS:")
    print("   • GPS navigation systems")
    print("   • Network routing protocols")
    print("   • Social network analysis")
    print("   • Game AI pathfinding")
    print("   • Logistics optimization")


if __name__ == "__main__":
    """
    Main execution block - run this file to see Dijkstra's algorithm in action
    """
    print("🚀 RUNNING DIJKSTRA'S ALGORITHM DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Show algorithm concepts
    explain_algorithm_concepts()
    print()
    
    # Demonstrate with sample data
    demonstrate_algorithm()
    print()
    
    print("🎓 This implementation is used in the Nigerian City Distance Calculator API")
    print("   to find optimal routes between any two cities in Nigeria.")
    print()
    print("🔗 Live API: https://csc-320-backend-putgsrlkc-jackthecoder17s-projects.vercel.app")
    print("📖 Documentation: https://csc-320-backend-putgsrlkc-jackthecoder17s-projects.vercel.app/docs")
