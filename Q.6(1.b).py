"""
Task 6 - Problem 1(b): Breadth-First Search (BFS) Algorithm
Finding path from Glogow (Start - Blue) to Płock (Goal - Red)
Using Open and Closed containers to explain the algorithm.
"""

from collections import deque



# Adjacency list representation of the Poland cities map
# Format: City -> [(neighbor, distance), ...]

state_space = {
    'Glogow': [('Leszno', 45), ('Wroclaw', 140)],
    'Leszno': [('Glogow', 45), ('Poznan', 90), ('Kalisz', 140), ('Wroclaw', 100)],
    'Poznan': [('Leszno', 90), ('Bydgoszcz', 140), ('Kalisz', 130)],
    'Bydgoszcz': [('Poznan', 140), ('Wloclawek', 110)],
    'Wloclawek': [('Bydgoszcz', 110), ('Konin', 120), ('Plock', 55)],
    'Plock': [('Wloclawek', 55), ('Warsaw', 130)],
    'Warsaw': [('Plock', 130), ('Lodz', 150), ('Radom', 105)],
    'Konin': [('Wloclawek', 120), ('Kalisz', 120), ('Lodz', 120)],
    'Kalisz': [('Leszno', 140), ('Poznan', 130), ('Konin', 120), ('Czestochowa', 160), ('Lodz', 120)],
    'Lodz': [('Konin', 120), ('Kalisz', 120), ('Warsaw', 150), ('Czestochowa', 128), ('Radom', 165)],
    'Czestochowa': [('Kalisz', 160), ('Lodz', 128), ('Katowice', 80), ('Opole', 118)],
    'Katowice': [('Czestochowa', 80), ('Krakow', 85)],
    'Krakow': [('Katowice', 85), ('Kielce', 120)],
    'Kielce': [('Krakow', 120), ('Radom', 82)],
    'Radom': [('Kielce', 82), ('Warsaw', 105), ('Lodz', 165)],
    'Wroclaw': [('Glogow', 140), ('Leszno', 100), ('Opole', 100)],
    'Opole': [('Wroclaw', 100), ('Czestochowa', 118)]
}

# Start and Goal cities
START = 'Glogow'  # Blue node
GOAL = 'Plock'    # Red node

print("=" * 70)
print("STATE SPACE - Graph Representation of Poland Cities Map")
print("=" * 70)
print(f"\nStart City (Blue): {START}")
print(f"Goal City (Red): {GOAL}")
print(f"\nTotal Cities: {len(state_space)}")
print("\nAdjacency List:")
print("-" * 50)
for city, neighbors in state_space.items():
    neighbor_str = ", ".join([f"{n}({d})" for n, d in neighbors])
    print(f"  {city}: {neighbor_str}")

# BREADTH-FIRST SEARCH (BFS) ALGORITHM

def bfs_with_containers(graph, start, goal):
    """
    Breadth-First Search using Open and Closed containers.
    
    OPEN: Queue containing nodes to be explored (FIFO - First In First Out)
    CLOSED: Set containing nodes already explored
    
    Key Difference from DFS:
    - DFS uses Stack (LIFO) - explores deepest nodes first
    - BFS uses Queue (FIFO) - explores shallowest nodes first (level by level)
    
    Args:
        graph: Dictionary representing the state space
        start: Starting city (Glogow)
        goal: Goal city (Plock)
    
    Returns:
        path: List of cities from start to goal (shortest path by number of edges)
    """
    
    print("\n" + "=" * 70)
    print("BFS ALGORITHM EXECUTION WITH OPEN AND CLOSED CONTAINERS")
    print("=" * 70)
    print("\nNote: BFS uses QUEUE (FIFO) - First In First Out")
    print("      Nodes are added at the BACK and removed from the FRONT")
    
    # Initialize containers
    # OPEN: Queue of (current_node, path_so_far) using deque for efficient FIFO
    open_container = deque([(start, [start])])
    
    # CLOSED: Set of visited nodes
    closed_container = set()
    
    step = 0
    
    print(f"\nInitial State:")
    print(f"  OPEN (Queue):  [{start}]  <- FRONT ... BACK")
    print(f"  CLOSED:        []")
    print("-" * 70)
    
    while open_container:
        step += 1
        
        # Dequeue from OPEN (Queue - FIFO: take from the front)
        current_node, path = open_container.popleft()
        
        print(f"\nStep {step}:")
        print(f"  Dequeue from FRONT: {current_node}")
        print(f"  Current Path: {' -> '.join(path)}")
        print(f"  Current Level (depth): {len(path) - 1}")
        
        # Check if goal is reached
        if current_node == goal:
            print(f"\n  *** GOAL REACHED! ***")
            open_nodes = [n for n, p in open_container]
            print(f"\n  Final OPEN:   {open_nodes}")
            print(f"  Final CLOSED: {sorted(closed_container)}")
            return path
        
        # Skip if already visited
        if current_node in closed_container:
            print(f"  Status: Already in CLOSED, skipping...")
            continue
        
        # Add current node to CLOSED
        closed_container.add(current_node)
        
        # Get neighbors (children) not in CLOSED
        neighbors = graph.get(current_node, [])
        children = [(neighbor, dist) for neighbor, dist in neighbors 
                    if neighbor not in closed_container]
        
        # Add children to OPEN (enqueue at the back)
        for neighbor, distance in children:
            # Also check if neighbor is already in OPEN to avoid duplicates
            open_nodes = [n for n, p in open_container]
            if neighbor not in open_nodes:
                new_path = path + [neighbor]
                open_container.append((neighbor, new_path))  # Add to BACK
        
        # Display container states
        open_nodes = [n for n, p in open_container]
        print(f"  Children added to BACK: {[n for n, d in children if n not in closed_container]}")
        print(f"  OPEN (Queue):  {open_nodes}  <- FRONT ... BACK")
        print(f"  CLOSED:        {sorted(closed_container)}")
    
    print("\n  No path found!")
    return None


# EXECUTE BFS AND DISPLAY RESULTS

# Run BFS
print("\n")
path = bfs_with_containers(state_space, START, GOAL)

# Display final result
print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

if path:
    print(f"\nPath found from {START} to {GOAL}:")
    print(f"  {' -> '.join(path)}")
    print(f"\nNumber of cities in path: {len(path)}")
    print(f"Number of edges (hops): {len(path) - 1}")
    
    # Calculate total distance
    total_distance = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        for neighbor, dist in state_space[current]:
            if neighbor == next_city:
                total_distance += dist
                break
    
    print(f"Total distance: {total_distance} km")
    
    # Show path with distances
    print(f"\nDetailed Path:")
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        for neighbor, dist in state_space[current]:
            if neighbor == next_city:
                print(f"  {current} --({dist} km)--> {next_city}")
                break
else:
    print(f"\nNo path exists from {START} to {GOAL}")
    
    
# PART 4: COMPARISON WITH DFS
print("\n" + "=" * 70)
print("BFS vs DFS COMPARISON")
print("=" * 70)
print("""
+------------------+--------------------------------+--------------------------------+
|    Property      |            BFS                 |            DFS                 |
+------------------+--------------------------------+--------------------------------+
| Data Structure   | Queue (FIFO)                   | Stack (LIFO)                   |
| Exploration      | Level by level (breadth)       | Deep first (depth)             |
| Path Found       | Shortest path (by edges)       | Not necessarily shortest       |
| Memory Usage     | Higher (stores all level nodes)| Lower (stores path only)       |
| Completeness     | Complete (finds solution)      | Complete (if no infinite paths)|
+------------------+--------------------------------+--------------------------------+
""")

print("=" * 70)
