import sys
import algorithms
import map_loader

def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    graph = map_loader.read_map(filename)
    
    # Dummy start and goal nodes for now since we aren't parsing the map yet
    start_node = None
    goal_node = None

    result = ""

    if method == "DFS":
        result = algorithms.dfs(start_node, goal_node, graph)
    elif method == "BFS":
        result = algorithms.bfs(start_node, goal_node, graph)
    elif method == "GBFS":
        result = algorithms.gbfs(start_node, goal_node, graph)
    elif method == "AS":
        result = algorithms.a_star(start_node, goal_node, graph)
    elif method == "CUS1":
        result = algorithms.cus1(start_node, goal_node, graph)
    elif method == "CUS2":
        result = algorithms.cus2(start_node, goal_node, graph)
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)

    print(f"{filename} {method}")
    print(result)

if __name__ == "__main__":
    main()
