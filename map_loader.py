import sys
import re

def read_map(filename):
    graph = {}
    node_coords = {}
    start_node = None
    goal_nodes = []

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    mode = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Nodes:"):
            mode = "Nodes"
            continue
        elif line.startswith("Edges:"):
            mode = "Edges"
            continue
        elif line.startswith("Origin:"):
            mode = "Origin"
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                start_node = parts[1].strip()
            continue
        elif line.startswith("Destinations:"):
            mode = "Destinations"
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                goal_nodes = [g.strip() for g in parts[1].split(';') if g.strip()]
            continue


        if mode == "Nodes":
            match = re.match(r'(\w+)\s*:\s*\(\s*([-\d.]+)\s*[,;]\s*([-\d.]+)\s*\)', line)
            if match:
                node_id, x, y = match.groups()
                node_coords[node_id] = (float(x), float(y))
                if node_id not in graph:
                    graph[node_id] = {}

        elif mode == "Edges":
            match = re.search(r'\(\s*(\w+)\s*[,;:]\s*(\w+)\s*\)\s*:\s*([-\d.]+)', line)
            if match:
                u, v, cost = match.groups()
                cost = float(cost)
                
                if u not in graph: graph[u] = {}
                if v not in graph: graph[v] = {}
                
                graph[u][v] = cost

        elif mode == "Origin":
            if not start_node:
                start_node = line.strip()

        elif mode == "Destinations":
            if not goal_nodes:
                goal_nodes = [g.strip() for g in line.split(';') if g.strip()]

    return {
        "graph": graph,
        "coords": node_coords,
        "start": start_node,
        "goals": goal_nodes
    }