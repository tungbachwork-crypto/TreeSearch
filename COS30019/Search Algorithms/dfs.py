def dfs(graph, origin, destination):
    origin = str(origin)
    destination = str(destination)

    stack = [(origin, [origin])]
    visited = set()
    nodes_created = 1

    while stack:
        current, path = stack.pop()

        if current == destination:
            total_cost = 0.0
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                total_cost += graph.get(u, {}).get(v, 0.0)

            return {
                "path": path,
                "cost": float(total_cost),
                "nodes_created": nodes_created
            }

        if current not in visited:
            visited.add(current)

            neighbors = sorted(graph.get(current, {}).keys(), reverse=True)

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
                    nodes_created += 1

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }