"""Iterative depth-limited Depth-First Search for the maze solver."""
from bfs import get_neighbors, reconstruct_path, validate_maze


def dfs(maze, start, goal, depth_limit=200):
    """Return (path, expanded_nodes) using a LIFO stack and depth limit.

    The limit counts moves from the start. DFS does not guarantee a shortest
    path. A per-path visited set prevents cycles while still allowing a cell
    to be reached through a different route.
    """
    validate_maze(maze, start, goal)
    if depth_limit < 0:
        raise ValueError("depth_limit must be zero or greater")

    # Stack entries: (current node, depth, path tuple).
    stack = [(start, 0, (start,))]
    expanded = 0

    while stack:
        node, depth, path = stack.pop()
        expanded += 1
        if node == goal:
            parent = {path[0]: None}
            for previous, current in zip(path, path[1:]):
                parent[current] = previous
            return reconstruct_path(parent, goal), expanded
        if depth >= depth_limit:
            continue

        path_set = set(path)
        # Reverse order so the first listed direction is explored first.
        for neighbor in reversed(get_neighbors(maze, node)):
            if neighbor not in path_set:
                stack.append((neighbor, depth + 1, path + (neighbor,)))
    return [], expanded
