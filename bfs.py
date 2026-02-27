from collections import deque

# Breadth-First Search Algorithm

def bfs(start_node, goal_nodes, graph):

    # The frontier is a queue (FIFO) that stores:
    # (current_node, path_from_start_to_that_node)
    frontier = deque([(start_node, [start_node])])

    # Explored set keeps track of visited nodes
    explored = set()

    # Count how many nodes have been created (start node counts as 1)
    nodes_created = 1

    # Continue searching while there are nodes to explore
    while frontier:
        # Remove the first node added (FIFO behavior)
        current_node, path = frontier.popleft()

        # Check if we have reached one of the goal nodes
        if current_node in goal_nodes:
            path_string = " - ".join(path)
            return (
                f"Goal Reached at: {current_node}\n"
                f"Nodes created: {nodes_created}\n"
                f"Path found: {path_string}"
            )

        # Only expand the node if it hasn't been visited before
        if current_node not in explored:
            explored.add(current_node)

            # Get all neighbors of the current node
            neighbors_dict = graph.get(current_node, {})
            neighbor_ids = list(neighbors_dict.keys())

            # Sort neighbors so that smaller node IDs are expanded first
            # (this keeps the search order consistent)
            neighbor_ids.sort(key=int)

            for neighbor in neighbor_ids:
                # Add neighbor to frontier only if:
                # - it has not been explored
                # - it is not already waiting in the frontier
                if (
                    neighbor not in explored
                    and neighbor not in [n for n, _ in frontier]
                ):
                    # Create a new path including this neighbor
                    new_path = path + [neighbor]

                    # Add neighbor to the queue for future expansion
                    frontier.append((neighbor, new_path))

                    # Increase node creation counter
                    nodes_created += 1

    # If the queue becomes empty and no goal was found
    return "No path found"