"""
DFS Algorithm Visualization - Single Graph
Poland Cities: Glogow (Start) to Plock (Goal)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# City coordinates for visualization
city_coords = {
    'Glogow': (0.5, 5), 'Leszno': (2, 5), 'Poznan': (2.5, 7), 'Bydgoszcz': (4, 9),
    'Wroclaw': (2.5, 3.5), 'Opole': (3.5, 1.5), 'Kalisz': (4.5, 5), 'Konin': (5.5, 7.5),
    'Wloclawek': (5.5, 8.5), 'Plock': (7, 8.5), 'Lodz': (6.5, 5.5), 'Czestochowa': (5, 3),
    'Katowice': (6, 1), 'Krakow': (8, 1.5), 'Kielce': (8.5, 3), 'Radom': (9, 5),
    'Warsaw': (8.5, 7)
}

# Graph edges from diagram (a)
edges = [
    ('Glogow', 'Leszno', 45), ('Glogow', 'Wroclaw', 140), ('Leszno', 'Poznan', 90),
    ('Leszno', 'Wroclaw', 100), ('Leszno', 'Kalisz', 140), ('Poznan', 'Bydgoszcz', 140),
    ('Poznan', 'Konin', 130), ('Bydgoszcz', 'Wloclawek', 110), ('Bydgoszcz', 'Konin', 120),
    ('Wloclawek', 'Plock', 55), ('Konin', 'Lodz', 120), ('Kalisz', 'Lodz', 120),
    ('Kalisz', 'Czestochowa', 160), ('Wroclaw', 'Opole', 100), ('Opole', 'Czestochowa', 118),
    ('Czestochowa', 'Katowice', 80), ('Czestochowa', 'Lodz', 128), ('Katowice', 'Krakow', 85),
    ('Lodz', 'Warsaw', 150), ('Lodz', 'Radom', 165), ('Lodz', 'Katowice', 280),
    ('Plock', 'Warsaw', 130), ('Warsaw', 'Radom', 105), ('Radom', 'Kielce', 82),
    ('Kielce', 'Krakow', 120)
]

# Build adjacency list
graph = {city: [] for city in city_coords}
for c1, c2, dist in edges:
    graph[c1].append((c2, dist))
    graph[c2].append((c1, dist))

# DFS Algorithm
def dfs(start, goal):
    open_list = [(start, [start])]  # Stack: (node, path)
    closed_set = set()
    steps = []
    
    while open_list:
        current, path = open_list.pop()  # LIFO - Stack
        
        if current in closed_set:
            continue
            
        closed_set.add(current)
        steps.append({
            'current': current,
            'path': path.copy(),
            'open': [x[0] for x in open_list],
            'closed': closed_set.copy()
        })
        
        if current == goal:
            return path, steps
        
        # Add neighbors (reverse for left-to-right expansion)
        neighbors = sorted(graph[current], key=lambda x: x[0], reverse=True)
        for neighbor, _ in neighbors:
            if neighbor not in closed_set:
                open_list.append((neighbor, path + [neighbor]))
    
    return None, steps

# Run DFS
path, steps = dfs('Glogow', 'Plock')

# Create visualization
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Draw all edges (gray)
for c1, c2, dist in edges:
    x1, y1 = city_coords[c1]
    x2, y2 = city_coords[c2]
    ax.plot([x1, x2], [y1, y2], 'gray', linewidth=1, alpha=0.4, zorder=1)

# Draw DFS path edges (red)
for i in range(len(path) - 1):
    x1, y1 = city_coords[path[i]]
    x2, y2 = city_coords[path[i + 1]]
    ax.plot([x1, x2], [y1, y2], 'red', linewidth=3, zorder=2)

# Draw nodes
for city, (x, y) in city_coords.items():
    if city == 'Glogow':
        color = 'blue'
        size = 400
    elif city == 'Plock':
        color = 'red'
        size = 400
    elif city in path:
        color = 'orange'
        size = 300
    else:
        color = 'lightgray'
        size = 200
    
    ax.scatter(x, y, c=color, s=size, zorder=3, edgecolors='black', linewidth=1.5)
    ax.annotate(city, (x, y), textcoords="offset points", xytext=(0, 12),
                ha='center', fontsize=9, fontweight='bold')

# Add step numbers on path
for i, city in enumerate(path):
    x, y = city_coords[city]
    ax.annotate(str(i + 1), (x, y), ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', zorder=4)

# Legend
legend_elements = [
    mpatches.Patch(color='blue', label='Start (Glogow)'),
    mpatches.Patch(color='red', label='Goal (Plock)'),
    mpatches.Patch(color='orange', label='Path Visited'),
    mpatches.Patch(color='lightgray', label='Unvisited'),
    plt.Line2D([0], [0], color='red', linewidth=3, label='DFS Path')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

# Title and info
ax.set_title('DFS (Depth-First Search) - Poland Cities\nGlogow → Plock', fontsize=16, fontweight='bold')
path_str = ' → '.join(path)
ax.text(0.5, -0.08, f'Path Found: {path_str}', transform=ax.transAxes,
        ha='center', fontsize=11, style='italic')

ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 10.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('d:/4th semester/Advance Algorithm/Advance_Assignment/DFS_Graph.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"DFS Path: {path_str}")
print("Saved: DFS_Graph.png")
