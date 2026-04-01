"""
Shortest-path helper for grid movement (BFS).
Used by predators only when the player is within vision (local planning).
"""
from collections import deque
from typing import Dict, Optional, Set, Tuple

from grid import Grid


def bfs_first_step_toward(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid: Grid,
    blocked: Set[Tuple[int, int]],
    max_expansions: int,
) -> Optional[Tuple[int, int]]:
    """
    First grid step from `start` along a shortest walkable path to `goal`.
    Cells in `blocked` cannot be entered except `goal` itself.
    Returns None if unreachable within expansion budget.
    """
    if start == goal:
        return None

    q = deque([start])
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    expansions = 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q and expansions < max_expansions:
        c, r = q.popleft()
        expansions += 1
        for dc, dr in dirs:
            nc, nr = c + dc, r + dr
            if not grid.is_walkable(nc, nr):
                continue
            if (nc, nr) in blocked and (nc, nr) != goal:
                continue
            if (nc, nr) in parent or (nc, nr) == start:
                continue
            parent[(nc, nr)] = (c, r)
            if (nc, nr) == goal:
                cur: Tuple[int, int] = goal
                while parent[cur] != start:
                    cur = parent[cur]
                return cur
            q.append((nc, nr))

    return None
