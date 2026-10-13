"""Breadth-First Search and shared grid/path utilities for the maze solver."""
from collections import deque

# Four-direction movement: up, down, left, right.
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def get_neighbors(maze, node):
    """Return reachable, non-wall neighboring cells within grid boundaries."""
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    r, c = node
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
            neighbors.append((nr, nc))
    return neighbors


def validate_maze(maze, start, goal):
    """Raise ValueError if the maze or endpoints are invalid."""
    if not maze or not maze[0]:
        raise ValueError("Maze must be a non-empty rectangular grid.")
    width = len(maze[0])
    if any(len(row) != width for row in maze):
        raise ValueError("All maze rows must have the same width.")
    for label, point in (("start", start), ("goal", goal)):
        r, c = point
        if not (0 <= r < len(maze) and 0 <= c < width):
            raise ValueError(f"{label} coordinate is outside the maze.")
        if maze[r][c] == "#":
            raise ValueError(f"{label} coordinate cannot be a wall.")


def reconstruct_path(parent, goal):
    """Reconstruct a path using parent pointers; return [] if unreachable."""
    if goal not in parent:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def bfs(maze, start, goal):
    """Return (shortest_path, expanded_nodes) using FIFO breadth-first search."""
    validate_maze(maze, start, goal)
    frontier = deque([start])
    parent = {start: None}
    expanded = 0

    while frontier:
        node = frontier.popleft()
        expanded += 1
        if node == goal:
            return reconstruct_path(parent, goal), expanded
        for neighbor in get_neighbors(maze, node):
            if neighbor not in parent:
                parent[neighbor] = node
                frontier.append(neighbor)
    return [], expanded
