
# Depth-First Search Algorithm

def dfs(start_node, goal_nodes, graph):
    # The frontier works like a stack (LIFO).
    # Each element stores: (current_node, path_from_start)
    frontier = [(start_node, [start_node])] 
    
    # Keep track of visited nodes to avoid revisiting them
    explored = set()
    
    # Count how many nodes have been created (start node counts as 1)
    nodes_created = 1 

    # Continue searching while there are nodes in the stack
    while frontier:
        # Pop the most recently added node (LIFO behavior)
        current_node, path = frontier.pop()

        # Check if we have reached one of the goal nodes
        if current_node in goal_nodes:
            path_string = " - ".join(path)

            return (
                f"Goal Reached at: {current_node}\n"
                f"Nodes created: {nodes_created}\n"
                f"Path found: {path_string}"
            )

        # Only expand the node if it hasn't been explored before
        if current_node not in explored:
            explored.add(current_node)

            # Get neighbors of the current node
            neighbors_dict = graph.get(current_node, {})
            neighbor_ids = list(neighbors_dict.keys())
            
            # Sort in reverse order so that smaller IDs are processed first
            # when popped from the stack (DFS behavior control)
            neighbor_ids.sort(key=int, reverse=True)

            for neighbor in neighbor_ids:
                # Add neighbor if it hasn't been visited
                if neighbor not in explored:
                    # Create a new path including this neighbor
                    new_path = list(path)
                    new_path.append(neighbor)
                    
                    # Push neighbor onto the stack
                    frontier.append((neighbor, new_path))
                    
                    # Increase node creation counter
                    nodes_created += 1

    # If stack becomes empty and no goal is found
    return "No path found"