import copy

def get_k_shortest_paths(graph, coords, origin, destination, k=5, algorithm_func=None):
    if algorithm_func is None:
        return []

    # 1. Find the first shortest path
    initial_result = algorithm_func(graph, coords, origin, destination)
    if not initial_result or not initial_result["path"]:
        return []

    # A list to store the final K shortest paths
    A = [initial_result]
    # A priority queue/list to store potential candidates for the next shortest path
    B = []

    for ki in range(1, k):
        # The previous shortest path
        prev_path = A[-1]["path"]

        # Iterate through every node in the previous path (except the last one)
        for i in range(len(prev_path) - 1):
            spur_node = prev_path[i]
            root_path = prev_path[:i + 1]

            # Temporarily modify the graph to remove edges
            temp_graph = copy.deepcopy(graph)
            
            # Remove edges that are part of previous shortest paths to force a new route
            for path_data in A:
                p = path_data["path"]
                if len(p) > i and root_path == p[:i + 1]:
                    u, v = p[i], p[i + 1]
                    if u in temp_graph and v in temp_graph[u]:
                        del temp_graph[u][v]

            # Find the "spur path" from the spur_node to the destination
            spur_result = algorithm_func(temp_graph, coords, spur_node, destination)

            if spur_result["path"]:
                # Total path is root_path + spur_path
                total_path = root_path[:-1] + spur_result["path"]
                
                # Calculate total cost
                total_cost = 0.0
                for j in range(len(total_path) - 1):
                    total_cost += graph[total_path[j]][total_path[j+1]]

                candidate = {
                    "path": total_path,
                    "cost": float(total_cost),
                    "nodes_created": spur_result.get("nodes_created", 0)
                }

                # Add to B if not already there
                if candidate not in B:
                    B.append(candidate)

        if not B:
            break

        # Sort B by cost and move the best candidate to A
        B.sort(key=lambda x: x["cost"])
        A.append(B.pop(0))

    return A