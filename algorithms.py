import heapq
import math

def dfs(start_node, goal_node, graph):
    return 

def bfs(start_node, goal_node, graph):
    return 

def gbfs(start_node, goal_node, graph):
    return 

def a_star(start_node, goal_node, graph):
    return 

def cus1(start_node, goal_nodes, graph):
    return
def cus2(start_node, goal_node, graph, coords): #Hill-Climbing
    def euclidean(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


    def heuristic(node, goals, coords):
        return min(euclidean(coords[node], coords[g]) for g in goals)

    def reconstruct_path(parent, goal):
        path = []
        while goal is not None:
            path.append(goal)
            goal = parent.get(goal)
        path.reverse()
        return path

    current = start_node
    parent = {start_node: None}
    visited = set([start_node])
    created_nodes = 1  # count origin

    while True:
        #  Goal test
        if current in goal_node:
            path = reconstruct_path(parent, current)
            return current, created_nodes, path

        neighbors_dict = graph.get(current, {})
        neighbors = list(neighbors_dict.items())  # [(neighbor, cost)]

        neighbors.sort(key=lambda x: int(x[0]))

        current_h = heuristic(current, goal_node, coords)

        best_neighbor = None
        best_h = current_h

        for neighbor, cost in neighbors:
            if neighbor in visited:
                continue

        created_nodes += 1
        h = heuristic(neighbor, goal_node, coords)

            # classic hill climbing (strict improvement)
        if h < best_h:
            best_h = h
            best_neighbor = neighbor

        #  Local minimum → failure
        if best_neighbor is None:
            return None, created_nodes, []

        parent[best_neighbor] = current
        visited.add(best_neighbor)
        current = best_neighbor
    return 

