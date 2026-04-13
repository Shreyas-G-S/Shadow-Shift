"""
Unit tests for Grid (walkability, toggle_shadows) and pathfinding BFS on a fixed maze.
Run: python -m unittest discover -s tests -v
"""
import unittest
from typing import Set, Tuple

from grid import Grid
from pathfinding import bfs_first_step_toward, bfs_walkable_depth_map


def _make_walled_box(rows: int, cols: int) -> list[list[int]]:
    """Border walls, interior floor."""
    t = [[1] * cols for _ in range(rows)]
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            t[r][c] = 0
    return t


def _make_toggle_grid() -> Grid:
    """Minimal grid with two shadow rows so toggle_shadows alternates lighting."""
    rows, cols = 8, 12
    tiles = _make_walled_box(rows, cols)
    shadows = [[0] * cols for _ in range(rows)]
    shadow_rows = [2, 5]
    active = shadow_rows[0]
    for x in range(3, cols - 3):
        if tiles[active][x] == 0:
            shadows[active][x] = 1
    return Grid(
        cols=cols,
        rows=rows,
        tiles=tiles,
        shadows=shadows,
        switches=[(2, 2)],
        switches_pressed=set(),
        shadow_rows=shadow_rows,
        current_shadow_index=0,
        exit_col=cols - 2,
        exit_row=rows - 2,
    )


def _make_bfs_maze_grid() -> Grid:
    """
    Fixed 5x5 maze (walls block); start (1,1), goal (3,3), center (2,2) is wall.
    #####
    #...#
    #.#.#
    #...#
    #####
    """
    rows, cols = 5, 5
    tiles = [[1] * cols for _ in range(rows)]
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            tiles[r][c] = 0
    tiles[2][2] = 1
    shadows = [[0] * cols for _ in range(rows)]
    return Grid(
        cols=cols,
        rows=rows,
        tiles=tiles,
        shadows=shadows,
        switches=[],
        switches_pressed=set(),
        shadow_rows=[2],
        current_shadow_index=0,
        exit_col=3,
        exit_row=3,
    )


class TestGridIsWalkable(unittest.TestCase):
    def test_out_of_bounds_not_walkable(self):
        g = _make_toggle_grid()
        self.assertFalse(g.is_walkable(-1, 2))
        self.assertFalse(g.is_walkable(g.cols, 2))
        self.assertFalse(g.is_walkable(2, -1))
        self.assertFalse(g.is_walkable(2, g.rows))

    def test_wall_not_walkable_floor_walkable(self):
        g = _make_toggle_grid()
        self.assertFalse(g.is_walkable(0, 2))  # border wall
        self.assertTrue(g.is_walkable(1, 2))  # interior floor

    def test_bfs_maze_center_wall(self):
        g = _make_bfs_maze_grid()
        self.assertFalse(g.is_walkable(2, 2))
        self.assertTrue(g.is_walkable(1, 1))
        self.assertTrue(g.is_walkable(3, 3))


class TestGridToggleShadows(unittest.TestCase):
    def test_toggle_cycles_shadow_row(self):
        g = _make_toggle_grid()
        self.assertEqual(g.current_shadow_index, 0)
        row0 = g.shadow_rows[0]
        row1 = g.shadow_rows[1]
        self.assertTrue(any(g.is_shadow(c, row0) for c in range(g.cols)))
        self.assertFalse(any(g.is_shadow(c, row1) for c in range(g.cols)))

        g.toggle_shadows()
        self.assertEqual(g.current_shadow_index, 1)
        self.assertFalse(any(g.is_shadow(c, row0) for c in range(g.cols)))
        self.assertTrue(any(g.is_shadow(c, row1) for c in range(g.cols)))

        g.toggle_shadows()
        self.assertEqual(g.current_shadow_index, 0)
        self.assertTrue(any(g.is_shadow(c, row0) for c in range(g.cols)))

    def test_toggle_empty_shadow_rows_no_crash(self):
        g = Grid(
            cols=4,
            rows=4,
            tiles=_make_walled_box(4, 4),
            shadows=[[0] * 4 for _ in range(4)],
            switches=[],
            switches_pressed=set(),
            shadow_rows=[],
            current_shadow_index=0,
            exit_col=2,
            exit_row=2,
        )
        g.toggle_shadows()
        self.assertEqual(g.current_shadow_index, 0)


class TestBfsFixedMaze(unittest.TestCase):
    def test_first_step_around_center_wall(self):
        g = _make_bfs_maze_grid()
        start = (1, 1)
        goal = (3, 3)
        blocked: Set[Tuple[int, int]] = set()
        nxt = bfs_first_step_toward(start, goal, g, blocked, max_expansions=50)
        self.assertEqual(nxt, (2, 1))

    def test_depth_map_wall_blocks_longer_path(self):
        g = _make_bfs_maze_grid()
        dm = bfs_walkable_depth_map(g, (1, 1), max_depth=10, max_nodes=100)
        self.assertIn((1, 1), dm)
        self.assertEqual(dm[(1, 1)], 0)
        self.assertIn((3, 3), dm)
        # Path (1,1)->(2,1)->(3,1)->(3,2)->(3,3) has length 4
        self.assertEqual(dm[(3, 3)], 4)
        self.assertNotIn((2, 2), dm)  # wall cell not in walkable map


if __name__ == "__main__":
    unittest.main()
