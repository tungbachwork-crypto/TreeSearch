from collections import deque

def bfs(graph, origin, destination):
    origin = str(origin)
    destination = str(destination)

    queue = deque([origin])
    visited = {origin}
    parent = {origin: None}
    nodes_created = 1

    while queue:
        current = queue.popleft()

        if current == destination:
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
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

        neighbors = sorted(graph.get(current, {}).keys())
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                nodes_created += 1

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }