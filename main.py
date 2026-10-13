"""CLI runner for the BFS vs. depth-limited DFS maze pathfinding engine."""
from time import perf_counter

from bfs import bfs
from dfs import dfs

MAZE = [
    list("S...#...."),
    list("##..#.#.."),
    list("........."),
    list(".####...."),
    list("......#.."),
    list("######..."),
]
START = (0, 0)
GOAL = (5, 8)
DEPTH_LIMIT = 200


def run_algorithm(name, solver, maze, start, goal):
    """Run a solver and return its result plus elapsed-time metrics."""
    begin = perf_counter()
    path, expanded = solver(maze, start, goal)
    elapsed_ms = (perf_counter() - begin) * 1000
    return {
        "name": name,
        "path": path,
        "expanded": expanded,
        "elapsed_ms": elapsed_ms,
        "path_length": max(0, len(path) - 1) if path else None,
    }


def render_maze(maze, path):
    """Return an ASCII grid with the discovered path marked by '*'."""
    rendered = [row[:] for row in maze]
    for r, c in path:
        if rendered[r][c] not in ("S", "G"):
            rendered[r][c] = "*"
    return "\n".join("".join(row) for row in rendered)


def print_result(result, maze):
    print(f"\n--- {result['name']} ---")
    if result["path"]:
        print(render_maze(maze, result["path"]))
        print("Path:", " -> ".join(map(str, result["path"])))
        print(f"Path length (moves): {result['path_length']}")
    else:
        print("No path found.")
        print("Path length: N/A")
    print(f"Expanded nodes: {result['expanded']}")
    print(f"Elapsed time: {result['elapsed_ms']:.4f} ms")


def main():
    maze = [row[:] for row in MAZE]
    # Keep S/G in the maze representation, but both are traversable cells.
    print("Grid-Based Maze Pathfinding Engine (BFS vs. DFS)")
    print(f"Grid: {len(maze)} x {len(maze[0])}; DFS depth limit: {DEPTH_LIMIT}")

    results = [
        run_algorithm("BFS", bfs, maze, START, GOAL),
        run_algorithm(
            "Depth-Limited DFS",
            lambda grid, start, goal: dfs(
                grid, start, goal, depth_limit=DEPTH_LIMIT
            ),
            maze,
            START,
            GOAL,
        ),
    ]
    for result in results:
        print_result(result, maze)

    print("\n--- Comparison ---")
    print(f"{'Algorithm':<22} {'Time (ms)':>12} {'Expanded':>10} {'Moves':>8}")
    for result in results:
        moves = str(result["path_length"]) if result["path_length"] is not None else "N/A"
        print(
            f"{result['name']:<22} {result['elapsed_ms']:>12.4f} "
            f"{result['expanded']:>10} {moves:>8}"
        )
    print("\nNote: timings depend on the machine and current run.")


if __name__ == "__main__":
    main()
