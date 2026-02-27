import heapq

# Uniform Cost Search

def cus1(start_node, goal_nodes, graph):
    # Priority queue (min-heap) ordered by path cost.
    # Each element stores:
    # (total_cost_so_far, node_id_as_int_for_tiebreak, node_name, path_to_node)
    priority_queue = []
    heapq.heappush(priority_queue, (0, int(start_node), start_node, [start_node]))

    # Dictionary to store the lowest cost found so far for each node
    visited = {}

    # Counter to track how many nodes were expanded
    nodes_expanded = 0

    # Continue searching while there are nodes in the priority queue
    while priority_queue:
        # Pop the node with the smallest accumulated cost
        current_cost, _, current_node, path = heapq.heappop(priority_queue)

        # If we have already found a cheaper way to reach this node, skip it
        if current_node in visited and visited[current_node] < current_cost:
            continue

        # Record the best cost for this node
        visited[current_node] = current_cost
        nodes_expanded += 1

        # Goal test: check if current node is one of the goal nodes
        if current_node in goal_nodes:
            path_string = " - ".join(path)
            return (
                f"Goal Reached at: {current_node}\n"
                f"Nodes expanded: {nodes_expanded}\n"
                f"Path found: {path_string}"
            )

        # Get neighbors of the current node
        neighbors = graph.get(current_node, {})

        for neighbor, edge_cost in neighbors.items():
            # Calculate new total cost to reach neighbor
            new_cost = current_cost + edge_cost

            # Only add neighbor if:
            # - it hasn't been visited yet, or
            # - we found a cheaper path to it
            if neighbor not in visited or new_cost < visited.get(neighbor, float('inf')):
                new_path = path + [neighbor]

                # Push neighbor into the priority queue
                heapq.heappush(
                    priority_queue,
                    (new_cost, int(neighbor), neighbor, new_path)
                )

    # If queue becomes empty and no goal is reached
    return "No path found"