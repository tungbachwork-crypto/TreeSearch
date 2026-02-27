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
            
        # Đánh dấu đã duyệt node này với chi phí hiện tại
        visited[current_node] = current_cost
        nodes_expanded += 1 # Tăng biến đếm performance
        
        # KIỂM TRA ĐÍCH: Nếu node hiện tại nằm trong danh sách các đích cần đến
        if str(current_node) in goal_nodes:
            # Format output chuẩn theo yêu cầu đề bài: "goal node_id nodes_expanded path"
            path_str = " ".join(map(str, path))
            return f"goal {current_node} {nodes_expanded}\n{path_str}"
            
        # MỞ RỘNG (EXPAND): Đi tìm các node hàng xóm
        # Giả sử graph có cấu trúc: graph[node] = {neighbor1: cost1, neighbor2: cost2}
        neighbors = graph.get(current_node, {})
        
        for neighbor, edge_cost in neighbors.items():
            new_cost = current_cost + edge_cost
            
            # Chỉ cho vào hàng đợi nếu neighbor chưa từng đi qua, 
            # HOẶC tìm được một con đường mới đi đến neighbor đó với giá rẻ hơn
            if neighbor not in visited or new_cost < visited.get(neighbor, float('inf')):
                new_path = list(path)
                new_path.append(neighbor)
                
                # Đẩy vào hàng đợi. heapq sẽ tự động xếp cost thấp lên đầu. 
                # Nếu cost bằng nhau, nó xếp ID neighbor nhỏ hơn lên đầu.
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
                
    # Nếu hàng đợi trống rỗng mà vẫn chưa thấy đích (như map06_no_solution)
    return "No path found"
def cus2(start_node, goal_node, graph):
    return 
