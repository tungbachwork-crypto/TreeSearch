import sys
import algorithms
import map_loader

def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    map_data = map_loader.read_map(filename)
    
    graph = map_data["graph"]
    start_node = map_data["start"]
    goal_nodes = map_data["goals"] 
    coords = map_data["coords"]

    result = ""

    if method == "DFS":
        result = algorithms.dfs(start_node, goal_nodes, graph)
    elif method == "BFS":
        result = algorithms.bfs(start_node, goal_nodes, graph)
    elif method == "GBFS":
        result = algorithms.gbfs(start_node, goal_nodes, graph)
    elif method == "AS":
        result = algorithms.a_star(start_node, goal_nodes, graph)
    elif method == "CUS1":
        result = algorithms.cus1(start_node, goal_nodes, graph)
    elif method == "CUS2":
        result = algorithms.cus2(start_node, goal_nodes, graph, coords)
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)

    print(f"{filename} {method}")
    print(result)

if __name__ == "__main__":
    main()