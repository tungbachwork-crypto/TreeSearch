import sys
import os

from dfs import dfs
from bfs import bfs
from gbfs import gbfs
from a_star import a_star
from cus1 import cus1
from cus2 import cus2


def load_testcase(filename):
    filepath = os.path.join("maps", f"{filename}.txt")

    start_node = None
    goal_nodes = []
    graph = {}
    coords = {}

    with open(filepath, "r") as file:
        lines = file.readlines()

    reading_nodes = False
    reading_edges = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("Nodes"):
            reading_nodes = True
            reading_edges = False
            continue

        if line.startswith("Edges"):
            reading_nodes = False
            reading_edges = True
            continue

        if reading_nodes and ":" in line:
            node_id, coord_part = line.split(":")
            node_id = node_id.strip()
            coord_part = coord_part.strip()[1:-1]
            x, y = coord_part.split(",")
            coords[node_id] = (float(x.strip()), float(y.strip()))

        if reading_edges and line.startswith("("):
            left, cost = line.split(":")
            cost = float(cost.strip())
            nodes_part = left.strip()[1:-1]
            from_node, to_node = nodes_part.split(",")

            from_node = from_node.strip()
            to_node = to_node.strip()

            if from_node not in graph:
                graph[from_node] = {}

            graph[from_node][to_node] = cost

        if line.startswith("Destination") or line.startswith("Destinations"):
            _, value = line.split(":", 1)
            goal_nodes = [
                node.strip()
                for node in value.strip().split(";")
                if node.strip()
            ]

        if line.startswith("Origin"):
            _, value = line.split(":", 1)
            start_node = value.strip()

    return start_node, goal_nodes, graph, coords


def extract_output(result_string):
    if not result_string:
        return None, None, None

    lines = result_string.split("\n")

    goal = None
    nodes_created = None
    path = None

    for line in lines:
        if line.startswith("Goal Reached at:"):
            goal = line.split(":")[1].strip()

        if line.startswith("Nodes created:"):
            nodes_created = line.split(":")[1].strip()

        if line.startswith("Path found:"):
            path = line.split(":")[1].strip().replace(" ", "")

    return goal, nodes_created, path


def main():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    start_node, goal_nodes, graph, coords = load_testcase(filename)

    algorithms = {
        "DFS": dfs,
        "BFS": bfs,
        "GBFS": gbfs,
        "A*": a_star,
        "CUS1": cus1,
        "CUS2": cus2
    }

    if method not in algorithms:
        print("Invalid method")
        sys.exit(1)

    algorithm = algorithms[method]

    if method in ["GBFS", "A*", "CUS2"]:
        result = algorithm(start_node, goal_nodes, graph, coords)
    else:
        result = algorithm(start_node, goal_nodes, graph)

    if result == "No path found":
        print(f"{filename} {method}")
        print("No solution found")
        sys.exit(0)

    goal, nodes_created, path = extract_output(result)

    print(f"{filename} {method}")
    print(f"{goal} {nodes_created}")
    print(path)


if __name__ == "__main__":
    main()