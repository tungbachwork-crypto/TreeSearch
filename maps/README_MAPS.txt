1. map01_basic.txt
Purpose: Sanity check. Validate basic graph parsing and search execution on a trivial graph.

Challenge: Minimal. Ensures the core system infrastructure is functional.

2. map02_dead_end.txt
Purpose: Introduce paths that lead to nowhere (leaf nodes that are not goals).

Challenge: Test the algorithm's ability to backtrack correctly (crucial for DFS) without getting stuck.

3. map03_cycle_loop.txt
Purpose: Graph contains cyclic paths (e.g., A → B → A).

Challenge: Verify that the visited / explored set is implemented correctly to prevent infinite loops.

4. map04_greedy_trap.txt
Purpose: A path with a low heuristic value (appears close to the goal) but leads to a dead end or a high-cost route.

Challenge: Expose the weakness of Greedy Best-First Search (GBFS) (which gets fooled) compared to A*.

5. map05_multi_goals.txt
Purpose: Graph contains multiple distinct Destination nodes.


Challenge: Verify if the algorithm correctly identifies the goal and handles multiple goal checks properly (as per requirement ).

6. map06_no_solution.txt
Purpose: Origin and Destination nodes are completely disconnected.

Challenge: Ensure the program terminates gracefully (returns "No Path" or "Failure") instead of crashing or running indefinitely.

7. map07_tie_breaker.txt
Purpose: Multiple successor nodes have identical costs or heuristic values.


Challenge: Verify strict adherence to the tie-breaking rule: "expand smaller node ID first".

8. map08_high_cost_short_path.txt
Purpose: A path with few steps (low depth) but extremely high edge weights/costs.

Challenge: Demonstrate the difference between BFS (finds fewest steps, ignores cost) and A* (finds lowest cost).

9. map09_bottleneck.txt
Purpose: Graph topology where all paths must converge through a single specific node.

Challenge: Test the search strategy's ability to navigate constrained paths.

10. map10_complex_maze.txt
Purpose: Large-scale graph combining cycles, dead ends, and traps.

Challenge: Performance stress test. Measure and compare "Nodes Expanded" and execution time across all algorithms.