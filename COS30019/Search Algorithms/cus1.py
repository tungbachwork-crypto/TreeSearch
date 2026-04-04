import heapq

def ucs(graph, origin, destination):
    origin = str(origin)
    destination = str(destination)

    pq = [(0.0, origin)]
    
    parent = {origin: None}
    
    visited_costs = {origin: 0.0}
    
    nodes_created = 0

    while pq:
        current_cost, current_node = heapq.heappop(pq)
        nodes_created += 1

        if current_node == destination:
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()

            return {
                "path": path,
                "cost": float(current_cost),
                "nodes_created": nodes_created
            }

        if current_cost > visited_costs.get(current_node, float('inf')):
            continue

        for neighbor, edge_cost in graph.get(current_node, {}).items():
            new_cost = current_cost + edge_cost

            if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                visited_costs[neighbor] = new_cost
                parent[neighbor] = current_node
                heapq.heappush(pq, (new_cost, neighbor))

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }