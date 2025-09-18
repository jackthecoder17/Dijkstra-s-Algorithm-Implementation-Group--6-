"""
Dijkstra's Algorithm - General Pseudocode
=========================================

Clean, general pseudocode for Dijkstra's algorithm
that can be shown in implementation presentations.

Author: Group Project - Backend Implementation
"""

import heapq
import sys

def dijkstra(V, edges, src):
    """
    Returns shortest distances from src to all other vertices
    
    Args:
        V: Number of vertices
        edges: List of edges [u, v, weight]
        src: Source vertex
    
    Returns:
        List of shortest distances from src to all vertices
    """
    # Create adjacency list
    adj = constructAdj(edges, V)

    # Create a priority queue to store vertices that
    # are being preprocessed.
    pq = []
    
    # Create a list for distances and initialize all
    # distances as infinite
    dist = [sys.maxsize] * V

    # Insert source itself in priority queue and initialize
    # its distance as 0.
    heapq.heappush(pq, [0, src])
    dist[src] = 0

    # Looping till priority queue becomes empty (or all
    # distances are not finalized) 
    while pq:
        # The first vertex in pair is the minimum distance
        # vertex, extract it from priority queue.
        u = heapq.heappop(pq)[1]

        # Get all adjacent of u.
        for x in adj[u]:
            # Get vertex label and weight of current
            # adjacent of u.
            v, weight = x[0], x[1]

            # If there is shorter path to v through u.
            if dist[v] > dist[u] + weight:
                # Updating distance of v
                dist[v] = dist[u] + weight
                heapq.heappush(pq, [dist[v], v])

    # Return the shortest distance array
    return dist


def constructAdj(edges, V):
    """
    Construct adjacency list from edge list
    
    Args:
        edges: List of edges [u, v, weight]
        V: Number of vertices
    
    Returns:
        Adjacency list
    """
    adj = [[] for _ in range(V)]
    
    for edge in edges:
        u, v, weight = edge
        adj[u].append([v, weight])
        # For undirected graph, add both directions
        adj[v].append([u, weight])
    
    return adj


def dijkstra_single_target(V, edges, src, target):
    """
    Returns shortest distance from src to target vertex
    
    Args:
        V: Number of vertices
        edges: List of edges [u, v, weight]
        src: Source vertex
        target: Target vertex
    
    Returns:
        Shortest distance from src to target
    """
    # Create adjacency list
    adj = constructAdj(edges, V)

    # Create a priority queue
    pq = []
    
    # Create a list for distances and initialize all
    # distances as infinite
    dist = [sys.maxsize] * V

    # Insert source itself in priority queue and initialize
    # its distance as 0.
    heapq.heappush(pq, [0, src])
    dist[src] = 0

    # Looping till priority queue becomes empty
    while pq:
        # Extract minimum distance vertex
        u = heapq.heappop(pq)[1]

        # If we reached target, we can stop early
        if u == target:
            break

        # Get all adjacent of u.
        for x in adj[u]:
            v, weight = x[0], x[1]

            # If there is shorter path to v through u.
            if dist[v] > dist[u] + weight:
                # Updating distance of v
                dist[v] = dist[u] + weight
                heapq.heappush(pq, [dist[v], v])

    # Return the shortest distance to target
    return dist[target] if dist[target] != sys.maxsize else -1


def dijkstra_with_path(V, edges, src, target):
    """
    Returns shortest distance and path from src to target
    
    Args:
        V: Number of vertices
        edges: List of edges [u, v, weight]
        src: Source vertex
        target: Target vertex
    
    Returns:
        Tuple of (distance, path) or (-1, []) if no path
    """
    # Create adjacency list
    adj = constructAdj(edges, V)

    # Create a priority queue
    pq = []
    
    # Create a list for distances and initialize all
    # distances as infinite
    dist = [sys.maxsize] * V
    
    # Create a list for previous vertices to reconstruct path
    prev = [-1] * V

    # Insert source itself in priority queue and initialize
    # its distance as 0.
    heapq.heappush(pq, [0, src])
    dist[src] = 0

    # Looping till priority queue becomes empty
    while pq:
        # Extract minimum distance vertex
        u = heapq.heappop(pq)[1]

        # If we reached target, we can stop early
        if u == target:
            break

        # Get all adjacent of u.
        for x in adj[u]:
            v, weight = x[0], x[1]

            # If there is shorter path to v through u.
            if dist[v] > dist[u] + weight:
                # Updating distance of v
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, [dist[v], v])

    # Reconstruct path
    if dist[target] == sys.maxsize:
        return -1, []
    
    path = []
    current = target
    while current != -1:
        path.append(current)
        current = prev[current]
    path.reverse()
    
    return dist[target], path


# Driver Code Starts

def test_dijkstra():
    """
    Test the Dijkstra's algorithm implementation
    """
    print("🧮 DIJKSTRA'S ALGORITHM - GENERAL IMPLEMENTATION")
    print("=" * 60)
    print()
    
    # Test case 1: Basic graph
    print("📊 Test Case 1: Basic Graph")
    V = 5
    src = 0
    edges = [[0, 1, 4], [0, 2, 8], [1, 4, 6], [2, 3, 2], [3, 4, 10]]
    
    print(f"   Vertices: {V}")
    print(f"   Source: {src}")
    print(f"   Edges: {edges}")
    
    result = dijkstra(V, edges, src)
    print(f"   Shortest distances: {result}")
    print()
    
    # Test case 2: Single target
    print("📊 Test Case 2: Single Target")
    target = 4
    distance = dijkstra_single_target(V, edges, src, target)
    print(f"   Distance from {src} to {target}: {distance}")
    print()
    
    # Test case 3: With path
    print("📊 Test Case 3: With Path")
    distance, path = dijkstra_with_path(V, edges, src, target)
    print(f"   Distance: {distance}")
    print(f"   Path: {path}")
    print()
    
    # Test case 4: Nigerian cities example
    print("📊 Test Case 4: Nigerian Cities Example")
    cities = ["Lagos", "Ibadan", "Abuja", "Kano"]
    city_edges = [
        [0, 1, 150],  # Lagos -> Ibadan
        [1, 2, 400],  # Ibadan -> Abuja
        [2, 3, 400],  # Abuja -> Kano
        [0, 2, 500]   # Lagos -> Abuja (direct)
    ]
    
    print(f"   Cities: {cities}")
    print(f"   Edges: {city_edges}")
    
    # Lagos (0) to Kano (3)
    distance, path = dijkstra_with_path(4, city_edges, 0, 3)
    print(f"   Distance from Lagos to Kano: {distance}")
    print(f"   Path: {[cities[i] for i in path]}")
    print()


if __name__ == "__main__":
    """
    Main execution - test the algorithm
    """
    test_dijkstra()
    
    print("🎓 This is the general pseudocode for Dijkstra's algorithm")
    print("   that can be used in any graph-based shortest path problem!")
    print()
    print("🔗 Live API: https://csc-320-backend-putgsrlkc-jackthecoder17s-projects.vercel.app")
    print("📖 Documentation: https://csc-320-backend-putgsrlkc-jackthecoder17s-projects.vercel.app/docs")
