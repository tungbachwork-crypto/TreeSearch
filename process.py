import time
import tracemalloc
import os

from dfs import dfs
from bfs import bfs
from gbfs import gbfs
from a_star import a_star
from cus1 import cus1
from cus2 import cus2

# Load a testcase file from the "maps" folder
def load_testcase(testcase_name):
    filepath = os.path.join("maps", f"{testcase_name}.txt")

    start_node = None
    graph = {}
    goal_nodes = []
    coords = {}

    # Read all lines from the testcase file
    with open(filepath, "r") as file:
        lines = file.readlines()

    reading_nodes = False
    reading_edges = False

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Detect the start of the node section
        if line.startswith("Nodes"):
            reading_nodes = True
            reading_edges = False
            continue

        # Detect the start of the edge section
        if line.startswith("Edges"):
            reading_nodes = False
            reading_edges = True
            continue

        # Read node coordinates
        if reading_nodes and ":" in line:
            node_id, coord_part = line.split(":")
            node_id = node_id.strip()

            # Remove parentheses and split x, y
            coord_part = coord_part.strip()[1:-1]
            x, y = coord_part.split(",")

            coords[node_id] = (float(x.strip()), float(y.strip()))

        # Read edge definitions
        if reading_edges and line.startswith("("):
            # Example format: (1,3): 27
            left, cost = line.split(":")
            cost = float(cost.strip())

            nodes_part = left.strip()[1:-1]
            from_node, to_node = nodes_part.split(",")

            from_node = from_node.strip()
            to_node = to_node.strip()

            # Create adjacency list entry if not exists
            if from_node not in graph:
                graph[from_node] = {}

            graph[from_node][to_node] = cost

        # Read destination nodes (can be multiple separated by ;)
        if line.startswith("Destination") or line.startswith("Destinations"):
            _, value = line.split(":", 1)
            goal_nodes = [
                node.strip()
                for node in value.strip().split(";")
                if node.strip()
            ]

        # Read origin node
        if line.startswith("Origin"):
            _, value = line.split(":", 1)
            start_node = value.strip()

    return start_node, goal_nodes, graph, coords


# Calculate total cost of a path using the graph
def calculate_cost(path, graph):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]
    return total_cost


# Extract the path from the result string returned by algorithms
def extract_path(result_string):
    if not result_string or "Path found:" not in result_string:
        return None

    try:
        path_part = result_string.split("Path found:")[1].split("\n")[0].strip()
        return [node.strip() for node in path_part.split("-")]
    except:
        return None


# Run a selected algorithm and measure its performance
def run_algorithm(algorithm_name, testcase_name):
    try:
        # Load graph data from testcase
        start_node, goal_nodes, graph, coords = load_testcase(testcase_name)

        if start_node is None:
            print("ERROR: Origin not found in testcase.")
            return None

        if not goal_nodes:
            print("ERROR: Destination not found in testcase.")
            return None

        # Map algorithm names to their corresponding functions
        algorithms = {
            "DFS": dfs,
            "BFS": bfs,
            "GBFS": gbfs,
            "A*": a_star,
            "CUS1": cus1,
            "CUS2": cus2
        }

        algorithm = algorithms.get(algorithm_name)

        if algorithm is None:
            print("ERROR: Invalid algorithm name.")
            return None

        # Start measuring memory and time
        tracemalloc.start()
        start_time = time.perf_counter()

        # Algorithms that use heuristic require coordinates
        if algorithm_name in ["CUS2", "GBFS", "A*"]:
            result = algorithm(start_node, goal_nodes, graph, coords)
        else:
            result = algorithm(start_node, goal_nodes, graph)

        end_time = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        time_used = end_time - start_time
        memory_used = peak / 1024  # convert bytes to KB

        if result is None:
            return None

        # Extract path from algorithm result
        path = extract_path(result)

        # If no valid path found, return result without cost
        if path is None:
            return {
                "result": result,
                "time": time_used,
                "memory": memory_used,
                "cost": None,
                "optimal": False
            }

        # Calculate cost of returned path
        cost = calculate_cost(path, graph)

        # Check optimality by comparing with A* result
        is_optimal = False
        try:
            optimal_result = a_star(start_node, goal_nodes, graph, coords)
            optimal_path = extract_path(optimal_result)

            if optimal_path:
                optimal_cost = calculate_cost(optimal_path, graph)
                is_optimal = (cost == optimal_cost)
        except:
            pass

        return {
            "result": result,
            "time": time_used,
            "memory": memory_used,
            "cost": cost,
            "optimal": is_optimal
        }

    except Exception as e:
        print("ERROR in run_algorithm:", e)
        return None