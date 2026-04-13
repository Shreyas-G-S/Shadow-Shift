"""
Shortest-path helper for grid movement (BFS).
Used by predators only when the player is within vision (local planning).
"""
from collections import deque
from typing import Dict, Optional, Set, Tuple

<<<<<<< HEAD
import config
from grid import Grid


def bfs_walkable_depth_map(
    grid: Grid,
    start: Tuple[int, int],
    max_depth: int,
    max_nodes: int,
) -> Dict[Tuple[int, int], int]:
    """
    Shortest-path distances from `start` over walkable tiles only (walls block).
    Used for predator line-of-sight: only tiles within `max_depth` steps are returned.
    Other agents do not block sight (simplification).
    """
    sc, sr = start
    dist: Dict[Tuple[int, int], int] = {(sc, sr): 0}
    q = deque([(sc, sr)])
    nodes = 0
    while q and nodes < max_nodes:
        c, r = q.popleft()
        nodes += 1
        d = dist[(c, r)]
        if d >= max_depth:
            continue
        for dc, dr in config.DIRS_4:
            nc, nr = c + dc, r + dr
            if not grid.is_walkable(nc, nr):
                continue
            nd = d + 1
            if (nc, nr) not in dist:
                dist[(nc, nr)] = nd
                q.append((nc, nr))

    return dist


=======
from grid import Grid


>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
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
<<<<<<< HEAD
=======
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45

    while q and expansions < max_expansions:
        c, r = q.popleft()
        expansions += 1
<<<<<<< HEAD
        for dc, dr in config.DIRS_4:
=======
        for dc, dr in dirs:
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
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
