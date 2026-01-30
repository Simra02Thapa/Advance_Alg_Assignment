# Advanced Algorithm Assignment
**Semester:** 4th Semester  



## Question 1(a) - Optimal Hub Placement

**File**: `Q(1.a).py`

### Description
Finds the optimal location to place a hub that minimizes total distance to all sensors using Weiszfeld's Algorithm (a gradient descent approach for the geometric median problem).

### Algorithm Used
- **Weiszfeld's Algorithm** (Iterative weighted centroid refinement)
- Starts with centroid as initial guess
- Iteratively moves toward optimal position

### Output Reflection
```
Optimal Hub Location: (x, y)
Total Distance from Hub to all Sensors: xxx units
Iterations to converge: xxx
```


## Question 1(b) - Traveling Salesman Problem

**File:** `Q(1.b).py`

### Description
Solves the classic Traveling Salesman Problem (TSP) using Simulated Annealing metaheuristic. Finds a near-optimal tour visiting all cities exactly once with minimum total distance.

### Algorithm Used
- **Simulated Annealing** with two cooling schedules:
  - Exponential cooling
  - Linear cooling
- Neighbor operations: Swap and 2-Opt

### Output Reflection
```
Initial Tour Cost: xxxx
Final Tour Cost: xxxx (Optimized)
Cooling Schedule: Exponential/Linear
Tour: [City1 → City2 → ... → City1]
```

---



## Question 2 - Strategic Tile Shatter

**File:** `Q(2).py`

### Description
Solves the Burst Balloons / Tile Shatter problem using Interval Dynamic Programming. Finds the maximum points obtainable by strategically shattering tiles.

### Algorithm Used
- Interval DP (similar to Matrix Chain Multiplication)
- State: `dp[left][right]` = max points for tiles between boundaries
- Transition: Try bursting each tile last in the interval

### Output Reflection
```
Example: Tile_multipliers = [3, 1, 5, 8]
DP Table progression shown step-by-step
Maximum Points: 167
```

---



## Question 3 - Minimum Service Centers

**File:** `Q(3).py`

### Description
Finds the minimum number of service centers needed to cover all nodes in a binary tree using Tree DP with Greedy approach.

### Algorithm Used
DFS-based Tree DP
- States: Needs service (0), Has center (1), Covered (2)
- Greedy: Place center at parent if child needs service

### Output Reflection
```
Service center placed at node X
Service center placed at node Y
Minimum Service Centers Required: N
```

---




## Question 4 - Smart Energy Grid Optimization

**File:** `Q(4).py`

### Description
Optimizes energy distribution across multiple districts in Nepal using multiple energy sources (Solar, Hydro, Diesel) while minimizing cost and diesel usage.

### Algorithm Used
- Greedy Strategy: Allocate cheapest source first (Solar → Hydro → Diesel)
- Dynamic Programming Concept: Track state at each hour

### Constraints
- Demand tolerance: ±10%
- Source availability: Solar (6AM-6PM), Hydro (24h), Diesel (24h)

### Output Reflection
```
Districts: Kathmandu, Pokhara, Biratnagar, Bharatpur
Total Energy Served: 27,650 kWh
Total Cost: NPR 221,690
Renewable Energy: 93.9%
Diesel Usage: 6.1% (only during peak evening hours)
```

---



## Question 5(a) - Emergency Network Simulator

**File:** `Q(5. a).py`

### Description
An interactive GUI-based Emergency Network Simulator designed for disaster response routing. The system models a city network (8 cities: A-H) where emergency responders can find optimal paths, identify vulnerable infrastructure, and simulate node failures to test network resilience.

### Features
The simulator integrates five core modules addressing different aspects of network optimization.
 **Q1 (MST)** computes the minimum spanning tree using Kruskal's algorithm to find the most cost-efficient way to connect all cities. **Q2 (Reliable Paths)** finds K edge-disjoint paths between source and destination while avoiding vulnerable roads, ensuring backup routes exist. 
 **Q3 (BST Optimization)** uses the DSW algorithm to balance the command hierarchy tree for efficient lookups. 
 **Q4 (Vulnerable Roads)** allows users to mark dangerous roads which are displayed as red dotted lines and automatically avoided by pathfinding. **Q5 (Node Failure Simulation)** enables users to disable cities to simulate failures, automatically visualizing disconnected nodes and recomputing alternative routes with impact analysis.

### Algorithms Used
- **Kruskal's Algorithm**: For MST computation - O(E log E)
- **Dijkstra's Algorithm**: For shortest path finding - O((V+E) log V)
- **Connected Components**: For detecting disconnected nodes after failure


### Code Reflection
This simulator demonstrates how graph algorithms address real-world emergency routing challenges. The MST provides cost-efficient infrastructure planning, while edge-disjoint paths ensure redundancy for critical routes. The node failure simulation reveals how a single point of failure can cascade through a network, disconnecting multiple nodes and significantly increasing travel times. The interactive GUI allows users to experiment with different failure scenarios and understand network vulnerability.

---



## Question 5(b) - Multithreaded Sorting System

**File:** `Q(5.b)GUI.py`

### Description
A GUI-based **Multithreaded Sorting System** that demonstrates parallel sorting using multiple threads. The program divides the input array into two halves, sorts them concurrently using separate threads, and merges the results.

### Features
- **Multithreading**: Uses 3 threads (2 for sorting halves, 1 for merging)
- **QuickSort Algorithm**: Efficient O(n log n) sorting for each half
- **Thread Synchronization**: Uses locks and join() for proper coordination
- **Real-time Logging**: Displays thread execution status in real-time
- **Modern GUI**: Interactive interface with input validation

### Algorithms Used
- **QuickSort**: Lomuto partition scheme - O(n log n) average case
- **Merge**: Two-pointer technique to combine sorted halves - O(n)
- **Thread Synchronization**: join() ensures merge waits for sort completion

### Output Reflection

**GUI Components:**
- Input field for entering integers (comma or space separated)
- Sort, Random (20), and Clear buttons
- Thread Execution Log showing real-time thread activity
- Sorting Results section displaying Original and Sorted arrays

**Results:**
- Original: 47, 65, 40, 16, 82, 53, 56, 66, 38, 99, 10, 70, 14, 48, 100, 35, 20, 14, 5, 78
- Sorted: 5, 10, 14, 14, 16, 20, 35, 38, 40, 47, 48, 53, 56, 65, 66, 70, 78, 82, 99, 100

---



## Question 6.1(a) - Depth-First Search (DFS)

**File:** `Q.6(1.a).py`

### Description
Implements Depth-First Search (DFS) algorithm to find a path from Glogow (Start - Blue node) to Płock (Goal - Red node) on the Poland cities map. Uses Open and Closed containers to demonstrate the algorithm's working.

### Algorithm
Depth-First Search explores as far as possible along each branch before backtracking.

### Data Structures
- **Open Container**: Stack (LIFO) - stores nodes to be explored
- **Closed Container**: Set - stores already visited nodes

### Output Reflection

**State Space:**
- Total Cities: 17
- Start: Glogow (Blue), Goal: Plock (Red)

**Step-by-Step Execution:**
```
Step 1: Open=[Glogow], Closed=[]
Step 2: Open=[Wroclaw, Leszno], Closed=[Glogow]
Step 3: Open=[Wroclaw, Kalisz, Poznan], Closed=[Glogow, Leszno]
Step 4: Open=[Wroclaw, Kalisz, Bydgoszcz], Closed=[Glogow, Leszno, Poznan]
Step 5: Open=[Wroclaw, Kalisz, Wloclawek], Closed=[..., Bydgoszcz]
Step 6: Open=[..., Plock], Closed=[..., Wloclawek]
        GOAL REACHED! ✓
```

**Final Path:** Glogow → Leszno → Poznan → Bydgoszcz → Wloclawek → Plock
**Total Distance:** 440 km

---



## Question 6.1(b) - Breadth-First Search (BFS)

**File:** `Q.6(1.b).py`

### Description
Implements Breadth-First Search (BFS) algorithm to find the shortest path (by edges) from Glogow to Płock. Uses Queue (FIFO) for Open container.

### Algorithm
**Breadth-First Search** explores all neighbors at current depth before moving to next level.

### Data Structures
- **Open Container**: Queue (FIFO) - stores nodes level by level
- **Closed Container**: Set - stores already visited nodes

### Output Reflection

**Step-by-Step Execution:**
```
Level 0: Open=[Glogow], Closed=[]
Level 1: Open=[Leszno, Wroclaw], Closed=[Glogow]
Level 2: Open=[Wroclaw, Poznan, Kalisz], Closed=[Glogow, Leszno]
Level 3: Open=[..., Bydgoszcz, Konin], Closed=[...]
Level 4: Open=[..., Wloclawek], Closed=[...]
Level 5: Open=[..., Plock], GOAL REACHED! ✓
```

**Final Path:** Glogow → Leszno → Poznan → Bydgoszcz → Wloclawek → Plock
**Path Length:** 5 edges
**Comparison:** BFS explores more nodes but guarantees shortest path by edge count.

---


## Question 6.2 - A* Algorithm

**File:** `Q.6(2).py`

### Description
Implements A* Search Algorithm to find the optimal shortest distance path from Glogow to Płock using heuristic function (straight-line distances).

### Algorithm
**A* Search** uses: `f(n) = g(n) + h(n)`
- `g(n)`: Actual cost from start to n
- `h(n)`: Heuristic (estimated cost from n to goal)

### Heuristic Function
Straight-line distances from each city to Płock (from diagram b):
```
h(Glogow)=200, h(Leszno)=170, h(Poznan)=160, h(Bydgoszcz)=90
h(Wloclawek)=44, h(Plock)=0, h(Konin)=96, h(Warsaw)=95
```

### Output Reflection

**Step-by-Step Execution:**
```
Step 1: Open=[(f=200, Glogow)]
        Expand Glogow: f(Leszno)=45+170=215
        
Step 2: Open=[(f=215, Leszno), (f=340, Wroclaw)]
        Expand Leszno: f(Poznan)=135+160=295
        
Step 3: Expand Poznan: f(Bydgoszcz)=275+90=365

Step 4: Expand Bydgoszcz: f(Wloclawek)=385+44=429

Step 5: Expand Wloclawek: f(Plock)=440+0=440
        GOAL REACHED! ✓
```

**Final Path:** Glogow → Leszno → Poznan → Bydgoszcz → Wloclawek → Plock
**Total Distance:** 440 km
**Optimality:** A* guarantees optimal path due to admissible heuristic

**Comparison of All Three Algorithms:**
| Algorithm | Nodes Explored | Optimality |
|-----------|----------------|------------|
| DFS | Fewer | Not guaranteed |
| BFS | More | Optimal by edges |
| A* | Moderate | Optimal by distance |

---

## Question 6.3 - Advantages and Disadvantages of BFS, DFS, and A*

### Context: Poland Cities Pathfinding Problem
Problem: Find path from Glogow (Blue) to Płock (Red) on a weighted graph of 17 Polish cities.
All algorithms found the same path: Glogow → Leszno → Poznan → Bydgoszcz → Wloclawek → Plock (440 km)

---

### 1. Depth-First Search (DFS)

#### Advantages:
| Advantage | Explanation (Based on Our Problem) |
|-----------|-----------------------------------|
| **Memory Efficient** | DFS only stores nodes along the current path. In our 17-city graph, it stored maximum ~6 nodes at a time (path depth), compared to BFS which stored entire levels. |
| **Fast for Deep Solutions** | Since Płock was reachable through a deep path (5 hops), DFS found it quickly by going deep first through Leszno → Poznan → Bydgoszcz → Wloclawek → Plock. |
| **Simple Implementation** | Uses a simple Stack (LIFO). Our implementation used Python list with append/pop operations. |
| **Good for Maze/Path Problems** | Works well when any solution is acceptable, not necessarily the optimal one. |

#### Disadvantages:
| Disadvantage | Explanation (Based on Our Problem) |
|--------------|-----------------------------------|
| **No Optimality Guarantee** | DFS found path of 440 km, but it could have found a longer path if the graph had different structure. It doesn't consider edge weights. |
| **Can Get Stuck in Deep Branches** | If Wroclaw branch (from Glogow) led to a very deep dead-end, DFS would explore it fully before trying Leszno branch. |
| **Not Complete in Infinite Graphs** | Could loop forever without proper cycle detection (we used Closed set to prevent this). |
| **Ignores Distance/Cost** | DFS treats all edges equally - doesn't prefer shorter routes over longer ones. |

---

### 2. Breadth-First Search (BFS)

#### Advantages:
| Advantage | Explanation (Based on Our Problem) |
|-----------|-----------------------------------|
| **Guarantees Shortest Path (by edges)** | BFS found the path with minimum number of hops (5 edges). If we only cared about fewest cities to traverse, BFS is optimal. |
| **Complete Algorithm** | BFS will always find a solution if one exists. It systematically explores all nodes level by level. |
| **Finds All Shortest Paths** | Can be modified to find all paths of the same shortest length. |
| **Good for Unweighted Graphs** | Perfect when all edges have equal cost (e.g., counting number of transfers in metro). |

#### Disadvantages:
| Disadvantage | Explanation (Based on Our Problem) |
|--------------|-----------------------------------|
| **High Memory Usage** | BFS stored entire levels in the queue. At Level 3, it had to store multiple cities (Bydgoszcz, Konin, Kalisz, etc.) simultaneously. |
| **Not Optimal for Weighted Graphs** | BFS found 5-hop path, but if there was a 4-hop path with longer total distance, BFS would prefer the 4-hop one - ignoring actual road distances. |
| **Slower for Deep Solutions** | Must explore ALL nodes at levels 0,1,2,3,4 before reaching Płock at level 5. In our case, explored more nodes than necessary. |
| **Ignores Edge Weights** | Treats Glogow-Leszno (45km) same as Glogow-Wroclaw (140km) - doesn't use distance information. |

---

### 3. A* Algorithm

#### Advantages:
| Advantage | Explanation (Based on Our Problem) |
|-----------|-----------------------------------|
| **Guarantees Optimal Path (by distance)** | A* found the true shortest path of 440 km by considering actual road distances. This is crucial for real navigation. |
| **Uses Heuristic Intelligence** | The straight-line distance heuristic (from diagram b) guided search toward Płock, avoiding unnecessary exploration of southern cities (Krakow, Katowice). |
| **Efficient Exploration** | Explored fewer nodes than BFS because heuristic pruned unpromising branches. Didn't fully explore Wroclaw→Opole→Czestochowa path. |
| **Admissible Heuristic = Optimal** | Since straight-line distance never overestimates road distance, A* guaranteed to find the optimal 440 km path. |
| **Best of Both Worlds** | Combines BFS's completeness with greedy search's efficiency. |

#### Disadvantages:
| Disadvantage | Explanation (Based on Our Problem) |
|--------------|-----------------------------------|
| **Requires Good Heuristic** | We needed straight-line distances from diagram (b). Without this data, A* cannot function properly. |
| **Heuristic Design is Critical** | A poor heuristic (overestimating) would lose optimality guarantee. We carefully used admissible values. |
| **More Complex Implementation** | Required priority queue, heuristic lookup table, and f(n)=g(n)+h(n) calculation at each step. |
| **Memory for Heuristic Storage** | Needed to store h(n) values for all 17 cities - additional space overhead. |
| **Computation Overhead** | Each node expansion requires heuristic calculation and priority queue operations (O(log n)). |

---

### Summary Comparison Table

| Criteria | DFS | BFS | A* |
|----------|-----|-----|-----|
| **Data Structure** | Stack (LIFO) | Queue (FIFO) | Priority Queue |
| **Time Complexity** | O(V + E) | O(V + E) | O(E log V) |
| **Space Complexity** | O(depth) = O(V) | O(width) = O(V) | O(V) |
| **Completeness** | No (may loop) | Yes | Yes |
| **Optimal (edges)** | No | Yes | Yes |
| **Optimal (distance)** | No | No | Yes |
| **Nodes Explored (our problem)** | ~6 | ~12 | ~8 |
| **Uses Edge Weights** | No | No | Yes |
| **Uses Heuristic** | No | No | Yes |
| **Best For** | Memory-limited, any path ok | Unweighted shortest path | Weighted shortest path |

---

### Conclusion for Poland Cities Problem

For our **Glogow to Płock navigation problem**:

1. **If memory is limited** → Use **DFS** (but accept potentially suboptimal paths)

2. **If counting hops/transfers** → Use **BFS** (guarantees fewest cities traversed)

3. **If minimizing travel distance** → Use **A*** (guarantees shortest km path with good heuristic)

**Recommendation:** For real-world GPS navigation like this Poland map, **A* is the best choice** because:
- It finds the truly shortest path (440 km)
- It's efficient with a good heuristic (straight-line distances)
- It balances memory usage and optimality

---






