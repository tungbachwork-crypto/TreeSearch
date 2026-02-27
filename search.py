import sys
import algorithms
import map_loader
import time

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

    start_time = time.perf_counter()

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

    end_time = time.perf_counter()
    exec_time_ms = (end_time - start_time) * 1000

    print(f"{filename} {method}")
    print(result)

    try:
        lines = result.strip().split('\n')
        if len(lines) >= 2 and lines[0].startswith("goal"):
            nodes_expanded = lines[0].split()[2]
            path = lines[1].strip().split() 
            
            total_cost = 0
            for i in range(len(path) - 1):
                total_cost += graph[path[i]][path[i+1]]
            
            sys.stderr.write(f"\n+--------------------------------------------------+\n")
            sys.stderr.write(f"| Method         : {method:<31} |\n")
            sys.stderr.write(f"| Execution time : {exec_time_ms:<15.3f} mili-sec        |\n")
            sys.stderr.write(f"| Total Cost     : {total_cost:<31} |\n")
            sys.stderr.write(f"| Expanded Node  : {nodes_expanded:<31} |\n")
            sys.stderr.write(f"+--------------------------------------------------+\n")
            
        elif "No path found" in result:
            sys.stderr.write(f"\n+--------------------------------------------------+\n")
            sys.stderr.write(f"|               PERFORMANCE REPORT                 |\n")
            sys.stderr.write(f"+--------------------------------------------------+\n")
            sys.stderr.write(f"| Method         : {method:<31} |\n")
            sys.stderr.write(f"| Execution time : {exec_time_ms:<15.3f} mili-sec        |\n")
            sys.stderr.write(f"| Result         : FAILED (No path found)          |\n")
            sys.stderr.write(f"+--------------------------------------------------+\n")
    except Exception as e:
        pass

if __name__ == "__main__":
    main()