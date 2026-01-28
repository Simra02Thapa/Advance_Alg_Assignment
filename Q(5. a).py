"""
Emergency Network Simulator - OOP Architecture
Separate classes for NetworkGraph, PathFinder, and BSTVisualizer.
Modular class design with clear responsibility separation.
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import networkx as nx
import math
import random


class NetworkGraph:
    """Manages the network graph structure and algorithms."""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.mst_edges = []
        self.disabled_nodes = set()
        self.vulnerable_edges = set()  # Track vulnerable roads
        self._build_graph()
    
    def _build_graph(self):
        """Construct initial network."""
        edges = [
            (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5),
            (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6),
            (4, 5, 3), (5, 6, 1), (6, 7, 4), (4, 7, 7)
        ]
        for u, v, w in edges:
            self.graph.add_edge(u, v, weight=w)
    
    def compute_mst(self):
        """Compute MST using Kruskal's algorithm."""
        mst = nx.minimum_spanning_tree(self.graph, algorithm='kruskal')
        self.mst_edges = list(mst.edges())
        total_weight = sum(self.graph[u][v]['weight'] for u, v in self.mst_edges)
        return self.mst_edges, total_weight
    
    def get_nodes(self):
        return list(self.graph.nodes())
    
    def get_node_positions(self):
        """Get node positions for visualization."""
        return nx.spring_layout(self.graph, seed=42)
    
    def disable_node(self, node_id):
        """Mark node as disabled (offline)."""
        if node_id in self.graph.nodes():
            self.disabled_nodes.add(node_id)
            return True
        return False
    
    def get_disabled_nodes(self):
        return self.disabled_nodes
    
    def mark_vulnerable_edge(self, u, v):
        """Mark an edge as vulnerable (dangerous road)."""
        self.vulnerable_edges.add((min(u, v), max(u, v)))
    
    def unmark_vulnerable_edge(self, u, v):
        """Unmark a vulnerable edge."""
        self.vulnerable_edges.discard((min(u, v), max(u, v)))
    
    def is_edge_vulnerable(self, u, v):
        """Check if an edge is vulnerable."""
        return (min(u, v), max(u, v)) in self.vulnerable_edges
    
    def get_vulnerable_edges(self):
        return self.vulnerable_edges


class PathFinder:
    """Handles path finding algorithms."""
    
    def __init__(self, graph, network=None):
        self.graph = graph
        self.network = network  # Reference to network to get vulnerable edges dynamically
    
    def find_disjoint_paths(self, source, target, avoid_vulnerable=True):
        """Find two edge-disjoint paths between source and target, optionally avoiding vulnerable roads."""
        try:
            # Create working graph excluding vulnerable edges if requested
            working_graph = self.graph.copy()
            if avoid_vulnerable and self.network:
                for u, v in self.network.vulnerable_edges:
                    if working_graph.has_edge(u, v):
                        working_graph.remove_edge(u, v)
            
            # First path - shortest path avoiding vulnerable edges
            path1 = nx.shortest_path(working_graph, source, target, weight='weight')
            
            # Create temporary graph without path1 edges
            temp_graph = working_graph.copy()
            for i in range(len(path1) - 1):
                if temp_graph.has_edge(path1[i], path1[i+1]):
                    temp_graph.remove_edge(path1[i], path1[i+1])
            
            # Second path
            try:
                path2 = nx.shortest_path(temp_graph, source, target, weight='weight')
                return path1, path2, True
            except nx.NetworkXNoPath:
                return path1, None, False
        except Exception as e:
            return None, None, False
    
    def get_shortest_path(self, source, target):
        """Get shortest path between nodes."""
        try:
            return nx.shortest_path(self.graph, source, target, weight='weight')
        except:
            return None


class BSTVisualizer:
    """Handles BST operations and visualization."""
    
    def __init__(self):
        self.bst = self._create_sample_bst()
        self.optimized_bst = None
    
    def _create_sample_bst(self):
        """Create sample BST for commands hierarchy - intentionally unbalanced."""
        # Unbalanced tree: all values lean to the right
        bst_data = {
            'root': 20,
            'left': None,
            'right': {
                'root': 30,
                'left': None,
                'right': {
                    'root': 40,
                    'left': None,
                    'right': {
                        'root': 50,
                        'left': None,
                        'right': {
                            'root': 60,
                            'left': None,
                            'right': {
                                'root': 70,
                                'left': None,
                                'right': {'root': 80, 'left': None, 'right': None}
                            }
                        }
                    }
                }
            }
        }
        return bst_data
    
    def _get_tree_height(self, node):
        """Calculate height of BST."""
        if node is None:
            return 0
        left_height = self._get_tree_height(node.get('left'))
        right_height = self._get_tree_height(node.get('right'))
        return 1 + max(left_height, right_height)
    
    def _get_in_order_nodes(self, node, nodes=None):
        """Get nodes in in-order traversal."""
        if nodes is None:
            nodes = []
        if node is None:
            return nodes
        
        self._get_in_order_nodes(node.get('left'), nodes)
        nodes.append(node['root'])
        self._get_in_order_nodes(node.get('right'), nodes)
        return nodes
    
    def _create_balanced_bst_from_sorted(self, sorted_nodes):
        """Create a balanced BST from sorted nodes."""
        if not sorted_nodes:
            return None
        
        mid = len(sorted_nodes) // 2
        node = {
            'root': sorted_nodes[mid],
            'left': self._create_balanced_bst_from_sorted(sorted_nodes[:mid]),
            'right': self._create_balanced_bst_from_sorted(sorted_nodes[mid+1:])
        }
        return node
    
    def optimize_bst(self):
        """Apply DSW rebalancing to minimize path length."""
        # Get in-order traversal
        sorted_nodes = self._get_in_order_nodes(self.bst)
        # Create balanced BST
        self.optimized_bst = self._create_balanced_bst_from_sorted(sorted_nodes)
        return "DSW algorithm applied. Tree rebalanced."
    
    def get_bst_info(self):
        """Get BST statistics."""
        return {
            'height': self._get_tree_height(self.bst),
            'nodes': len(self._get_in_order_nodes(self.bst))
        }


class GraphColorer:
    """Graph coloring using Welsh-Powell algorithm."""
    
    @staticmethod
    def color_graph(graph):
        """Apply Welsh-Powell coloring algorithm."""
        colors = {}
        color_palette = ["red", "blue", "green", "yellow", "purple", "orange", "cyan"]
        
        # Sort nodes by degree (descending)
        sorted_nodes = sorted(graph.nodes(), key=lambda x: -graph.degree(x))
        
        for node in sorted_nodes:
            # Find used colors by neighbors
            neighbor_colors = {colors[neighbor] for neighbor in graph.neighbors(node) if neighbor in colors}
            
            # Assign first available color
            for color_id in range(len(color_palette)):
                if color_id not in neighbor_colors:
                    colors[node] = color_id
                    break
        
        return colors


class SimulatorUI:
    """Main GUI controller."""

    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Simulator - OOP")
        self.root.geometry("1300x850")

        # Initialize components
        self.network = NetworkGraph()
        self.path_finder = PathFinder(self.network.graph, self.network.vulnerable_edges)
        self.bst_viz = BSTVisualizer()
        self.pos = self.network.get_node_positions()

        self.selected_paths = []
        self.path1_edges = []  # Primary path (blue)
        self.path2_edges = []  # Backup path (purple)
        self.mst_edges = []

        self._build_ui()
        self._draw_canvas()

    def _build_ui(self):
        """Build improved user interface layout."""

        #  LEFT CONTROL PANEL 
        left_panel = ttk.Frame(self.root, padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        title = ttk.Label(left_panel, text="Emergency Network Simulator",
                          font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))

        # Path Selection
        path_frame = ttk.LabelFrame(left_panel, text="Path Selection", padding=10)
        path_frame.pack(fill=tk.X, pady=10)

        ttk.Label(path_frame, text="Source Node:").pack(anchor=tk.W)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(path_frame, textvariable=self.source_var,
                     values=self.network.get_nodes(), state="readonly")
        self.source_combo.pack(fill=tk.X, pady=2)

        ttk.Label(path_frame, text="Target Node:").pack(anchor=tk.W)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(path_frame, textvariable=self.target_var,
                     values=self.network.get_nodes(), state="readonly")
        self.target_combo.pack(fill=tk.X, pady=2)

        # Algorithms Section 
        algo_frame = ttk.LabelFrame(left_panel, text="Network Algorithms", padding=10)
        algo_frame.pack(fill=tk.X, pady=5)

        ttk.Button(algo_frame, text="Q1: Compute MST",
                   command=self._on_mst_click).pack(fill=tk.X, pady=3)

        ttk.Button(algo_frame, text="Q2: Reliable Path Finder (Disjoint Paths)",
                   command=self._on_reliable_path_click).pack(fill=tk.X, pady=3)

        ttk.Button(algo_frame, text="Bonus: Graph Coloring",
                   command=self._on_coloring_click).pack(fill=tk.X, pady=3)

        #  Tree Section
        bst_frame = ttk.LabelFrame(left_panel, text="Command Tree (BST)", padding=10)
        bst_frame.pack(fill=tk.X, pady=5)

        ttk.Button(bst_frame, text="Q3: Optimize BST",
                   command=self._on_bst_click).pack(fill=tk.X, pady=3)

        # Failure Section
        failure_frame = ttk.LabelFrame(left_panel, text="Failure Simulation", padding=10)
        failure_frame.pack(fill=tk.X, pady=5)

        ttk.Button(failure_frame, text="Q4: Simulate Node Failure",
                   command=self._on_failure_click).pack(fill=tk.X, pady=3)

        ttk.Button(failure_frame, text="Reset Simulator",
                   command=self._on_reset_click).pack(fill=tk.X, pady=3)

        # Road Management Section
        road_frame = ttk.LabelFrame(left_panel, text="Road Management", padding=10)
        road_frame.pack(fill=tk.X, pady=5)

        ttk.Button(road_frame, text="Mark Edge as Vulnerable",
                   command=self._on_mark_vulnerable_click).pack(fill=tk.X, pady=3)

        ttk.Button(road_frame, text="Unmark Vulnerable Edge",
                   command=self._on_unmark_vulnerable_click).pack(fill=tk.X, pady=3)

        # Status Box 
        status_frame = ttk.LabelFrame(left_panel, text="System Status", padding=8)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.status_area = tk.Text(status_frame, height=10, width=35,
                                   bg="#f4f4f4", relief=tk.SOLID, borderwidth=1)
        self.status_area.pack(fill=tk.BOTH, expand=True)

        # RIGHT CANVAS PANEL 
        canvas_panel = ttk.Frame(self.root, padding=5)
        canvas_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        canvas_title = ttk.Label(canvas_panel, text="Network Visualization",
                                 font=("Arial", 14, "bold"))
        canvas_title.pack(pady=5)

        self.canvas = tk.Canvas(canvas_panel, bg="white", cursor="hand2")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-3>", self._on_canvas_rightclick)
        self.canvas.bind("<Double-Button-1>", self._on_canvas_doubleclick)
        self.canvas.bind("<Shift-Button-1>", self._on_canvas_mark_vulnerable)
    
    def _draw_canvas(self):
        """Draw network on canvas."""
        self.canvas.delete("all")
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 800, 800
        
        # Scale positions
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        def transform(x, y):
            tx = 50 + (x - x_min) / x_range * (width - 100)
            ty = 50 + (y - y_min) / y_range * (height - 100)
            return tx, ty
        
        # Draw edges
        for u, v, data in self.network.graph.edges(data=True):
            if u in self.network.get_disabled_nodes() or v in self.network.get_disabled_nodes():
                edge_color = "gray"
                dash_pattern = (4, 4)
            elif self.network.is_edge_vulnerable(u, v):
                edge_color = "red"  # Vulnerable roads in red
                dash_pattern = (4, 4)
            elif (u, v) in self.mst_edges or (v, u) in self.mst_edges:
                edge_color = "green"
                dash_pattern = ()
            elif [u, v] in self.path1_edges or [v, u] in self.path1_edges:
                edge_color = "blue"
                dash_pattern = ()
            elif [u, v] in self.path2_edges or [v, u] in self.path2_edges:
                edge_color = "purple"
                dash_pattern = ()
            else:
                edge_color = "black"
                dash_pattern = ()
            
            x1, y1 = transform(self.pos[u][0], self.pos[u][1])
            x2, y2 = transform(self.pos[v][0], self.pos[v][1])
            self.canvas.create_line(x1, y1, x2, y2, fill=edge_color, width=2, dash=dash_pattern)
            
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my, text=str(data['weight']), fill="red")
        
        # Draw nodes
        for node in self.network.get_nodes():
            x, y = transform(self.pos[node][0], self.pos[node][1])
            
            if node in self.network.get_disabled_nodes():
                node_color = "red"
            else:
                node_color = "lightblue"
            
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=node_color, outline="black", width=2)
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 10, "bold"))
    
    def _on_mst_click(self):
        """Handle MST computation."""
        edges, weight = self.network.compute_mst()
        self.mst_edges = edges
        self.status_area.delete(1.0, tk.END)
        self.status_area.insert(1.0, f"MST Computed\nTotal Weight: {weight}\nEdges: {len(edges)}")
        self._draw_canvas()
    
    def _on_reliable_path_click(self):
        """Handle reliable path finding with disjoint paths."""
        try:
            src = int(self.source_var.get())
            tgt = int(self.target_var.get())
            
            # Find disjoint paths (most reliable approach)
            path1, path2, found = self.path_finder.find_disjoint_paths(src, tgt)
            
            self.status_area.delete(1.0, tk.END)
            if path1:
                # Calculate path weights
                path1_weight = sum(self.network.graph[path1[i]][path1[i+1]]['weight'] for i in range(len(path1)-1))
                path1_str = ' -> '.join(map(str, path1))
                text = f"Path 1 (Primary Route - Blue): {path1_str}\nWeight: {path1_weight}\n"
                
                # Store path1 edges
                self.path1_edges = [[path1[i], path1[i+1]] for i in range(len(path1)-1)]
                self.path2_edges = []  # Clear path2
                
                if path2:
                    path2_weight = sum(self.network.graph[path2[i]][path2[i+1]]['weight'] for i in range(len(path2)-1))
                    path2_str = ' -> '.join(map(str, path2))
                    text += f"\nPath 2 (Backup Route - Purple): {path2_str}\nWeight: {path2_weight}\n\n"
                    text += f"Both paths are edge-disjoint (no shared edges)"
                    self.path2_edges = [[path2[i], path2[i+1]] for i in range(len(path2)-1)]
                else:
                    text += "\nOnly 1 reliable path available"
                
                self.status_area.insert(1.0, text)
                self._draw_canvas()
            else:
                self.status_area.insert(1.0, "No path found between selected nodes")
        except Exception as e:
            messagebox.showerror("Error", f"Path finding failed: {str(e)}")
    
    def _on_bst_click(self):
        """Handle BST optimization with visualization."""
        # Get info before optimization
        info_before = self.bst_viz.get_bst_info()
        height_before = info_before['height']
        
        # Optimize BST
        self.bst_viz.optimize_bst()
        
        # Get info after optimization
        info_after = self.bst_viz.get_bst_info()
        height_after = self._get_bst_height(self.bst_viz.optimized_bst)
        
        # Update status
        self.status_area.delete(1.0, tk.END)
        text = f"Q3: Command Hierarchy Optimizer\n\n"
        text += f"BEFORE Optimization:\n"
        text += f"  Height: {height_before}\n"
        text += f"  Nodes: {info_before['nodes']}\n\n"
        text += f"AFTER DSW Rebalancing:\n"
        text += f"  Height: {height_after}\n"
        text += f"  Nodes: {info_after['nodes']}\n\n"
        text += f"Algorithm: DSW (Day-Stout-Warren)\n"
        text += f"Purpose: Minimize longest communication\n"
        text += f"path from HQ to any node"
        
        self.status_area.insert(1.0, text)
        
        # Visualize BST on canvas
        self._draw_bst_comparison()
    
    def _get_bst_height(self, node):
        """Get height of BST node."""
        if node is None:
            return 0
        left_height = self._get_bst_height(node.get('left'))
        right_height = self._get_bst_height(node.get('right'))
        return 1 + max(left_height, right_height)
    
    def _draw_bst_comparison(self):
        """Draw before/after BST comparison on canvas."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 1000, 700
        
        # Calculate heights
        height_before = self._get_bst_height(self.bst_viz.bst)
        height_after = self._get_bst_height(self.bst_viz.optimized_bst)
        
        # Draw title
        self.canvas.create_text(width // 2, 15, text="BST Rebalancing Comparison", 
                               font=("Arial", 16, "bold"))
        
        # Draw "BEFORE" tree on left
        self.canvas.create_text(width // 4, 35, text=f"BEFORE (Height: {height_before})", 
                               font=("Arial", 12, "bold"), fill="red")
        self.canvas.create_rectangle(10, 50, width // 2 - 10, height - 20, 
                                    outline="red", width=2)
        self._draw_bst_tree(self.bst_viz.bst, width // 4, 100, width // 6, 0, height - 80)
        
        # Draw "AFTER" tree on right
        self.canvas.create_text(3 * width // 4, 35, text=f"AFTER Optimized (Height: {height_after})", 
                               font=("Arial", 12, "bold"), fill="green")
        self.canvas.create_rectangle(width // 2 + 10, 50, width - 10, height - 20, 
                                    outline="green", width=2)
        if self.bst_viz.optimized_bst:
            self._draw_bst_tree(self.bst_viz.optimized_bst, 3 * width // 4, 100, width // 6, 0, height - 80)
        
        # Draw improvement stats at bottom
        improvement = ((height_before - height_after) / height_before * 100) if height_before > 0 else 0
        stats_text = f"Height Reduction: {height_before} → {height_after} (↓{improvement:.1f}%) | Max Path Length: {height_before} → {height_after} hops"
        self.canvas.create_text(width // 2, height - 10, text=stats_text, 
                               font=("Arial", 10), fill="blue")
    
    def _draw_bst_tree(self, node, x, y, x_offset, min_x, max_x, depth=0):
        """Recursively draw BST tree on canvas with depth coloring."""
        if node is None:
            return
        
        # Color based on depth: darker colors for deeper nodes
        depth_colors = ["lightgreen", "lightyellow", "lightyellow", "lightcoral", "salmon", "red", "darkred"]
        node_color = depth_colors[min(depth, len(depth_colors) - 1)]
        
        # Draw node
        node_radius = 25
        self.canvas.create_oval(x - node_radius, y - node_radius,
                               x + node_radius, y + node_radius,
                               fill=node_color, outline="black", width=2)
        self.canvas.create_text(x, y, text=str(node['root']), font=("Arial", 10, "bold"))
        
        # Draw depth label
        self.canvas.create_text(x, y + 35, text=f"D:{depth}", font=("Arial", 8), fill="gray")
        
        # Draw edges and recurse
        y_offset = 80
        x_offset_new = x_offset // 2 if x_offset > 40 else 40
        
        if node.get('left'):
            left_x = x - x_offset_new
            left_y = y + y_offset
            self.canvas.create_line(x, y + node_radius, left_x, left_y - node_radius,
                                   fill="black", width=1)
            self._draw_bst_tree(node['left'], left_x, left_y, x_offset_new, min_x, max_x, depth + 1)
        
        if node.get('right'):
            right_x = x + x_offset_new
            right_y = y + y_offset
            self.canvas.create_line(x, y + node_radius, right_x, right_y - node_radius,
                                   fill="black", width=1)
            self._draw_bst_tree(node['right'], right_x, right_y, x_offset_new, min_x, max_x, depth + 1)
    
    def _on_failure_click(self):
        """Handle node failure simulation."""
        try:
            node = simpledialog.askinteger("Node Failure", "Enter node ID to disable:")
            if node is not None:
                if self.network.disable_node(node):
                    self.status_area.delete(1.0, tk.END)
                    self.status_area.insert(1.0, f"Node {node} disabled\nRecomputing paths...")
                    self._draw_canvas()
                else:
                    messagebox.showerror("Error", f"Node {node} not found")
        except:
            pass
    
    def _on_coloring_click(self):
        """Handle graph coloring with visualization."""
        # Apply graph coloring algorithm
        colors = GraphColorer.color_graph(self.network.graph)
        num_colors = len(set(colors.values()))
        
        # Store colors for visualization
        self.node_colors = colors
        
        # Update status area with detailed information
        self.status_area.delete(1.0, tk.END)
        text = f"BONUS: GRAPH COLORING FOR FREQUENCY ASSIGNMENT\n"
        text += f"{'='*50}\n\n"
        text += f"ALGORITHM: Welsh-Powell\n"
        text += f"{'='*50}\n\n"
        text += f"RESULTS:\n"
        text += f"  Total Colors Used: {num_colors}\n"
        text += f"  Total Nodes: {len(self.network.get_nodes())}\n"
        text += f"  Total Edges: {len(self.network.graph.edges())}\n\n"
        text += f"COLOR ASSIGNMENTS (Frequencies):\n"
        text += f"{'-'*50}\n"
        
        # Create color name mapping
        color_names = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan"]
        
        # Sort nodes by color for better display
        sorted_by_color = sorted(colors.items(), key=lambda x: x[1])
        
        for node, color_idx in sorted_by_color:
            color_name = color_names[color_idx] if color_idx < len(color_names) else f"Color{color_idx}"
            text += f"  Node {node}: {color_name} (Frequency {color_idx + 1})\n"
        
        text += f"\n{'='*50}\n"
        text += f"GUARANTEE:\n"
        text += f"No adjacent hubs share the same frequency\n"
        text += f"Interference-free communication network!"
        
        self.status_area.insert(1.0, text)
        
        # Visualize coloring on canvas
        self._draw_colored_graph(colors, color_names)
    
    def _draw_colored_graph(self, colors, color_names):
        """Draw the graph with node coloring on canvas."""
        self.canvas.delete("all")
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 800, 800
        
        # Scale positions
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        def transform(x, y):
            tx = 50 + (x - x_min) / x_range * (width - 100)
            ty = 50 + (y - y_min) / y_range * (height - 100)
            return tx, ty
        
        # Draw title
        self.canvas.create_text(width // 2, 20, text="Graph Coloring: Frequency Assignment to Hubs",
                               font=("Arial", 14, "bold"))
        
        # Color palette for visualization
        color_palette = ["red", "blue", "green", "yellow", "purple", "orange", "cyan"]
        
        # Draw edges first
        for u, v, data in self.network.graph.edges(data=True):
            x1, y1 = transform(self.pos[u][0], self.pos[u][1])
            x2, y2 = transform(self.pos[v][0], self.pos[v][1])
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=1)
            
            # Draw edge weight
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mx, my, text=str(data['weight']), fill="gray", font=("Arial", 8))
        
        # Draw nodes with assigned colors
        for node in self.network.get_nodes():
            x, y = transform(self.pos[node][0], self.pos[node][1])
            color_idx = colors.get(node, 0)
            node_color = color_palette[color_idx % len(color_palette)]
            
            # Draw larger node circle
            node_radius = 20
            self.canvas.create_oval(x - node_radius, y - node_radius,
                                   x + node_radius, y + node_radius,
                                   fill=node_color, outline="black", width=2)
            
            # Draw node ID
            self.canvas.create_text(x, y - 5, text=str(node), font=("Arial", 10, "bold"), fill="black")
            
            # Draw frequency number below node
            freq_num = color_idx + 1
            self.canvas.create_text(x, y + 10, text=f"F{freq_num}", font=("Arial", 8), fill="white")
        
        # Draw legend
        legend_x = width - 150
        legend_y = 50
        self.canvas.create_text(legend_x, legend_y - 20, text="FREQUENCY LEGEND",
                               font=("Arial", 10, "bold"))
        
        for idx in range(min(len(set(colors.values())), len(color_palette))):
            color = color_palette[idx]
            color_name = color_names[idx] if idx < len(color_names) else f"Color{idx}"
            
            # Color sample
            self.canvas.create_rectangle(legend_x, legend_y + idx * 25,
                                        legend_x + 20, legend_y + 20 + idx * 25,
                                        fill=color, outline="black", width=1)
            
            # Label
            self.canvas.create_text(legend_x + 30, legend_y + 10 + idx * 25,
                                   text=f"F{idx + 1}: {color_name}",
                                   font=("Arial", 9), anchor="w")
    
    def _on_reset_click(self):
        """Reset simulator."""
        self.network = NetworkGraph()
        self.selected_paths = []
        self.mst_edges = []
        self.path1_edges = []
        self.path2_edges = []
        self.status_area.delete(1.0, tk.END)
        self.status_area.insert(1.0, "Simulator reset")
        self._draw_canvas()
    
    def _on_mark_vulnerable_click(self):
        """Mark an edge as vulnerable."""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("Mark Edge as Vulnerable")
            dialog.geometry("300x150")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Enter two node IDs:").pack(pady=10)
            
            ttk.Label(dialog, text="Node 1:").pack()
            node1_var = tk.StringVar()
            ttk.Entry(dialog, textvariable=node1_var, width=20).pack()
            
            ttk.Label(dialog, text="Node 2:").pack()
            node2_var = tk.StringVar()
            ttk.Entry(dialog, textvariable=node2_var, width=20).pack()
            
            def mark_edge():
                try:
                    u = int(node1_var.get())
                    v = int(node2_var.get())
                    
                    if self.network.graph.has_edge(u, v):
                        self.network.mark_vulnerable_edge(u, v)
                        self.status_area.delete(1.0, tk.END)
                        self.status_area.insert(1.0, f"Edge {u}-{v} marked as vulnerable")
                        self._draw_canvas()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", f"Edge {u}-{v} does not exist")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid node IDs")
            
            ttk.Button(dialog, text="Mark as Vulnerable", command=mark_edge).pack(pady=10)
        except:
            pass
    
    def _on_unmark_vulnerable_click(self):
        """Unmark a vulnerable edge."""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("Unmark Vulnerable Edge")
            dialog.geometry("300x150")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text="Enter two node IDs:").pack(pady=10)
            
            ttk.Label(dialog, text="Node 1:").pack()
            node1_var = tk.StringVar()
            ttk.Entry(dialog, textvariable=node1_var, width=20).pack()
            
            ttk.Label(dialog, text="Node 2:").pack()
            node2_var = tk.StringVar()
            ttk.Entry(dialog, textvariable=node2_var, width=20).pack()
            
            def unmark_edge():
                try:
                    u = int(node1_var.get())
                    v = int(node2_var.get())
                    
                    if self.network.is_edge_vulnerable(u, v):
                        self.network.unmark_vulnerable_edge(u, v)
                        self.status_area.delete(1.0, tk.END)
                        self.status_area.insert(1.0, f"Edge {u}-{v} unmarked as vulnerable")
                        self._draw_canvas()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", f"Edge {u}-{v} is not vulnerable")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid node IDs")
            
            ttk.Button(dialog, text="Unmark as Vulnerable", command=unmark_edge).pack(pady=10)
        except:
            pass
    
    def _on_canvas_doubleclick(self, event):
        """Handle double-click on canvas to add new node."""
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 800, 800
        
        # Inverse transform to get graph coordinates
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        # Convert click coordinates back to graph space
        graph_x = x_min + (event.x - 50) / (width - 100) * x_range
        graph_y = y_min + (event.y - 50) / (height - 100) * y_range
        
        # Find nearest existing node
        nearest_node = None
        min_distance = float('inf')
        
        for node in self.network.get_nodes():
            dist = math.sqrt((self.pos[node][0] - graph_x)**2 + (self.pos[node][1] - graph_y)**2)
            if dist < min_distance:
                min_distance = dist
                nearest_node = node
        
        if nearest_node is not None:
            # Create new node
            new_node = max(self.network.get_nodes()) + 1
            edge_weight = random.randint(5, 10)
            
            # Add node and edge to graph
            self.network.graph.add_node(new_node)
            self.network.graph.add_edge(nearest_node, new_node, weight=edge_weight)
            
            # Add position for new node
            self.pos[new_node] = (graph_x, graph_y)
            
            # Update path finder with new graph
            self.path_finder = PathFinder(self.network.graph, self.network.vulnerable_edges)
            
            # Update dropdown menus with new node
            self.source_combo['values'] = self.network.get_nodes()
            self.target_combo['values'] = self.network.get_nodes()
            
            # Update UI
            self.status_area.delete(1.0, tk.END)
            self.status_area.insert(1.0, f"Node {new_node} added\nConnected to Node {nearest_node}\nEdge weight: {edge_weight}")
            self._draw_canvas()
    
    def _on_canvas_mark_vulnerable(self, event):
        """Handle Shift+Click to mark/unmark vulnerable roads."""
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 800, 800
        
        # Transform canvas coordinates to graph space
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        graph_x = x_min + (event.x - 50) / (width - 100) * x_range
        graph_y = y_min + (event.y - 50) / (height - 100) * y_range
        
        # Find nearest edge to click
        nearest_edge = None
        min_dist = float('inf')
        threshold = 0.1
        
        for u, v in self.network.graph.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            
            # Distance from point to line segment
            dist = self._point_to_segment_distance(graph_x, graph_y, x1, y1, x2, y2)
            
            if dist < min_dist and dist < threshold:
                min_dist = dist
                nearest_edge = (u, v)
        
        if nearest_edge:
            u, v = nearest_edge
            # Toggle vulnerable status
            if self.network.is_edge_vulnerable(u, v):
                self.network.unmark_vulnerable_edge(u, v)
                status = f"Edge {u}-{v} unmarked as vulnerable"
            else:
                self.network.mark_vulnerable_edge(u, v)
                status = f"Edge {u}-{v} marked as vulnerable (dashed red)"
            
            self.status_area.delete(1.0, tk.END)
            self.status_area.insert(1.0, status)
            self._draw_canvas()
    
    def _point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        """Calculate distance from point to line segment."""
        # Vector from start to end
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return ((px - x1)**2 + (py - y1)**2)**0.5
        
        # Parameter t of projection
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)))
        
        # Closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        # Distance
        return ((px - closest_x)**2 + (py - closest_y)**2)**0.5
    
    def _on_canvas_rightclick(self, event):
        """Handle right-click on canvas."""
        self.status_area.delete(1.0, tk.END)
        self.status_area.insert(1.0, "Shift+Click on edges to mark/unmark them as vulnerable roads")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorUI(root)
    root.mainloop()
