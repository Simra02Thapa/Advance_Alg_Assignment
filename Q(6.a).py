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