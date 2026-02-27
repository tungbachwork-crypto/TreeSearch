import heapq

def dfs(start_node, goal_node, graph):
    return 

def bfs(start_node, goal_node, graph):
    return 

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
def cus2(start_node, goal_node, graph):
    return 
