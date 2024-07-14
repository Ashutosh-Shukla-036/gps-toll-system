import networkx as nx
import heapq
import pygame
import time
import tkinter as tk
from tkinter import messagebox

# Create a graph
def create_graph():
    G = nx.Graph()
    G.add_edge('A', 'B', weight=4)
    G.add_edge('A', 'C', weight=2)
    G.add_edge('B', 'C', weight=1)
    G.add_edge('B', 'D', weight=5)
    G.add_edge('C', 'D', weight=8)
    G.add_edge('C', 'E', weight=10)
    G.add_edge('D', 'E', weight=2)
    return G

# Dijkstra's algorithm
def dijkstra(graph, start, end):
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

# Calculate toll
def calculate_toll(path, graph, toll_rate_per_km=0.5):
    toll = 0
    for i in range(len(path) - 1):
        toll += graph[path[i]][path[i + 1]]['weight'] * toll_rate_per_km
    return toll

# Pygame animation
def animate_vehicle(path):
    pygame.init()

    # Set up display
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Vehicle Animation")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # Positions for points (for demonstration purposes)
    positions = {
        'A': (100, 100),
        'B': (300, 100),
        'C': (200, 300),
        'D': (400, 300),
        'E': (500, 500)
    }

    # Vehicle properties
    vehicle_radius = 10
    vehicle_pos = positions[path[0]]
    speed = 0.1  # Speed factor

    running = True
    for i in range(1, len(path)):
        start_pos = positions[path[i - 1]]
        end_pos = positions[path[i]]
        start_time = time.time()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = time.time()
            elapsed_time = current_time - start_time

            # Calculate the vehicle's position based on linear interpolation
            t = min(1, elapsed_time / speed)
            vehicle_pos = (
                start_pos[0] + t * (end_pos[0] - start_pos[0]),
                start_pos[1] + t * (end_pos[1] - start_pos[1])
            )

            # Clear screen
            window.fill(white)

            # Draw edges
            for u, v in G.edges:
                pygame.draw.line(window, black, positions[u], positions[v], 2)

            # Draw nodes
            for node, pos in positions.items():
                pygame.draw.circle(window, black, pos, vehicle_radius)

            # Draw vehicle
            pygame.draw.circle(window, red, (int(vehicle_pos[0]), int(vehicle_pos[1])), vehicle_radius)

            pygame.display.update()

            if t >= 1:
                break

    pygame.quit()

# Tkinter GUI
def on_calculate():
    start = start_entry.get()
    end = end_entry.get()
    if start not in G or end not in G:
        messagebox.showerror("Error", "Invalid start or end point")
        return

    path, cost = dijkstra(G, start, end)
    toll = calculate_toll(path, G)

    path_label.config(text=f"Path: {' -> '.join(path)}")
    toll_label.config(text=f"Toll: {toll}")

    # Start the pygame animation
    animate_vehicle(path)

root = tk.Tk()
root.title("GPS Toll-Based System")

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

path_label = tk.Label(root, text="")
path_label.pack()

toll_label = tk.Label(root, text="")
toll_label.pack()

# Create graph and start Tkinter main loop
G = create_graph()
root.mainloop()
