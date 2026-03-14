"""
Shadow Shift – grid environment (maze, corridors, dynamic lighting, switches).
PEAS: Environment = grid-based maze with corridors, dynamic lighting, moving obstacles.
       Actuators = switches to manipulate shadow zones.
"""
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Grid:
    """
    Grid-based maze: tiles (walls/floors), shadow zones, and switch positions.
    No pygame dependency; pure state and logic for explainability.
    """
    cols: int
    rows: int
    tiles: List[List[int]]      # 1 = wall, 0 = floor
    shadows: List[List[int]]    # 1 = in shadow
    switches: List[Tuple[int, int]]
    shadow_rows: List[int]      # row indices that can be the active shadow corridor
    current_shadow_index: int

    @classmethod
    def simple_maze(cls, cols: int, rows: int) -> "Grid":
        """
        Build a simple maze with corridors, one active shadow corridor, and switches.
        """
        tiles = [[0 for _ in range(cols)] for _ in range(rows)]
        shadows = [[0 for _ in range(cols)] for _ in range(rows)]

        # Outer border walls
        for x in range(cols):
            tiles[0][x] = 1
            tiles[rows - 1][x] = 1
        for y in range(rows):
            tiles[y][0] = 1
            tiles[y][cols - 1] = 1

        # Internal walls to form corridors
        for x in range(2, cols - 2):
            if x % 3 == 0:
                tiles[rows // 3][x] = 1
            if x % 4 == 0:
                tiles[(2 * rows) // 3][x] = 1

        # Two possible shadow corridor rows (dynamic lighting)
        row_a = rows // 2
        row_b = max(1, min(rows - 2, row_a + 2))
        shadow_rows = [row_a, row_b]
        current_shadow_index = 0
        active_row = shadow_rows[current_shadow_index]
        for x in range(3, cols - 3):
            if tiles[active_row][x] == 0:
                shadows[active_row][x] = 1

        # Switch tiles: stepping on one toggles which row is shadowed
        switches: List[Tuple[int, int]] = [
            (2, row_a),
            (cols - 3, row_a),
        ]

        return cls(
            cols=cols,
            rows=rows,
            tiles=tiles,
            shadows=shadows,
            switches=switches,
            shadow_rows=shadow_rows,
            current_shadow_index=current_shadow_index,
        )

    def is_walkable(self, col: int, row: int) -> bool:
        if not (0 <= col < self.cols and 0 <= row < self.rows):
            return False
        return self.tiles[row][col] == 0

    def is_shadow(self, col: int, row: int) -> bool:
        if not (0 <= col < self.cols and 0 <= row < self.rows):
            return False
        return self.shadows[row][col] == 1

    def is_switch(self, col: int, row: int) -> bool:
        return (col, row) in self.switches

    def toggle_shadows(self) -> None:
        """Cycle to the next shadow corridor row (actuator: switch)."""
        if not self.shadow_rows:
            return
        self.current_shadow_index = (self.current_shadow_index + 1) % len(self.shadow_rows)
        for r in range(self.rows):
            for c in range(self.cols):
                self.shadows[r][c] = 0
        active_row = self.shadow_rows[self.current_shadow_index]
        for x in range(3, self.cols - 3):
            if self.tiles[active_row][x] == 0:
                self.shadows[active_row][x] = 1
