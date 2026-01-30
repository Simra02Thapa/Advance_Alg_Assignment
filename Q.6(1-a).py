<<<<<<< HEAD
# Task 6.1: Building the State Space from Map (a)
# The Adjacency List represents the actual road distances (g-costs)

poland_map = {
    'Glogow': {'Leszno': 45, 'Zielona_Gora': 40}, # Starting Node
    'Zielona_Gora': {'Glogow': 40, 'Poznan': 90},
    'Leszno': {'Glogow': 45, 'Poznan': 140, 'Wroclaw': 100, 'Kalisz': 140},
    'Wroclaw': {'Leszno': 100, 'Opole': 100, 'Czestochowa': 118},
    'Opole': {'Wroclaw': 100, 'Katowice': 85},
    'Katowice': {'Opole': 85, 'Krakow': 85, 'Czestochowa': 80},
    'Krakow': {'Katowice': 85, 'Kielce': 120},
    'Kielce': {'Krakow': 120, 'Radom': 82, 'Lodz': 280},
    'Radom': {'Kielce': 82, 'Warsaw': 105},
    'Warsaw': {'Radom': 105, 'Lodz': 150, 'Plock': 130},
    'Plock': {'Warsaw': 130, 'Wloclawek': 55, 'Lodz': 165}, # Goal Node
    'Wloclawek': {'Plock': 55, 'Bydgoszcz': 110, 'Konin': 120},
    'Bydgoszcz': {'Wloclawek': 110, 'Poznan': 140},
    'Poznan': {'Bydgoszcz': 140, 'Zielona_Gora': 90, 'Leszno': 140, 'Konin': 120},
    'Konin': {'Poznan': 120, 'Wloclawek': 120, 'Kalisz': 160, 'Lodz': 120},
    'Kalisz': {'Konin': 160, 'Leszno': 140, 'Lodz': 128},
    'Lodz': {'Kalisz': 128, 'Konin': 120, 'Wloclawek': 165, 'Plock': 165, 'Warsaw': 150, 'Kielce': 280, 'Czestochowa': 128},
    'Czestochowa': {'Lodz': 128, 'Wroclaw': 118, 'Katowice': 80}
}

# Example of accessing the state space:
print(f"Connections from Glogow: {poland_map['Glogow']}")



# Q(6.a) (DFS Implementation) 

def solve_dfs(graph, start, goal):
    # Open is the Stack (LIFO), Closed is the Visited set
    open_container = [start]
    closed_container = []
    parent = {start: None}

    print(f"{'Step':<5} | {'Current Node':<15} | {'Open Container (Stack)':<45} | {'Closed Container':<30}")
    print("-" * 95)
    
    step = 1
    while open_container:
        # LIFO: Pop the last element added
        current = open_container.pop()
        
        if current in closed_container:
            continue
        
        open_str = str(open_container)
        closed_str = str(closed_container)
        
        print(f"{step:<5} | {current:<15} | {open_str:<45} | {closed_str:<30}")
        
        if current == goal:
            print("\nGoal Reached!")
            return reconstruct_path(parent, goal)
        
        closed_container.append(current)
        
        for neighbor in graph[current]:
            if neighbor not in closed_container:
                open_container.append(neighbor)
                parent[neighbor] = current
        
        step += 1

def reconstruct_path(parent, goal):
    path = []
    while goal:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]

# Execution
print("\n" + "█"*130)
print("DEPTH-FIRST SEARCH (DFS) ALGORITHM - POLAND PARCEL DELIVERY")
print("█"*130)
print(f"START NODE: Glogow (Blue) | GOAL NODE: Plock (Red)")
print("█"*130)

path = solve_dfs(poland_map, 'Glogow', 'Plock')
print(f"DFS Path Found: {' -> '.join(path)}")
=======
"""
Task 6 - Problem 1(a): Depth-First Search (DFS) Algorithm
Finding path from Glogow (Start - Blue) to Płock (Goal - Red)
Using Open and Closed containers to explain the algorithm.
"""


# STATE SPACE (Graph Representation)

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


# DEPTH-FIRST SEARCH (DFS) ALGORITHM

def dfs_with_containers(graph, start, goal):
    """
    Depth-First Search using Open and Closed containers.
    
    OPEN: Stack containing nodes to be explored (LIFO - Last In First Out)
    CLOSED: Set containing nodes already explored
    
    Args:
        graph: Dictionary representing the state space
        start: Starting city (Glogow)
        goal: Goal city (Plock)
    
    Returns:
        path: List of cities from start to goal
    """
    
    print("\n" + "=" * 70)
    print("DFS ALGORITHM EXECUTION WITH OPEN AND CLOSED CONTAINERS")
    print("=" * 70)
    
    # Initialize containers
    # OPEN: Stack of (current_node, path_so_far)
    open_container = [(start, [start])]
    
    # CLOSED: Set of visited nodes
    closed_container = set()
    
    step = 0
    
    print(f"\nInitial State:")
    print(f"  OPEN:   [{start}]")
    print(f"  CLOSED: []")
    print("-" * 70)
    
    while open_container:
        step += 1
        
        # Pop from OPEN (Stack - LIFO: take from the end)
        current_node, path = open_container.pop()
        
        print(f"\nStep {step}:")
        print(f"  Current Node: {current_node}")
        print(f"  Current Path: {' -> '.join(path)}")
        
        # Check if goal is reached
        if current_node == goal:
            print(f"\n  *** GOAL REACHED! ***")
            print(f"\n  Final OPEN:   {[n for n, p in open_container]}")
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
        
        # Add children to OPEN (in reverse order so first neighbor is processed first)
        for neighbor, distance in reversed(children):
            new_path = path + [neighbor]
            open_container.append((neighbor, new_path))
        
        # Display container states
        open_nodes = [n for n, p in open_container]
        print(f"  Children added: {[n for n, d in children]}")
        print(f"  OPEN:   {open_nodes}")
        print(f"  CLOSED: {sorted(closed_container)}")
    
    print("\n  No path found!")
    return None
# PART 3: EXECUTE DFS AND DISPLAY RESULTS

# Run DFS
print("\n")
path = dfs_with_containers(state_space, START, GOAL)

# Display final result
print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

if path:
    print(f"\nPath found from {START} to {GOAL}:")
    print(f"  {' -> '.join(path)}")
    print(f"\nNumber of cities in path: {len(path)}")
    
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

print("\n" + "=" * 70)
>>>>>>> 576c714 (Q.)
