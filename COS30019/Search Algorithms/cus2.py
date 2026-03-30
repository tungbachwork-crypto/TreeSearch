import math
import heapq

def theta_star(graph, coords, origin, destination):
    origin = str(origin)
    destination = str(destination)

    def euclidean(a, b):
        if a not in coords or b not in coords:
            return 0
        lat1, lon1 = coords[a]
        lat2, lon2 = coords[b]
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    def line_of_sight(a, b):
        return b in graph.get(a, {})

    g_cost = {origin: 0.0}
    parent = {origin: None}
    open_heap = [(euclidean(origin, destination), origin)]
    closed = set()
    nodes_created = 0

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)
        nodes_created += 1

        if current == destination:
            path = []
            curr = current
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            return {
                "path": path,
                "cost": float(g_cost[current]),
                "nodes_created": nodes_created
            }

        for neighbor, edge_cost in graph.get(current, {}).items():
            if neighbor in closed:
                continue

            p = parent[current]

            if p is not None and line_of_sight(p, neighbor):
                shortcut_cost = graph[p][neighbor] 
                tentative_g = g_cost[p] + shortcut_cost
                new_parent = p
            else:
                tentative_g = g_cost[current] + edge_cost
                new_parent = current

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                parent[neighbor] = new_parent
                f_val = tentative_g + euclidean(neighbor, destination)
                heapq.heappush(open_heap, (f_val, neighbor))

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }