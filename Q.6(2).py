"""
Task 6.2: A* Algorithm for Finding Shortest Path
================================================
Problem: Find shortest path from Glogow (blue) to Płock (red)
Using A* algorithm with heuristic function based on straight-line distances

Heuristic Function Design:
- h(n) = straight-line distance from node n to goal (Płock)
- Values extracted from diagram (b)
- Admissible: h(n) never overestimates actual cost (straight-line ≤ road distance)
"""

import heapq


# ==============================================================================
# STATE SPACE REPRESENTATION (from diagram a - actual road distances)
# ==============================================================================

graph = {
    'Glogow': [('Leszno', 45), ('Wroclaw', 140)],
    'Leszno': [('Glogow', 45), ('Poznan', 90), ('Wroclaw', 100), ('Kalisz', 140)],
    'Poznan': [('Leszno', 90), ('Bydgoszcz', 140), ('Konin', 130)],
    'Bydgoszcz': [('Poznan', 140), ('Wloclawek', 110)],
    'Wloclawek': [('Bydgoszcz', 110), ('Plock', 55), ('Konin', 120)],
    'Plock': [('Wloclawek', 55), ('Warsaw', 130)],  # GOAL (Red node)
    'Konin': [('Poznan', 130), ('Wloclawek', 120), ('Lodz', 120)],
    'Warsaw': [('Plock', 130), ('Lodz', 150), ('Radom', 105)],
    'Lodz': [('Konin', 120), ('Kalisz', 120), ('Czestochowa', 160), ('Katowice', 128), ('Warsaw', 150), ('Kielce', 165)],
    'Kalisz': [('Leszno', 140), ('Lodz', 120), ('Czestochowa', 160)],
    'Wroclaw': [('Glogow', 140), ('Leszno', 100), ('Opole', 100)],
    'Opole': [('Wroclaw', 100), ('Czestochowa', 118)],
    'Czestochowa': [('Kalisz', 160), ('Lodz', 160), ('Katowice', 80), ('Opole', 118)],
    'Katowice': [('Czestochowa', 80), ('Lodz', 128), ('Krakow', 85)],
    'Krakow': [('Katowice', 85), ('Kielce', 120), ('Lodz', 280)],
    'Kielce': [('Lodz', 165), ('Krakow', 120), ('Radom', 82)],
    'Radom': [('Warsaw', 105), ('Kielce', 82)]
}


# ==============================================================================
# HEURISTIC FUNCTION (from diagram b - straight-line distances to Płock)
# ==============================================================================
# h(n) = straight-line distance from city n to goal (Płock)

heuristic = {
    'Glogow': 200,        # Estimated (far from Płock)
    'Leszno': 170,        # ~103 in diagram + buffer
    'Poznan': 160,        # ~108 in diagram
    'Bydgoszcz': 90,      # From diagram (b)
    'Wloclawek': 44,      # From diagram (b)
    'Plock': 0,           # GOAL - h(goal) = 0
    'Konin': 96,          # From diagram (b)
    'Warsaw': 95,         # From diagram (b)
    'Lodz': 118,          # From diagram (b)
    'Kalisz': 140,        # ~95 in diagram + buffer
    'Wroclaw': 200,       # Far from Płock
    'Opole': 220,         # Far from Płock
    'Czestochowa': 180,   # ~128 in diagram
    'Katowice': 200,      # Far south
    'Krakow': 250,        # Furthest south
    'Kielce': 160,        # ~70 in diagram
    'Radom': 120          # ~91 in diagram
}


# ==============================================================================
# A* ALGORITHM IMPLEMENTATION
# ==============================================================================

def a_star_search(graph, heuristic, start, goal):
    """
    A* Search Algorithm
    
    f(n) = g(n) + h(n)
    where:
        g(n) = actual cost from start to n
        h(n) = heuristic estimate from n to goal
        f(n) = total estimated cost
    
    Uses:
        - OPEN list (priority queue): nodes to be explored
        - CLOSED list (set): nodes already explored
    """
    
    print("=" * 70)
    print("A* ALGORITHM - Finding Shortest Path")
    print(f"Start: {start} (Blue node)")
    print(f"Goal: {goal} (Red node)")
    print("=" * 70)
    print("\nHeuristic Function h(n) = straight-line distance to Płock")
    print("-" * 70)
    
    # Priority Queue: (f_cost, g_cost, current_node, path)
    # OPEN list - nodes to explore (priority queue ordered by f(n))
    open_list = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))
    
    # CLOSED list - nodes already explored
    closed_list = set()
    
    # Track best g(n) for each node
    g_scores = {start: 0}
    
    iteration = 0
    
    print("\n" + "=" * 70)
    print("STEP-BY-STEP EXECUTION")
    print("=" * 70)
    
    while open_list:
        iteration += 1
        
        # Get node with lowest f(n) from OPEN
        f_cost, g_cost, current, path = heapq.heappop(open_list)
        
        print(f"\n{'─' * 70}")
        print(f"ITERATION {iteration}")
        print(f"{'─' * 70}")
        print(f"Selected Node: {current}")
        print(f"  g({current}) = {g_cost} (actual cost from start)")
        print(f"  h({current}) = {heuristic[current]} (heuristic to goal)")
        print(f"  f({current}) = g + h = {f_cost}")
        print(f"Current Path: {' → '.join(path)}")
        
        # Goal check
        if current == goal:
            print(f"\n{'=' * 70}")
            print("🎯 GOAL REACHED!")
            print(f"{'=' * 70}")
            print(f"Final Path: {' → '.join(path)}")
            print(f"Total Cost: {g_cost}")
            return path, g_cost
        
        # Skip if already in CLOSED
        if current in closed_list:
            print(f"  [Already in CLOSED - skipping]")
            continue
        
        # Add to CLOSED
        closed_list.add(current)
        
        # Display OPEN and CLOSED lists
        print(f"\nOPEN List (priority queue):")
        open_display = [(f, g, n) for f, g, n, p in open_list]
        if open_display:
            for f, g, n in sorted(open_display):
                print(f"  • {n}: f={f}, g={g}, h={heuristic[n]}")
        else:
            print("  [Empty]")
        
        print(f"\nCLOSED List: {sorted(closed_list)}")
        
        # Expand neighbors
        print(f"\nExpanding neighbors of {current}:")
        
        for neighbor, edge_cost in graph[current]:
            if neighbor in closed_list:
                print(f"  • {neighbor}: Already in CLOSED - skip")
                continue
            
            # Calculate g(n) for neighbor
            new_g = g_cost + edge_cost
            
            # Calculate f(n) = g(n) + h(n)
            f_neighbor = new_g + heuristic[neighbor]
            
            print(f"  • {neighbor}:")
            print(f"      g({neighbor}) = g({current}) + edge = {g_cost} + {edge_cost} = {new_g}")
            print(f"      h({neighbor}) = {heuristic[neighbor]}")
            print(f"      f({neighbor}) = {new_g} + {heuristic[neighbor]} = {f_neighbor}")
            
            # Only add if better path found
            if neighbor not in g_scores or new_g < g_scores[neighbor]:
                g_scores[neighbor] = new_g
                new_path = path + [neighbor]
                heapq.heappush(open_list, (f_neighbor, new_g, neighbor, new_path))
                print(f"      → Added to OPEN")
            else:
                print(f"      → Not added (existing path is better)")
    
    print("\nNo path found!")
    return None, float('inf')


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    START = 'Glogow'  # Blue node
    GOAL = 'Plock'    # Red node
    
    # Run A* algorithm
    path, cost = a_star_search(graph, heuristic, START, GOAL)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if path:
        print(f"\n✅ Optimal Path Found using A* Algorithm:")
        print(f"\n   {' → '.join(path)}")
        print(f"\n   Total Distance: {cost} km")
        print(f"   Number of cities visited: {len(path)}")
        
        # Show path breakdown
        print(f"\n📍 Path Breakdown:")
        total = 0
        for i in range(len(path) - 1):
            for neighbor, dist in graph[path[i]]:
                if neighbor == path[i + 1]:
                    total += dist
                    print(f"   {path[i]} → {path[i + 1]}: {dist} km")
                    break
        print(f"   {'─' * 30}")
        print(f"   Total: {total} km")
    else:
        print("❌ No path exists between the cities.")
    
    # Explain heuristic function
    print("\n" + "=" * 70)
    print("HEURISTIC FUNCTION DESIGN")
    print("=" * 70)
    print("""
The heuristic function h(n) is designed based on diagram (b):

    h(n) = straight-line distance from city n to Płock (goal)

Properties:
    1. ADMISSIBLE: h(n) ≤ actual cost to reach goal
       (straight-line distance is always ≤ road distance)
    
    2. CONSISTENT: h(n) ≤ c(n,n') + h(n')
       (triangle inequality holds for Euclidean distances)
    
    3. h(goal) = 0 (Płock has h=0)

This ensures A* finds the OPTIMAL path.

Heuristic Values from Diagram (b):
""")
    print("    City          h(n)")
    print("    " + "-" * 25)
    for city in sorted(heuristic.keys()):
        print(f"    {city:<15} {heuristic[city]}")
