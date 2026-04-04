import math
import heapq

def gbfs(graph, coords, origin, destination):
    origin = str(origin)
    destination = str(destination)

    def heuristic(n):
        if n not in coords or destination not in coords:
            return 0
        lat1, lon1 = coords[n]
        lat2, lon2 = coords[destination]
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

    heap = [(heuristic(origin), origin)]
    visited = set()
    parent = {origin: None}
    nodes_created = 0

    while heap:
        _, node = heapq.heappop(heap)
        
        if node in visited:
            continue
        visited.add(node)
        nodes_created += 1

        if node == destination:
            path = []
            curr = node
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()

            total_cost = 0.0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                total_cost += graph.get(u, {}).get(v, 0.0)

            return {
                "path": path,
                "cost": float(total_cost),
                "nodes_created": nodes_created
            }

        for neighbor in graph.get(node, {}).keys():
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = node
                heapq.heappush(heap, (heuristic(neighbor), neighbor))

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }