import heapq
import math
from collections import deque

def dfs(start_node, goal_nodes, graph):
    """
    Finds a path to the goal using Depth-First Search (DFS).
    
    Parameters:
    - start_node: The starting node (e.g., '2').
    - goal_nodes: A list of target nodes (e.g., ['4', '5']).
    - graph: A dictionary of dictionaries representing edges and costs.
             Example: {'2': {'1': 4.0, '3': 4.0}}
    """

    frontier = [(start_node, [start_node])] 
    
    explored = set()
    
    nodes_created = 1 

    while frontier:
        current_node, path = frontier.pop()

        if current_node in goal_nodes:
            path_string = "-".join(path)
            return f"{current_node} {nodes_created}\n{path_string}"

        if current_node not in explored:
            explored.add(current_node)

            neighbors_dict = graph.get(current_node, {})
            neighbor_ids = list(neighbors_dict.keys())
            
            neighbor_ids.sort(key=int, reverse=True)

            for neighbor in neighbor_ids:
                if neighbor not in explored:
                    new_path = list(path)
                    new_path.append(neighbor)
                    
                    frontier.append((neighbor, new_path))
                    nodes_created += 1

    return "No path found"

def bfs(start_node, goal_nodes, graph):
    """
    Finds a path to the goal using Breadth-First Search (BFS).
    
    Parameters:
    - start_node: The starting node (e.g., '2').
    - goal_nodes: A list of target nodes (e.g., ['4', '5']).
    - graph: A dictionary of dictionaries representing edges and costs.
             Example: {'2': {'1': 4.0, '3': 4.0}}
    """
    
    frontier = deque([(start_node, [start_node])])
    
    explored = set()
    
    nodes_created = 1

    while frontier:
        current_node, path = frontier.popleft()

        if current_node in goal_nodes:
            path_string = "-".join(path)
            return f"{current_node} {nodes_created}\n{path_string}"
        
        if current_node not in explored:
            explored.add(current_node)

            neighbors_dict = graph.get(current_node, {})
            neighbor_ids = list(neighbors_dict.keys())

            neighbor_ids.sort(key=int)

            for neighbor in neighbor_ids:
                if neighbor not in explored:
                    new_path = list(path)
                    new_path.append(neighbor)

                    frontier.append((neighbor, new_path))
                    nodes_created += 1

    return "No path found"

def gbfs(start_node, goal_node, graph):
    return 

def a_star(start_node, goal_node, graph):
    return 
def cus1(start_node, goal_nodes, graph):
    """
    Uniform Cost Search (UCS) - Uninformed Search
    """
    
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node, [start_node]))
    
    visited = {}
    
    nodes_expanded = 0
    
    while priority_queue:
        current_cost, current_node, path = heapq.heappop(priority_queue)
        
        if current_node in visited and visited[current_node] < current_cost:
            continue
            
        visited[current_node] = current_cost
        nodes_expanded += 1 
        if str(current_node) in goal_nodes:
       
            path_str = " ".join(map(str, path))
            return f"goal {current_node} {nodes_expanded}\n{path_str}"

        neighbors = graph.get(current_node, {})
        
        for neighbor, edge_cost in neighbors.items():
            new_cost = current_cost + edge_cost

            if neighbor not in visited or new_cost < visited.get(neighbor, float('inf')):
                new_path = list(path)
                new_path.append(neighbor)

                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
                

    return "No path found"
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


