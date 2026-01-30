"""
Emergency Network Simulator - OOP Architecture
Separate classes for NetworkGraph, PathFinder, and BSTVisualizer.
Modular class design with clear responsibility separation.
Enhanced GUI with city names and modern styling.
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import networkx as nx
import math
import random

# City name mappings for network visualization
CITY_NAMES = {
    0: "A",
    1: "B", 
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H"
}

# Command names for BST visualization
COMMAND_NAMES = {
    20: "A",
    30: "B",
    40: "C",
    50: "D",
    60: "E",
    70: "F",
    80: "G"
}

# Modern color scheme
COLORS = {
    'primary': '#2563eb',        # Blue
    'secondary': '#7c3aed',      # Purple
    'success': '#10b981',        # Green
    'danger': '#ef4444',         # Red
    'warning': '#f59e0b',        # Orange
    'info': '#06b6d4',           # Cyan
    'dark': '#1f2937',           # Dark gray
    'light': '#f3f4f6',          # Light gray
    'white': '#ffffff',
    'node_default': '#60a5fa',   # Light blue
    'node_disabled': '#fca5a5',  # Light red
    'node_highlight': '#34d399', # Light green
    'edge_default': '#6b7280',   # Gray
    'edge_mst': '#3b82f6',       # Blue (MST)
    'edge_path1': '#22c55e',     # Green (Primary)
    'edge_path2': '#f97316',     # Orange (Backup)
    'edge_vulnerable': '#ef4444', # Red
    'canvas_bg': '#f8fafc',      # Very light blue-gray
    'status_bg': '#ecfdf5',      # Light green bg
    'panel_bg': '#f1f5f9'        # Light slate
}


class NetworkGraph:
    """Manages the network graph structure and algorithms."""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.mst_edges = []
        self.disabled_nodes = set()
        self.vulnerable_edges = set()  # Track vulnerable roads
        self.city_names = CITY_NAMES.copy()
        self._build_graph()
    
    def _build_graph(self):
        """Construct initial network with city connections."""
        edges = [
            (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5),
            (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6),
            (4, 5, 3), (5, 6, 1), (6, 7, 4), (4, 7, 7)
        ]
        for u, v, w in edges:
            self.graph.add_edge(u, v, weight=w)
    
    def get_city_name(self, node_id):
        """Get city name for a node."""
        return self.city_names.get(node_id, f"City-{node_id}")
    
    def compute_mst(self):
        """Compute MST using Kruskal's algorithm."""
        mst = nx.minimum_spanning_tree(self.graph, algorithm='kruskal')
        self.mst_edges = list(mst.edges())
        total_weight = sum(self.graph[u][v]['weight'] for u, v in self.mst_edges)
        return self.mst_edges, total_weight
    
    def get_nodes(self):
        return list(self.graph.nodes())
    
    def get_node_positions(self):
        """Get node positions for visualization - using circular/shell layout."""
        # Create a structured layout with cities arranged in a meaningful pattern
        # Outer ring (major cities) and inner points for connectivity
        positions = {
            0: (0.0, 1.0),      # Lahore (top)
            1: (0.95, 0.3),     # Karachi (right upper)
            2: (-0.4, 0.6),     # Islamabad (left upper)
            3: (0.6, -0.4),     # Multan (right lower)
            4: (-0.95, 0.0),    # Peshawar (far left)
            5: (0.0, -0.9),     # Quetta (bottom)
            6: (0.7, -0.9),     # Faisalabad (bottom right)
            7: (-0.7, -0.5)     # Rawalpindi (left lower)
        }
        return positions
    
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
    """Main GUI controller with enhanced modern UI."""

    def __init__(self, root):
        self.root = root
        self.root.title("🚨 Interactive Emergency Network Simulator")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['panel_bg'])

        # Initialize components
        self.network = NetworkGraph()
        self.path_finder = PathFinder(self.network.graph, self.network.vulnerable_edges)
        self.bst_viz = BSTVisualizer()
        self.pos = self.network.get_node_positions()

        self.selected_paths = []
        self.path1_edges = []  # Primary path (green)
        self.path2_edges = []  # Backup path (orange)
        self.mst_edges = []
        
        # Dragging state
        self.dragging_node = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Apply modern theme
        self._setup_styles()
        self._build_ui()
        
        # Delay initial draw until canvas is properly sized
        self.root.after(100, self._initial_draw)
    
    def _initial_draw(self):
        """Initial draw after window is fully rendered."""
        self.root.update_idletasks()  # Ensure canvas has proper dimensions
        self._draw_canvas()

    def _setup_styles(self):
        """Configure modern ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=COLORS['primary'],
                       foreground='white')
        
        style.map('Modern.TButton',
                 background=[('active', COLORS['info']), ('pressed', COLORS['dark'])])
        
        # Configure accent buttons
        style.configure('Accent.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=COLORS['success'])
        
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8),
                       background=COLORS['danger'])
        
        # Configure label frames
        style.configure('Modern.TLabelframe',
                       background=COLORS['light'],
                       padding=10)
        style.configure('Modern.TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=COLORS['dark'],
                       background=COLORS['light'])
        
        # Configure labels
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       foreground=COLORS['primary'],
                       background=COLORS['panel_bg'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=COLORS['dark'],
                       background=COLORS['panel_bg'])

    def _build_ui(self):
        """Build improved user interface layout with modern styling."""

        # LEFT CONTROL PANEL 
        left_panel = tk.Frame(self.root, bg=COLORS['panel_bg'], padx=15, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Title with icon
        title_frame = tk.Frame(left_panel, bg=COLORS['panel_bg'])
        title_frame.pack(pady=(0, 20))
        
        title = tk.Label(title_frame, text="🚨 Emergency Network",
                        font=("Segoe UI", 18, "bold"), 
                        fg=COLORS['primary'], bg=COLORS['panel_bg'])
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Interactive Simulator",
                           font=("Segoe UI", 10), 
                           fg=COLORS['edge_default'], bg=COLORS['panel_bg'])
        subtitle.pack()

        # Path Selection Frame
        path_frame = tk.LabelFrame(left_panel, text="📍 Route Selection", 
                                   font=("Segoe UI", 11, "bold"),
                                   fg=COLORS['dark'], bg=COLORS['light'],
                                   padx=10, pady=10)
        path_frame.pack(fill=tk.X, pady=10)

        # Source city selection
        tk.Label(path_frame, text="Source City:", font=("Segoe UI", 10),
                bg=COLORS['light'], fg=COLORS['dark']).pack(anchor=tk.W)
        self.source_var = tk.StringVar()
        city_values = [f"{node} - {self.network.get_city_name(node)}" for node in self.network.get_nodes()]
        self.source_combo = ttk.Combobox(path_frame, textvariable=self.source_var,
                                         values=city_values, state="readonly", width=25)
        self.source_combo.pack(fill=tk.X, pady=(2, 8))

        # Target city selection
        tk.Label(path_frame, text="Destination City:", font=("Segoe UI", 10),
                bg=COLORS['light'], fg=COLORS['dark']).pack(anchor=tk.W)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(path_frame, textvariable=self.target_var,
                                         values=city_values, state="readonly", width=25)
        self.target_combo.pack(fill=tk.X, pady=2)

        # Algorithms Section 
        algo_frame = tk.LabelFrame(left_panel, text="🔧 Network Algorithms", 
                                   font=("Segoe UI", 11, "bold"),
                                   fg=COLORS['dark'], bg=COLORS['light'],
                                   padx=10, pady=10)
        algo_frame.pack(fill=tk.X, pady=8)

        self._create_button(algo_frame, "🌲 Q1: Compute MST (Kruskal)", 
                           self._on_mst_click, COLORS['success'])
        self._create_button(algo_frame, "🛤️ Q2: Find Reliable Paths", 
                           self._on_reliable_path_click, COLORS['primary'])
        self._create_button(algo_frame, "🎨 Bonus: Graph Coloring", 
                           self._on_coloring_click, COLORS['secondary'])

        # BST Section
        bst_frame = tk.LabelFrame(left_panel, text="🌳 Command Hierarchy (BST)", 
                                  font=("Segoe UI", 11, "bold"),
                                  fg=COLORS['dark'], bg=COLORS['light'],
                                  padx=10, pady=10)
        bst_frame.pack(fill=tk.X, pady=8)

        self._create_button(bst_frame, "⚡ Q3: Optimize BST (DSW)", 
                           self._on_bst_click, COLORS['warning'])

        # Failure Section
        failure_frame = tk.LabelFrame(left_panel, text="⚠️ Failure Simulation", 
                                      font=("Segoe UI", 11, "bold"),
                                      fg=COLORS['dark'], bg=COLORS['light'],
                                      padx=10, pady=10)
        failure_frame.pack(fill=tk.X, pady=8)

        self._create_button(failure_frame, "💥 Q4: Simulate Node Failure", 
                           self._on_failure_click, COLORS['danger'])
        self._create_button(failure_frame, "🔄 Reset Simulator", 
                           self._on_reset_click, COLORS['edge_default'])

        # Road Management Section
        road_frame = tk.LabelFrame(left_panel, text="🚧 Road Management", 
                                   font=("Segoe UI", 11, "bold"),
                                   fg=COLORS['dark'], bg=COLORS['light'],
                                   padx=10, pady=10)
        road_frame.pack(fill=tk.X, pady=8)

        self._create_button(road_frame, "⚠️ Mark Road Vulnerable", 
                           self._on_mark_vulnerable_click, COLORS['danger'])
        self._create_button(road_frame, "✅ Unmark Vulnerable Road", 
                           self._on_unmark_vulnerable_click, COLORS['success'])

        # Status Box with modern styling
        status_frame = tk.LabelFrame(left_panel, text="📊 System Status", 
                                     font=("Segoe UI", 11, "bold"),
                                     fg=COLORS['dark'], bg=COLORS['light'],
                                     padx=8, pady=8)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=8)

        self.status_area = tk.Text(status_frame, height=12, width=32,
                                   bg=COLORS['status_bg'], fg=COLORS['dark'],
                                   font=("Consolas", 9),
                                   relief=tk.FLAT, borderwidth=0, padx=10, pady=10)
        self.status_area.pack(fill=tk.BOTH, expand=True)
        
        # Initial status message
        self.status_area.insert(1.0, "🟢 System Ready\n\n" +
                                "Welcome to Emergency Network!\n\n" +
                                "• Select source & destination\n" +
                                "• Use algorithms to analyze\n" +
                                "• Double-click to add nodes\n" +
                                "• Shift+click to mark roads\n" +
                                "• Drag nodes to reposition")

        # RIGHT CANVAS PANEL with gradient-like header
        canvas_panel = tk.Frame(self.root, bg=COLORS['panel_bg'], padx=10, pady=10)
        canvas_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Canvas header
        header_frame = tk.Frame(canvas_panel, bg=COLORS['primary'], padx=15, pady=8)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        canvas_title = tk.Label(header_frame, text="🗺️ Network Visualization",
                               font=("Segoe UI", 14, "bold"),
                               fg=COLORS['white'], bg=COLORS['primary'])
        canvas_title.pack()

        # Canvas with rounded corners effect (using frame border)
        canvas_container = tk.Frame(canvas_panel, bg=COLORS['dark'], padx=2, pady=2)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_container, bg=COLORS['canvas_bg'], 
                               cursor="hand2", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events
        self.canvas.bind("<Button-3>", self._on_canvas_rightclick)
        self.canvas.bind("<Double-Button-1>", self._on_canvas_doubleclick)
        self.canvas.bind("<Shift-Button-1>", self._on_canvas_mark_vulnerable)
        
        # Drag events for nodes
        self.canvas.bind("<Button-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_release)
    
    def _create_button(self, parent, text, command, color):
        """Create a modern styled button."""
        btn = tk.Button(parent, text=text, command=command,
                       font=("Segoe UI", 9, "bold"),
                       fg=COLORS['white'], bg=color,
                       activebackground=COLORS['dark'],
                       activeforeground=COLORS['white'],
                       relief=tk.FLAT, cursor="hand2",
                       padx=15, pady=8)
        btn.pack(fill=tk.X, pady=4)
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS['dark']))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        return btn
    
    def _draw_canvas(self):
        """Draw network on canvas with city names."""
        self.canvas.delete("all")
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        # Scale positions
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        def transform(x, y):
            tx = 80 + (x - x_min) / x_range * (width - 160)
            ty = 80 + (y - y_min) / y_range * (height - 160)
            return tx, ty
        
        # Draw title on canvas
        self.canvas.create_text(width // 2, 25, text="🚨 Interactive Emergency Network Simulator",
                               font=("Segoe UI", 14, "bold"), fill=COLORS['primary'])
        
        # Draw legend
        self._draw_legend(width, height)
        
        # Draw edges with modern styling
        for u, v, data in self.network.graph.edges(data=True):
            x1, y1 = transform(self.pos[u][0], self.pos[u][1])
            x2, y2 = transform(self.pos[v][0], self.pos[v][1])
            
            if u in self.network.get_disabled_nodes() or v in self.network.get_disabled_nodes():
                edge_color = COLORS['edge_default']
                dash_pattern = (8, 8)
                edge_width = 2
            elif self.network.is_edge_vulnerable(u, v):
                edge_color = COLORS['edge_vulnerable']
                dash_pattern = (6, 4)
                edge_width = 3
            elif (u, v) in self.mst_edges or (v, u) in self.mst_edges:
                edge_color = COLORS['edge_mst']
                dash_pattern = ()
                edge_width = 4
            elif [u, v] in self.path1_edges or [v, u] in self.path1_edges:
                edge_color = COLORS['edge_path1']
                dash_pattern = ()
                edge_width = 5
            elif [u, v] in self.path2_edges or [v, u] in self.path2_edges:
                edge_color = COLORS['edge_path2']
                dash_pattern = ()
                edge_width = 5
            else:
                edge_color = COLORS['edge_default']
                dash_pattern = ()
                edge_width = 2
            
            self.canvas.create_line(x1, y1, x2, y2, fill=edge_color, 
                                   width=edge_width, dash=dash_pattern,
                                   capstyle=tk.ROUND)
            
            # Draw edge weight with background
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_oval(mx-12, my-10, mx+12, my+10, 
                                   fill=COLORS['white'], outline=COLORS['edge_default'])
            self.canvas.create_text(mx, my, text=str(data['weight']), 
                                   fill=COLORS['danger'], font=("Segoe UI", 9, "bold"))
        
        # Draw nodes with city names
        node_radius = 28
        for node in self.network.get_nodes():
            x, y = transform(self.pos[node][0], self.pos[node][1])
            city_name = self.network.get_city_name(node)
            
            if node in self.network.get_disabled_nodes():
                node_color = COLORS['node_disabled']
                outline_color = COLORS['danger']
            else:
                node_color = COLORS['node_default']
                outline_color = COLORS['primary']
            
            # Draw node shadow
            self.canvas.create_oval(x-node_radius+3, y-node_radius+3, 
                                   x+node_radius+3, y+node_radius+3, 
                                   fill='#d1d5db', outline='')
            
            # Draw node circle
            self.canvas.create_oval(x-node_radius, y-node_radius, 
                                   x+node_radius, y+node_radius, 
                                   fill=node_color, outline=outline_color, width=3)
            
            # Draw node ID
            self.canvas.create_text(x, y-6, text=str(node), 
                                   font=("Segoe UI", 11, "bold"), fill=COLORS['dark'])
            
            # Draw city name below node
            self.canvas.create_text(x, y+node_radius+12, text=city_name,
                                   font=("Segoe UI", 9, "bold"), fill=COLORS['dark'])
    
    def _draw_legend(self, width, height):
        """Draw a legend on the canvas."""
        legend_x = width - 145
        legend_y = 60
        
        # Legend background with shadow effect
        self.canvas.create_rectangle(legend_x - 12, legend_y - 22, 
                                    legend_x + 133, legend_y + 133,
                                    fill='#e5e7eb', outline='')
        self.canvas.create_rectangle(legend_x - 15, legend_y - 25, 
                                    legend_x + 130, legend_y + 130,
                                    fill=COLORS['white'], outline=COLORS['primary'], width=2)
        
        self.canvas.create_text(legend_x + 57, legend_y - 8, text="🗺️ LEGEND",
                               font=("Segoe UI", 10, "bold"), fill=COLORS['dark'])
        
        # Define legend items with their styles (color, label, dashed)
        legend_items = [
            (COLORS['edge_mst'], "MST Edge", False),
            (COLORS['edge_path1'], "Primary (Green)", False),
            (COLORS['edge_path2'], "Backup (Orange)", False),
            (COLORS['edge_vulnerable'], "Dangerous Road", False),
        ]
        
        for i, (color, label, is_dashed) in enumerate(legend_items):
            y_pos = legend_y + 18 + i * 28
            dash = (6, 4) if is_dashed else ()
            self.canvas.create_line(legend_x, y_pos, legend_x + 35, y_pos, 
                                   fill=color, width=4, dash=dash)
            self.canvas.create_text(legend_x + 45, y_pos, text=label,
                                   font=("Segoe UI", 9), anchor="w", fill=COLORS['dark'])
    
    def _on_mst_click(self):
        """Handle MST computation with city names."""
        edges, weight = self.network.compute_mst()
        self.mst_edges = edges
        self.status_area.delete(1.0, tk.END)
        
        # Build detailed MST info with city names
        text = "🌲 MINIMUM SPANNING TREE (Kruskal)\n"
        text += "━" * 35 + "\n\n"
        text += f"✅ Total Weight: {weight}\n"
        text += f"📊 Edges in MST: {len(edges)}\n\n"
        text += "Connected Routes:\n"
        text += "─" * 35 + "\n"
        
        for u, v in edges:
            city_u = self.network.get_city_name(u)
            city_v = self.network.get_city_name(v)
            w = self.network.graph[u][v]['weight']
            text += f"  {city_u} ↔ {city_v} ({w}km)\n"
        
        self.status_area.insert(1.0, text)
        self._draw_canvas()
    
    def _on_reliable_path_click(self):
        """Handle reliable path finding with disjoint paths and city names."""
        try:
            src_text = self.source_var.get()
            tgt_text = self.target_var.get()
            
            # Extract node ID from "ID - CityName" format
            src = int(src_text.split(" - ")[0]) if " - " in src_text else int(src_text)
            tgt = int(tgt_text.split(" - ")[0]) if " - " in tgt_text else int(tgt_text)
            
            # Find disjoint paths (most reliable approach)
            path1, path2, found = self.path_finder.find_disjoint_paths(src, tgt)
            
            self.status_area.delete(1.0, tk.END)
            if path1:
                # Calculate path weights
                path1_weight = sum(self.network.graph[path1[i]][path1[i+1]]['weight'] for i in range(len(path1)-1))
                path1_cities = [self.network.get_city_name(n) for n in path1]
                path1_str = ' → '.join(path1_cities)
                
                text = "🛤️ RELIABLE PATH FINDER\n"
                text += "━" * 35 + "\n\n"
                text += "� PRIMARY ROUTE:\n"
                text += f"   {path1_str}\n"
                text += f"   Distance: {path1_weight} km\n\n"
                
                # Store path1 edges
                self.path1_edges = [[path1[i], path1[i+1]] for i in range(len(path1)-1)]
                self.path2_edges = []  # Clear path2
                
                if path2:
                    path2_weight = sum(self.network.graph[path2[i]][path2[i+1]]['weight'] for i in range(len(path2)-1))
                    path2_cities = [self.network.get_city_name(n) for n in path2]
                    path2_str = ' → '.join(path2_cities)
                    
                    text += "� BACKUP ROUTE:\n"
                    text += f"   {path2_str}\n"
                    text += f"   Distance: {path2_weight} km\n\n"
                    text += "─" * 35 + "\n"
                    text += "✅ Both routes are edge-disjoint\n"
                    text += "   (No shared roads)\n"
                    self.path2_edges = [[path2[i], path2[i+1]] for i in range(len(path2)-1)]
                else:
                    text += "⚠️ Only 1 reliable path available\n"
                
                self.status_area.insert(1.0, text)
                self._draw_canvas()
            else:
                self.status_area.insert(1.0, "❌ No path found between selected cities")
        except Exception as e:
            messagebox.showerror("Error", f"Path finding failed: {str(e)}\n\nPlease select valid source and destination cities.")
    
    def _on_bst_click(self):
        """Handle BST optimization with network-style visualization."""
        # Get info before optimization
        info_before = self.bst_viz.get_bst_info()
        height_before = info_before['height']
        
        # Optimize BST
        self.bst_viz.optimize_bst()
        
        # Get info after optimization
        info_after = self.bst_viz.get_bst_info()
        height_after = self._get_bst_height(self.bst_viz.optimized_bst)
        
        # Update status with enhanced styling
        self.status_area.delete(1.0, tk.END)
        text = "⚡ COMMAND HIERARCHY OPTIMIZER\n"
        text += "━" * 35 + "\n\n"
        text += "📊 BEFORE Optimization:\n"
        text += f"   Tree Height: {height_before}\n"
        text += f"   Total Commands: {info_before['nodes']}\n\n"
        text += "✅ AFTER DSW Rebalancing:\n"
        text += f"   Tree Height: {height_after}\n"
        text += f"   Total Commands: {info_after['nodes']}\n\n"
        text += "─" * 35 + "\n"
        text += "📌 Algorithm: DSW (Day-Stout-Warren)\n"
        text += "🎯 Purpose: Minimize longest path\n"
        text += "   from HQ to any command unit"
        
        self.status_area.insert(1.0, text)
        
        # Visualize BST on canvas with network-style nodes
        self._draw_bst_comparison()
    
    def _get_bst_height(self, node):
        """Get height of BST node."""
        if node is None:
            return 0
        left_height = self._get_bst_height(node.get('left'))
        right_height = self._get_bst_height(node.get('right'))
        return 1 + max(left_height, right_height)
    
    def _draw_bst_comparison(self):
        """Draw before/after BST comparison with network-style nodes."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        # Calculate heights
        height_before = self._get_bst_height(self.bst_viz.bst)
        height_after = self._get_bst_height(self.bst_viz.optimized_bst)
        
        # Draw main title
        self.canvas.create_text(width // 2, 20, text="🌳 BST Rebalancing - Command Hierarchy Optimization", 
                               font=("Segoe UI", 16, "bold"), fill=COLORS['primary'])
        
        # Draw "BEFORE" section
        before_x = width // 4
        self.canvas.create_text(before_x, 50, text=f"❌ BEFORE (Height: {height_before})", 
                               font=("Segoe UI", 13, "bold"), fill=COLORS['danger'])
        self.canvas.create_rectangle(15, 70, width // 2 - 15, height - 50, 
                                    outline=COLORS['danger'], width=3, dash=(5, 3))
        self._draw_bst_tree_network_style(self.bst_viz.bst, before_x, 120, width // 6, 
                                          is_optimized=False, section_height=height - 180)
        
        # Draw "AFTER" section
        after_x = 3 * width // 4
        self.canvas.create_text(after_x, 50, text=f"✅ AFTER Optimized (Height: {height_after})", 
                               font=("Segoe UI", 13, "bold"), fill=COLORS['success'])
        self.canvas.create_rectangle(width // 2 + 15, 70, width - 15, height - 50, 
                                    outline=COLORS['success'], width=3, dash=(5, 3))
        if self.bst_viz.optimized_bst:
            self._draw_bst_tree_network_style(self.bst_viz.optimized_bst, after_x, 120, width // 6,
                                              is_optimized=True, section_height=height - 180)
        
        # Draw improvement stats at bottom
        improvement = ((height_before - height_after) / height_before * 100) if height_before > 0 else 0
        stats_text = f"📈 Height Reduction: {height_before} → {height_after} (↓{improvement:.0f}%) | Max Hops: {height_before} → {height_after}"
        self.canvas.create_text(width // 2, height - 25, text=stats_text, 
                               font=("Segoe UI", 11, "bold"), fill=COLORS['info'])
    
    def _draw_bst_tree_network_style(self, node, x, y, x_offset, is_optimized=False, 
                                      section_height=500, depth=0):
        """Draw BST tree with network-style nodes (like the main graph)."""
        if node is None:
            return
        
        # Get command name for this node
        cmd_name = COMMAND_NAMES.get(node['root'], f"Cmd-{node['root']}")
        
        # Colors based on optimization state and depth
        if is_optimized:
            base_colors = [COLORS['node_highlight'], '#6ee7b7', '#a7f3d0', '#d1fae5']
            outline_color = COLORS['success']
        else:
            base_colors = [COLORS['node_disabled'], '#fca5a5', '#fecaca', '#fee2e2']
            outline_color = COLORS['danger']
        
        node_color = base_colors[min(depth, len(base_colors) - 1)]
        
        # Node dimensions (network style)
        node_radius = 28
        
        # Draw node shadow
        self.canvas.create_oval(x - node_radius + 3, y - node_radius + 3,
                               x + node_radius + 3, y + node_radius + 3,
                               fill='#d1d5db', outline='')
        
        # Draw node circle (network style)
        self.canvas.create_oval(x - node_radius, y - node_radius,
                               x + node_radius, y + node_radius,
                               fill=node_color, outline=outline_color, width=3)
        
        # Draw command name
        self.canvas.create_text(x, y - 5, text=cmd_name, 
                               font=("Segoe UI", 9, "bold"), fill=COLORS['dark'])
        
        # Draw node value (priority)
        self.canvas.create_text(x, y + 10, text=f"P:{node['root']}", 
                               font=("Segoe UI", 7), fill=COLORS['edge_default'])
        
        # Draw depth indicator
        depth_indicator = f"L{depth}"
        self.canvas.create_text(x, y + node_radius + 12, text=depth_indicator,
                               font=("Segoe UI", 8), fill=COLORS['info'])
        
        # Draw edges and recurse
        y_offset = 85
        x_offset_new = max(x_offset // 2, 50)
        
        if node.get('left'):
            left_x = x - x_offset_new
            left_y = y + y_offset
            # Draw edge line
            self.canvas.create_line(x, y + node_radius, left_x, left_y - node_radius,
                                   fill=outline_color, width=2)
            self._draw_bst_tree_network_style(node['left'], left_x, left_y, x_offset_new,
                                               is_optimized, section_height, depth + 1)
        
        if node.get('right'):
            right_x = x + x_offset_new
            right_y = y + y_offset
            # Draw edge line
            self.canvas.create_line(x, y + node_radius, right_x, right_y - node_radius,
                                   fill=outline_color, width=2)
            self._draw_bst_tree_network_style(node['right'], right_x, right_y, x_offset_new,
                                               is_optimized, section_height, depth + 1)
    
    def _on_failure_click(self):
        """Handle node failure simulation with city names."""
        try:
            # Create a custom dialog with city names
            dialog = tk.Toplevel(self.root)
            dialog.title("💥 Simulate Node Failure")
            dialog.geometry("350x200")
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.configure(bg=COLORS['light'])
            
            tk.Label(dialog, text="Select City to Disable:", 
                    font=("Segoe UI", 12, "bold"),
                    bg=COLORS['light'], fg=COLORS['dark']).pack(pady=15)
            
            # Dropdown with city names
            city_var = tk.StringVar()
            city_values = [f"{node} - {self.network.get_city_name(node)}" 
                          for node in self.network.get_nodes() 
                          if node not in self.network.get_disabled_nodes()]
            
            city_combo = ttk.Combobox(dialog, textvariable=city_var,
                                      values=city_values, state="readonly", width=30)
            city_combo.pack(pady=10)
            
            def disable_city():
                try:
                    selection = city_var.get()
                    node = int(selection.split(" - ")[0])
                    city_name = self.network.get_city_name(node)
                    
                    if self.network.disable_node(node):
                        self.status_area.delete(1.0, tk.END)
                        text = f"💥 NODE FAILURE SIMULATED\n"
                        text += "━" * 35 + "\n\n"
                        text += f"❌ {city_name} (Node {node}) OFFLINE\n\n"
                        text += "System is rerouting traffic...\n"
                        text += "Consider finding alternate paths."
                        self.status_area.insert(1.0, text)
                        self._draw_canvas()
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to disable node: {str(e)}")
            
            btn = tk.Button(dialog, text="🔴 Disable City",
                           command=disable_city,
                           font=("Segoe UI", 10, "bold"),
                           fg=COLORS['white'], bg=COLORS['danger'],
                           relief=tk.FLAT, padx=20, pady=8)
            btn.pack(pady=20)
        except:
            pass
    
    def _on_coloring_click(self):
        """Handle graph coloring with visualization and city names."""
        # Apply graph coloring algorithm
        colors = GraphColorer.color_graph(self.network.graph)
        num_colors = len(set(colors.values()))
        
        # Store colors for visualization
        self.node_colors = colors
        
        # Update status area with detailed information
        self.status_area.delete(1.0, tk.END)
        text = "🎨 GRAPH COLORING\n"
        text += "━" * 35 + "\n"
        text += "Frequency Assignment Algorithm\n\n"
        text += f"📊 Algorithm: Welsh-Powell\n"
        text += f"🎯 Colors Used: {num_colors}\n"
        text += f"📡 Total Hubs: {len(self.network.get_nodes())}\n\n"
        text += "FREQUENCY ASSIGNMENTS:\n"
        text += "─" * 35 + "\n"
        
        # Create color name mapping
        color_names = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Cyan"]
        
        # Sort nodes by color for better display
        sorted_by_color = sorted(colors.items(), key=lambda x: x[1])
        
        for node, color_idx in sorted_by_color:
            city_name = self.network.get_city_name(node)
            color_name = color_names[color_idx] if color_idx < len(color_names) else f"Color{color_idx}"
            text += f"  {city_name}: F{color_idx + 1} ({color_name})\n"
        
        text += f"\n{'─'*35}\n"
        text += "✅ No adjacent cities share frequency\n"
        text += "🔊 Interference-free communication!"
        
        self.status_area.insert(1.0, text)
        
        # Visualize coloring on canvas
        self._draw_colored_graph(colors, color_names)
    
    def _draw_colored_graph(self, colors, color_names):
        """Draw the graph with node coloring on canvas with city names."""
        self.canvas.delete("all")
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        # Scale positions
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        def transform(x, y):
            tx = 80 + (x - x_min) / x_range * (width - 200)
            ty = 80 + (y - y_min) / y_range * (height - 160)
            return tx, ty
        
        # Draw title
        self.canvas.create_text(width // 2, 25, text="🎨 Graph Coloring: Frequency Assignment",
                               font=("Segoe UI", 16, "bold"), fill=COLORS['primary'])
        
        # Color palette for visualization (modern colors)
        color_palette = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#f97316", "#06b6d4"]
        
        # Draw edges first
        for u, v, data in self.network.graph.edges(data=True):
            x1, y1 = transform(self.pos[u][0], self.pos[u][1])
            x2, y2 = transform(self.pos[v][0], self.pos[v][1])
            self.canvas.create_line(x1, y1, x2, y2, fill=COLORS['edge_default'], width=2)
            
            # Draw edge weight
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_oval(mx-10, my-8, mx+10, my+8, 
                                   fill=COLORS['white'], outline=COLORS['edge_default'])
            self.canvas.create_text(mx, my, text=str(data['weight']), 
                                   fill=COLORS['edge_default'], font=("Segoe UI", 8))
        
        # Draw nodes with assigned colors and city names
        node_radius = 28
        for node in self.network.get_nodes():
            x, y = transform(self.pos[node][0], self.pos[node][1])
            city_name = self.network.get_city_name(node)
            color_idx = colors.get(node, 0)
            node_color = color_palette[color_idx % len(color_palette)]
            
            # Draw node shadow
            self.canvas.create_oval(x - node_radius + 3, y - node_radius + 3,
                                   x + node_radius + 3, y + node_radius + 3,
                                   fill='#d1d5db', outline='')
            
            # Draw node circle
            self.canvas.create_oval(x - node_radius, y - node_radius,
                                   x + node_radius, y + node_radius,
                                   fill=node_color, outline=COLORS['dark'], width=2)
            
            # Draw city name
            self.canvas.create_text(x, y - 5, text=city_name[:8], 
                                   font=("Segoe UI", 8, "bold"), fill="white")
            
            # Draw frequency number
            freq_num = color_idx + 1
            self.canvas.create_text(x, y + 10, text=f"F{freq_num}", 
                                   font=("Segoe UI", 9, "bold"), fill="white")
        
        # Draw legend
        legend_x = width - 140
        legend_y = 70
        
        # Legend background
        self.canvas.create_rectangle(legend_x - 15, legend_y - 30,
                                    legend_x + 125, legend_y + len(set(colors.values())) * 28 + 10,
                                    fill=COLORS['white'], outline=COLORS['edge_default'], width=1)
        
        self.canvas.create_text(legend_x + 55, legend_y - 15, text="FREQUENCIES",
                               font=("Segoe UI", 10, "bold"), fill=COLORS['dark'])
        
        for idx in range(min(len(set(colors.values())), len(color_palette))):
            color = color_palette[idx]
            color_name = color_names[idx] if idx < len(color_names) else f"Color{idx}"
            
            # Color sample circle
            self.canvas.create_oval(legend_x, legend_y + idx * 28,
                                   legend_x + 20, legend_y + 20 + idx * 28,
                                   fill=color, outline=COLORS['dark'], width=1)
            
            # Label
            self.canvas.create_text(legend_x + 30, legend_y + 10 + idx * 28,
                                   text=f"F{idx + 1}: {color_name}",
                                   font=("Segoe UI", 9), anchor="w", fill=COLORS['dark'])
    
    def _on_reset_click(self):
        """Reset simulator with enhanced feedback."""
        self.network = NetworkGraph()
        self.path_finder = PathFinder(self.network.graph, self.network.vulnerable_edges)
        self.selected_paths = []
        self.mst_edges = []
        self.path1_edges = []
        self.path2_edges = []
        self.pos = self.network.get_node_positions()
        
        # Update city dropdowns
        city_values = [f"{node} - {self.network.get_city_name(node)}" for node in self.network.get_nodes()]
        self.source_combo['values'] = city_values
        self.target_combo['values'] = city_values
        self.source_var.set('')
        self.target_var.set('')
        
        self.status_area.delete(1.0, tk.END)
        text = "🔄 SIMULATOR RESET\n"
        text += "━" * 35 + "\n\n"
        text += "✅ Network restored to default\n"
        text += "✅ All paths cleared\n"
        text += "✅ All nodes active\n\n"
        text += "Ready for new simulations!"
        self.status_area.insert(1.0, text)
        self._draw_canvas()
    
    def _on_mark_vulnerable_click(self):
        """Mark an edge as vulnerable with city names."""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("⚠️ Mark Road as Vulnerable")
            dialog.geometry("350x220")
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.configure(bg=COLORS['light'])
            
            tk.Label(dialog, text="Select Road to Mark Dangerous:", 
                    font=("Segoe UI", 11, "bold"),
                    bg=COLORS['light'], fg=COLORS['dark']).pack(pady=10)
            
            city_values = [f"{node} - {self.network.get_city_name(node)}" for node in self.network.get_nodes()]
            
            tk.Label(dialog, text="From City:", font=("Segoe UI", 10),
                    bg=COLORS['light']).pack()
            node1_var = tk.StringVar()
            ttk.Combobox(dialog, textvariable=node1_var, values=city_values, 
                        state="readonly", width=28).pack(pady=5)
            
            tk.Label(dialog, text="To City:", font=("Segoe UI", 10),
                    bg=COLORS['light']).pack()
            node2_var = tk.StringVar()
            ttk.Combobox(dialog, textvariable=node2_var, values=city_values,
                        state="readonly", width=28).pack(pady=5)
            
            def mark_edge():
                try:
                    u = int(node1_var.get().split(" - ")[0])
                    v = int(node2_var.get().split(" - ")[0])
                    
                    if self.network.graph.has_edge(u, v):
                        self.network.mark_vulnerable_edge(u, v)
                        city_u = self.network.get_city_name(u)
                        city_v = self.network.get_city_name(v)
                        self.status_area.delete(1.0, tk.END)
                        text = f"⚠️ ROAD MARKED VULNERABLE\n"
                        text += "━" * 35 + "\n\n"
                        text += f"🚧 {city_u} ↔ {city_v}\n\n"
                        text += "This road will be avoided\n"
                        text += "when finding reliable paths."
                        self.status_area.insert(1.0, text)
                        self._draw_canvas()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", f"No direct road between these cities")
                except Exception as e:
                    messagebox.showerror("Error", "Please select valid cities")
            
            btn = tk.Button(dialog, text="🚧 Mark as Vulnerable", command=mark_edge,
                           font=("Segoe UI", 10, "bold"),
                           fg=COLORS['white'], bg=COLORS['danger'],
                           relief=tk.FLAT, padx=20, pady=8)
            btn.pack(pady=15)
        except:
            pass
    
    def _on_unmark_vulnerable_click(self):
        """Unmark a vulnerable edge with city names."""
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("✅ Unmark Vulnerable Road")
            dialog.geometry("350x220")
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.configure(bg=COLORS['light'])
            
            tk.Label(dialog, text="Select Road to Restore:", 
                    font=("Segoe UI", 11, "bold"),
                    bg=COLORS['light'], fg=COLORS['dark']).pack(pady=10)
            
            # Show only vulnerable edges
            vulnerable_roads = []
            for u, v in self.network.get_vulnerable_edges():
                city_u = self.network.get_city_name(u)
                city_v = self.network.get_city_name(v)
                vulnerable_roads.append(f"{u}-{v}: {city_u} ↔ {city_v}")
            
            if not vulnerable_roads:
                tk.Label(dialog, text="No vulnerable roads to unmark", 
                        font=("Segoe UI", 10),
                        bg=COLORS['light'], fg=COLORS['edge_default']).pack(pady=30)
                return
            
            tk.Label(dialog, text="Vulnerable Road:", font=("Segoe UI", 10),
                    bg=COLORS['light']).pack()
            road_var = tk.StringVar()
            ttk.Combobox(dialog, textvariable=road_var, values=vulnerable_roads,
                        state="readonly", width=28).pack(pady=10)
            
            def unmark_edge():
                try:
                    selection = road_var.get()
                    edge_part = selection.split(":")[0]
                    u, v = map(int, edge_part.split("-"))
                    
                    self.network.unmark_vulnerable_edge(u, v)
                    city_u = self.network.get_city_name(u)
                    city_v = self.network.get_city_name(v)
                    self.status_area.delete(1.0, tk.END)
                    text = f"✅ ROAD RESTORED\n"
                    text += "━" * 35 + "\n\n"
                    text += f"🛣️ {city_u} ↔ {city_v}\n\n"
                    text += "Road is now safe for routing."
                    self.status_area.insert(1.0, text)
                    self._draw_canvas()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", "Please select a road")
            
            btn = tk.Button(dialog, text="✅ Restore Road", command=unmark_edge,
                           font=("Segoe UI", 10, "bold"),
                           fg=COLORS['white'], bg=COLORS['success'],
                           relief=tk.FLAT, padx=20, pady=8)
            btn.pack(pady=15)
        except:
            pass
    
    def _on_canvas_doubleclick(self, event):
        """Handle double-click on canvas to add new node with city name."""
        # Check if clicking on an existing node - if so, don't add new node
        existing_node = self._get_node_at_position(event.x, event.y)
        if existing_node is not None:
            # Clicked on existing node, show info instead
            city_name = self.network.get_city_name(existing_node)
            self.status_area.delete(1.0, tk.END)
            text = f"📍 NODE INFO\n"
            text += "━" * 35 + "\n\n"
            text += f"🏙️ {city_name} (Node {existing_node})\n\n"
            text += "To add a new city, double-click\non an empty area of the canvas."
            self.status_area.insert(1.0, text)
            return
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        # Inverse transform to get graph coordinates
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        # Convert click coordinates back to graph space
        graph_x = x_min + (event.x - 80) / (width - 160) * x_range
        graph_y = y_min + (event.y - 80) / (height - 160) * y_range
        
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
            
            # Generate a new city name
            new_city_names = ["Gujranwala", "Sialkot", "Hyderabad", "Sukkur", "Bahawalpur", 
                            "Sargodha", "Abbottabad", "Mardan", "Gwadar", "Zhob"]
            new_city_name = new_city_names[new_node % len(new_city_names)] if new_node not in CITY_NAMES else f"City-{new_node}"
            self.network.city_names[new_node] = new_city_name
            
            # Add node and edge to graph
            self.network.graph.add_node(new_node)
            self.network.graph.add_edge(nearest_node, new_node, weight=edge_weight)
            
            # Add position for new node
            self.pos[new_node] = (graph_x, graph_y)
            
            # Update path finder with new graph
            self.path_finder = PathFinder(self.network.graph, self.network.vulnerable_edges)
            
            # Update dropdown menus with new node
            city_values = [f"{node} - {self.network.get_city_name(node)}" for node in self.network.get_nodes()]
            self.source_combo['values'] = city_values
            self.target_combo['values'] = city_values
            
            # Update UI
            nearest_city = self.network.get_city_name(nearest_node)
            self.status_area.delete(1.0, tk.END)
            text = f"🏙️ NEW CITY ADDED\n"
            text += "━" * 35 + "\n\n"
            text += f"📍 {new_city_name} (Node {new_node})\n\n"
            text += f"Connected to: {nearest_city}\n"
            text += f"Distance: {edge_weight} km"
            self.status_area.insert(1.0, text)
            self._draw_canvas()
    
    def _on_canvas_mark_vulnerable(self, event):
        """Handle Shift+Click to mark/unmark vulnerable roads."""
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        # Transform canvas coordinates to graph space
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        graph_x = x_min + (event.x - 80) / (width - 160) * x_range
        graph_y = y_min + (event.y - 80) / (height - 160) * y_range
        
        # Find nearest edge to click
        nearest_edge = None
        min_dist = float('inf')
        threshold = 0.15
        
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
            city_u = self.network.get_city_name(u)
            city_v = self.network.get_city_name(v)
            
            # Toggle vulnerable status
            if self.network.is_edge_vulnerable(u, v):
                self.network.unmark_vulnerable_edge(u, v)
                status = f"✅ ROAD RESTORED\n━" + "━" * 34 + f"\n\n🛣️ {city_u} ↔ {city_v}\n\nRoad is now safe for routing."
            else:
                self.network.mark_vulnerable_edge(u, v)
                status = f"⚠️ ROAD MARKED VULNERABLE\n━" + "━" * 34 + f"\n\n🚧 {city_u} ↔ {city_v}\n\nThis road will be avoided."
            
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
    
    def _get_node_at_position(self, event_x, event_y):
        """Find node at given canvas position."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        node_radius = 28
        
        for node in self.network.get_nodes():
            # Transform graph coords to canvas coords
            canvas_x = 80 + (self.pos[node][0] - x_min) / x_range * (width - 160)
            canvas_y = 80 + (self.pos[node][1] - y_min) / y_range * (height - 160)
            
            # Check if click is within node radius
            dist = math.sqrt((event_x - canvas_x)**2 + (event_y - canvas_y)**2)
            if dist <= node_radius:
                return node
        return None
    
    def _on_drag_start(self, event):
        """Handle mouse press for dragging."""
        node = self._get_node_at_position(event.x, event.y)
        if node is not None:
            self.dragging_node = node
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.canvas.configure(cursor="fleur")  # Change cursor to move cursor
    
    def _on_drag_motion(self, event):
        """Handle mouse drag motion."""
        if self.dragging_node is None:
            return
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 100 or height < 100:
            width, height = 750, 700
        
        x_coords = [self.pos[node][0] for node in self.network.get_nodes()]
        y_coords = [self.pos[node][1] for node in self.network.get_nodes()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_range = x_max - x_min if x_max > x_min else 1
        y_range = y_max - y_min if y_max > y_min else 1
        
        # Convert canvas coordinates to graph coordinates
        new_graph_x = x_min + (event.x - 80) / (width - 160) * x_range
        new_graph_y = y_min + (event.y - 80) / (height - 160) * y_range
        
        # Update node position
        self.pos[self.dragging_node] = (new_graph_x, new_graph_y)
        
        # Redraw canvas
        self._draw_canvas()
    
    def _on_drag_release(self, event):
        """Handle mouse release after dragging."""
        if self.dragging_node is not None:
            city_name = self.network.get_city_name(self.dragging_node)
            self.status_area.delete(1.0, tk.END)
            text = f"📍 NODE REPOSITIONED\n"
            text += "━" * 35 + "\n\n"
            text += f"🏙️ {city_name} moved to new location\n\n"
            text += "Tip: Drag nodes to customize\nyour network layout!"
            self.status_area.insert(1.0, text)
        
        self.dragging_node = None
        self.canvas.configure(cursor="hand2")  # Reset cursor
    
    def _on_canvas_rightclick(self, event):
        """Handle right-click on canvas - show help."""
        self.status_area.delete(1.0, tk.END)
        text = "💡 INTERACTION GUIDE\n"
        text += "━" * 35 + "\n\n"
        text += "🖱️ Drag nodes: Reposition cities\n\n"
        text += "🖱️ Double-click: Add new city\n\n"
        text += "⇧ Shift+click on road:\n"
        text += "   Toggle vulnerable status\n\n"
        text += "📌 Select cities from dropdowns\n"
        text += "   to find routes between them"
        self.status_area.insert(1.0, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorUI(root)
    root.mainloop()
