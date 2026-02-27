import heapq
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
    return
def cus2(start_node, goal_node, graph):
    return 
