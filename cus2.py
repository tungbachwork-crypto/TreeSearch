import math
import heapq

# Theta* Search Algorithm

def cus2(start_node, goal_nodes, graph, coords):

    # Calculate Euclidean distance between two coordinate points
    def euclidean(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    # Heuristic function:
    # Estimates distance from current node to the closest goal node
    def heuristic(node):
        return min(euclidean(coords[node], coords[g]) for g in goal_nodes)

    # Line-of-sight check:
    # In this simplified version, we only check whether
    # there is a direct edge between two nodes in the graph.
    def line_of_sight(a, b):
        # NOTE: This is still simplified (direct edge check only)
        return b in graph.get(a, {})

    # Reconstruct the final path using the parent dictionary
    def reconstruct_path(parent, node):
        path = []
        while node is not None:
            path.append(node)
            node = parent[node]
        return path[::-1]  # reverse to get start → goal order

    # g_cost stores the best known cost from start to each node
    g_cost = {start_node: 0.0}

    # parent dictionary stores the predecessor of each node
    parent = {start_node: None}

    counter = 0              # Tie-breaker for heap ordering
    created_nodes = 1        # Start node counts as created

    # Priority queue ordered by f = g + h
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start_node), counter, start_node))

    # Closed set keeps track of expanded nodes
    closed = set()

    while open_heap:
        # Get node with smallest f value
        _, _, current = heapq.heappop(open_heap)

        # Skip if already processed
        if current in closed:
            continue

        closed.add(current)

        # Goal test
        if current in goal_nodes:
            path = reconstruct_path(parent, current)

            return (
                f"Goal Reached at: {current}\n"
                f"Nodes created: {created_nodes}\n"
                f"Path found: {' - '.join(path)}"
            )

        # Expand neighbors in sorted order for consistent behavior
        for neighbour, edge_cost in sorted(graph.get(current, {}).items()):

            if neighbour in closed:
                continue

            # If neighbour not seen before, initialize its cost
            if neighbour not in g_cost:
                g_cost[neighbour] = math.inf
                created_nodes += 1

            # Get parent of current node
            p = parent[current]

            # Theta* improvement:
            # If there is line of sight from current's parent to neighbour,
            # try connecting them directly (shortcut).
            if p is not None and line_of_sight(p, neighbour):
                tentative_g = g_cost[p] + euclidean(coords[p], coords[neighbour])
                new_parent = p
            else:
                tentative_g = g_cost[current] + edge_cost
                new_parent = current

            # If we found a better path to neighbour, update it
            if tentative_g < g_cost[neighbour]:
                g_cost[neighbour] = tentative_g
                parent[neighbour] = new_parent

                counter += 1
                f_val = tentative_g + heuristic(neighbour)

                # Push updated neighbour into the priority queue
                heapq.heappush(open_heap, (f_val, counter, neighbour))

    # If no path to goal is found
    return "No path found"