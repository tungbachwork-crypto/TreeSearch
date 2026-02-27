import math
import heapq

# A* Search Algorithm

def a_star(start_node, goal_nodes, graph, coords):
    # Heuristic function:
    # Calculates the straight-line (Euclidean) distance
    # from the current node to the closest goal node.
    def heuristic(node):
        x1, y1 = coords[node]
        return min(
            math.sqrt((x1 - coords[g][0]) ** 2 + (y1 - coords[g][1]) ** 2)
            for g in goal_nodes
        )

    # Node class to store information about each state in the search
    class Node:
        def __init__(self, node_id, parent=None, g=0, h=0):
            self.id = node_id        # The node name / label
            self.parent = parent     # The previous node (used to rebuild the path)
            self.g = g               # Cost from start node to this node
            self.h = h               # Heuristic cost from this node to goal
            self.f = g + h           # Total estimated cost (f = g + h)

    open_list = []      # Priority queue (min-heap) for nodes to explore
    closed = {}         # Dictionary to store visited nodes and their best g cost
    created_nodes = 0   # Counter to track how many nodes were created
    counter = 0         # Tie-breaker counter to keep heap stable

    # Create the start node
    start_h = heuristic(start_node)
    start = Node(start_node, None, 0, start_h)

    # Push the start node into the open list
    heapq.heappush(open_list, (start.f, counter, start))
    created_nodes += 1
    counter += 1

    # Main A* loop
    while open_list:
        # Pop the node with the smallest f value
        _, _, current = heapq.heappop(open_list)

        # If we reach one of the goal nodes, reconstruct the path
        if current.id in goal_nodes:
            path = []
            node = current

            # Follow parent links back to the start
            while node:
                path.append(node.id)
                node = node.parent

            path.reverse()  # Reverse to get start → goal order

            return (
                f"Goal Reached at: {current.id}\n"
                f"Nodes created: {created_nodes}\n"
                f"Path found: {' - '.join(path)}"
            )

        # Skip this node if we already found a better path to it
        if current.id in closed and closed[current.id] <= current.g:
            continue

        # Mark this node as visited with its current best g cost
        closed[current.id] = current.g

        # Get neighbors in sorted order (for consistent behavior)
        neighbors = sorted(graph.get(current.id, {}).items())

        for neighbor_id, cost in neighbors:
            # Calculate new g cost for neighbor
            new_g = current.g + cost

            # Calculate heuristic for neighbor
            h = heuristic(neighbor_id)

            # Create a new child node
            child = Node(neighbor_id, current, new_g, h)

            # Add child to open list for future exploration
            heapq.heappush(open_list, (child.f, counter, child))
            created_nodes += 1
            counter += 1

    # If open list becomes empty and goal was never reached
    return "No path found"