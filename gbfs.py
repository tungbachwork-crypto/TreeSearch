import math
import heapq

# Greedy Best_First Search Algorithm

def gbfs(start_node, goal_nodes, graph, coords):

    # Heuristic function:
    # Estimates how close a node is to the nearest goal
    # using straight-line (Euclidean) distance.
    def heuristic(node):
        x1, y1 = coords[node]
        return min(
            math.sqrt((x1 - coords[g][0]) ** 2 + (y1 - coords[g][1]) ** 2)
            for g in goal_nodes
        )

    # Node class stores the current node and its parent
    # (used later to reconstruct the final path).
    class Node:
        def __init__(self, node_id, parent=None):
            self.id = node_id
            self.parent = parent

    # Priority queue (min-heap) ordered by heuristic value only
    open_list = []

    # Closed set keeps track of already visited nodes
    closed = set()

    # Counter to track how many nodes were created
    created_nodes = 0

    # Tie-breaker counter to maintain heap order when heuristic values are equal
    counter = 0

    # Create and push the start node into the priority queue
    start = Node(start_node, None)
    heapq.heappush(open_list, (heuristic(start_node), counter, start))
    created_nodes += 1
    counter += 1

    # Main search loop
    while open_list:
        # Pop node with the smallest heuristic value (greedy choice)
        _, _, current = heapq.heappop(open_list)

        # Goal test: check if current node is one of the goals
        if current.id in goal_nodes:
            path = []
            node = current

            # Reconstruct path by following parent links
            while node:
                path.append(node.id)
                node = node.parent

            path.reverse()

            return (
                f"Goal Reached at: {current.id}\n"
                f"Nodes created: {created_nodes}\n"
                f"Path found: {' - '.join(path)}"
            )

        # Skip if node has already been visited
        if current.id in closed:
            continue

        # Mark node as visited
        closed.add(current.id)

        # Get neighbors in sorted order for consistent expansion
        neighbors = sorted(graph.get(current.id, {}).items())

        for neighbor_id, cost in neighbors:
            # Only consider neighbor if it hasn't been explored
            if neighbor_id not in closed:
                child = Node(neighbor_id, current)

                # Push neighbor into priority queue using heuristic only
                heapq.heappush(
                    open_list,
                    (heuristic(neighbor_id), counter, child)
                )

                created_nodes += 1
                counter += 1

    # If no goal was found after exploring all reachable nodes
    return "No path found"