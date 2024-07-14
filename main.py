import networkx as nx
import heapq
import pygame
import time
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import matplotlib.pyplot as plt

# Global variables for Pygame
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vehicle Animation")

# Global variables for Tkinter
root = tk.Tk()
root.title("GPS Toll-Based System")

# Colors for Pygame
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Positions for points (for demonstration purposes)
positions = {
    'A': (100, 100),
    'B': (300, 100),
    'C': (200, 200),
    'D': (400, 200),
    'E': (100, 300),
    'F': (300, 300),
    'G': (500, 300),
    'H': (200, 400),
    'I': (400, 400),
    'J': (600, 400),
    'K': (100, 500),
    'L': (300, 500),
    'M': (500, 500),
    'N': (200, 600),
    'O': (400, 600)
}

# Vehicle properties for Pygame
vehicle_radius = 10

def create_graph():
    """Create a graph with 15 nodes and predefined edges."""
    G = nx.Graph()
    edges = [
        ('A', 'B', {'weight': 4}), ('A', 'E', {'weight': 5}), ('A', 'C', {'weight': 6}),
        ('B', 'C', {'weight': 2}), ('B', 'F', {'weight': 5}),
        ('C', 'D', {'weight': 3}), ('C', 'F', {'weight': 1}),
        ('D', 'G', {'weight': 3}), ('D', 'I', {'weight': 5}),
        ('E', 'F', {'weight': 2}), ('E', 'H', {'weight': 4}),
        ('F', 'G', {'weight': 2}), ('F', 'L', {'weight': 5}),
        ('G', 'I', {'weight': 2}), ('G', 'M', {'weight': 4}),
        ('H', 'K', {'weight': 3}), ('H', 'N', {'weight': 5}),
        ('I', 'J', {'weight': 4}), ('I', 'O', {'weight': 6}),
        ('J', 'O', {'weight': 5}),
        ('K', 'L', {'weight': 2}),
        ('L', 'M', {'weight': 3}),
        ('N', 'O', {'weight': 4})
    ]
    G.add_edges_from(edges)
    return G

def dijkstra(graph, start, end):
    """Implement Dijkstra's algorithm to find the shortest path."""
    pq = [(0, start)]
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    shortest_path = {}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path, current_node = [], end
    while current_node != start:
        path.insert(0, current_node)
        current_node = shortest_path.get(current_node, start)
    path.insert(0, start)

    return path, distances[end]

def calculate_toll(path, graph, toll_rate_per_km=0.5):
    """Calculate the toll based on the path and toll rate per kilometer."""
    toll = 0
    for i in range(len(path) - 1):
        distance = graph[path[i]][path[i + 1]]['weight']
        toll += distance

    toll *= toll_rate_per_km
    return toll

def animate_vehicle(path, graph):
    """Animate the vehicle along the path using Pygame."""
    global window
    vehicle_pos = positions[path[0]]
    speed = 2

    for i in range(1, len(path)):
        start_pos = positions[path[i - 1]]
        end_pos = positions[path[i]]
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            current_time = time.time()
            elapsed_time = current_time - start_time
            t = min(1, elapsed_time / speed)
            vehicle_pos = (
                start_pos[0] + t * (end_pos[0] - start_pos[0]),
                start_pos[1] + t * (end_pos[1] - start_pos[1])
            )

            window.fill(white)
            for u, v in graph.edges():
                pygame.draw.line(window, black, positions[u], positions[v], 2)
            for node, pos in positions.items():
                pygame.draw.circle(window, black, pos, vehicle_radius)
                font = pygame.font.Font(None, 24)
                text = font.render(node, True, black)
                window.blit(text, (pos[0] - 10, pos[1] - 10))
            pygame.draw.circle(window, red, (int(vehicle_pos[0]), int(vehicle_pos[1])), vehicle_radius)
            pygame.display.update()

            if t >= 1:
                break

def on_calculate():
    """Handle the calculation and animation when the button is pressed."""
    global root, G
    start = start_entry.get()
    end = end_entry.get()
    if start not in G or end not in G:
        messagebox.showerror("Error", "Invalid start or end point")
        return

    path, cost = dijkstra(G, start, end)
    toll = calculate_toll(path, G)
    path_label.config(text=f"Path: {' -> '.join(path)}")
    toll_label.config(text=f"Toll: {toll}")

    animation_thread = Thread(target=animate_vehicle, args=(path, G))
    animation_thread.start()

def show_graph():
    """Display the graph with node names, edge weights, and highlighted shortest path."""
    global G
    start = start_entry.get()
    end = end_entry.get()
    if start not in G or end not in G:
        messagebox.showerror("Error", "Invalid start or end point")
        return

    path, _ = dijkstra(G, start, end)
    draw_graph(G, path)

def draw_graph(G, path):
    """Draw the graph with node names, edge weights, and highlight the shortest path."""
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
    plt.show()

# Tkinter GUI setup
start_label = tk.Label(root, text="Start Point:")
start_label.pack()
start_entry = tk.Entry(root)
start_entry.pack()
end_label = tk.Label(root, text="End Point:")
end_label.pack()
end_entry = tk.Entry(root)
end_entry.pack()
calculate_button = tk.Button(root, text="Calculate Toll", command=on_calculate)
calculate_button.pack()
show_graph_button = tk.Button(root, text="Show Graph", command=show_graph)
show_graph_button.pack()
path_label = tk.Label(root, text="")
path_label.pack()
toll_label = tk.Label(root, text="")
toll_label.pack()

# Create graph
G = create_graph()

# Start Tkinter main loop
root.mainloop()
