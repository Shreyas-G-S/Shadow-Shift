"""
Shadow Shift – grid environment (maze, corridors, dynamic lighting, switches).
PEAS: Environment = grid-based maze with corridors, dynamic lighting, moving obstacles.
       Actuators = switches to manipulate shadow zones.
"""
from dataclasses import dataclass
<<<<<<< HEAD
from typing import Tuple, List, Set
=======
from typing import Tuple, List
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45


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
<<<<<<< HEAD
    switches_pressed: Set[Tuple[int, int]]  # each switch tile hit at least once (exit win gate)
    shadow_rows: List[int]      # row indices that can be the active shadow corridor
    current_shadow_index: int
    exit_col: int
    exit_row: int
=======
    shadow_rows: List[int]      # row indices that can be the active shadow corridor
    current_shadow_index: int
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45

    @classmethod
    def simple_maze(cls, cols: int, rows: int) -> "Grid":
        """
<<<<<<< HEAD
        Build a simple maze with corridors, shadow rows (cycled by switches), switches,
        and an exit goal tile.
=======
        Build a simple maze with corridors, one active shadow corridor, and switches.
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
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

<<<<<<< HEAD
        def row_has_corridor_floor(r: int) -> bool:
            return 0 <= r < rows and any(tiles[r][x] == 0 for x in range(3, cols - 3))

        # Three shadow corridor candidates (dynamic lighting; switches cycle all)
        row_a = rows // 2
        row_b = max(1, min(rows - 2, row_a + 2))
        row_c = max(1, min(rows - 2, (2 * rows) // 3 - 1))
        shadow_rows: List[int] = []
        for r in (row_a, row_b, row_c):
            if r not in shadow_rows and row_has_corridor_floor(r):
                shadow_rows.append(r)
        if len(shadow_rows) < 3:
            for r in range(1, rows - 1):
                if r not in shadow_rows and row_has_corridor_floor(r):
                    shadow_rows.append(r)
                if len(shadow_rows) >= 3:
                    break
        if not shadow_rows:
            shadow_rows = [max(1, min(rows - 2, row_a))]

=======
        # Two possible shadow corridor rows (dynamic lighting)
        row_a = rows // 2
        row_b = max(1, min(rows - 2, row_a + 2))
        shadow_rows = [row_a, row_b]
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
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

<<<<<<< HEAD
        forbidden: Set[Tuple[int, int]] = {(1, 1), *switches}
        exit_col, exit_row = cls._pick_exit_tile(cols, rows, tiles, forbidden)

=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
        return cls(
            cols=cols,
            rows=rows,
            tiles=tiles,
            shadows=shadows,
            switches=switches,
<<<<<<< HEAD
            switches_pressed=set(),
            shadow_rows=shadow_rows,
            current_shadow_index=current_shadow_index,
            exit_col=exit_col,
            exit_row=exit_row,
        )

    @staticmethod
    def _pick_exit_tile(
        cols: int,
        rows: int,
        tiles: List[List[int]],
        forbidden: Set[Tuple[int, int]],
    ) -> Tuple[int, int]:
        """Place exit on floor, away from spawn; prefer bottom-right area."""
        for c in range(cols - 2, 2, -1):
            for r in range(rows - 2, 2, -1):
                if tiles[r][c] != 0:
                    continue
                if (c, r) in forbidden:
                    continue
                return c, r
        return cols - 3, rows - 3

    def _in_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self.cols and 0 <= row < self.rows

    def is_walkable(self, col: int, row: int) -> bool:
        if not self._in_bounds(col, row):
=======
            shadow_rows=shadow_rows,
            current_shadow_index=current_shadow_index,
        )

    def is_walkable(self, col: int, row: int) -> bool:
        if not (0 <= col < self.cols and 0 <= row < self.rows):
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
            return False
        return self.tiles[row][col] == 0

    def is_shadow(self, col: int, row: int) -> bool:
<<<<<<< HEAD
        if not self._in_bounds(col, row):
=======
        if not (0 <= col < self.cols and 0 <= row < self.rows):
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
            return False
        return self.shadows[row][col] == 1

    def is_switch(self, col: int, row: int) -> bool:
        return (col, row) in self.switches

<<<<<<< HEAD
    def is_exit(self, col: int, row: int) -> bool:
        return col == self.exit_col and row == self.exit_row

    def switch_needs_visit(self, col: int, row: int) -> bool:
        return self.is_switch(col, row) and (col, row) not in self.switches_pressed

    def all_switches_pressed(self) -> bool:
        return all(s in self.switches_pressed for s in self.switches)

    def switches_hit_count(self) -> int:
        return sum(1 for s in self.switches if s in self.switches_pressed)

    def press_switch(self, col: int, row: int) -> None:
        """Record switch visit and cycle shadow corridor (dynamic lighting)."""
        if not self.is_switch(col, row):
            return
        self.switches_pressed.add((col, row))
        self.toggle_shadows()

=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
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
