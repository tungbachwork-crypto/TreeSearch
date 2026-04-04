import math
import heapq

def a_star(graph, coords, origin, destination):
    origin = str(origin)
    destination = str(destination)

    def heuristic(n1, n2):
        if n1 not in coords or n2 not in coords:
            return 0
        lat1, lon1 = coords[n1]
        lat2, lon2 = coords[n2]
        
        R = 6371
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

    open_list = []
    heapq.heappush(open_list, (0, origin))

    came_from = {}
    g_score = {origin: 0}
    nodes_created = 0

    while open_list:
        f_val, current = heapq.heappop(open_list)
        nodes_created += 1

        if current == destination:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(origin)
            path.reverse()

            return {
                "path": path,
                "cost": float(g_score[destination]),
                "nodes_created": nodes_created
            }

        for neighbor, cost in graph.get(current, {}).items():
            tentative_g = g_score[current] + cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, destination)
                heapq.heappush(open_list, (f_score, neighbor))

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_created": nodes_created
    }