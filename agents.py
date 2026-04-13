"""
Shadow Shift – agent definitions and behavior (Player, Predators, Neutrals).
PEAS: Sensors = limited perception of nearby tiles, obstacles, other agents.
       Actuators = player/agent movement.
Agent roles: Player (manual, switches); Predators (chase, local pathfinding, no overlap);
             Neutrals (wander, block paths).
"""
import random
from dataclasses import dataclass
<<<<<<< HEAD
from typing import Tuple, List, Sequence, Optional

from config import (
    DIRS_4,
    PREDATOR_VISION_RANGE,
    PREDATOR_SHADOW_VISION_RANGE,
    PREDATOR_BFS_MAX_EXPANSIONS,
    PREDATOR_LOS_MAX_NODES,
    PREDATOR_STALK_JITTER,
    PREDATOR_MEMORY_DECAY_TILES,
)
from grid import Grid
from pathfinding import bfs_first_step_toward, bfs_walkable_depth_map
=======
from typing import Tuple, List, Sequence

from config import (
    PREDATOR_VISION_RANGE,
    PREDATOR_SHADOW_VISION_RANGE,
    PREDATOR_BFS_MAX_EXPANSIONS,
)
from grid import Grid
from pathfinding import bfs_first_step_toward
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45


@dataclass
class Player:
    """Player agent: manual movement, reacts to threats, uses switches."""
    col: int
    row: int

    def move(self, dx: int, dy: int, grid: Grid) -> None:
        nc, nr = self.col + dx, self.row + dy
        if grid.is_walkable(nc, nr):
            self.col, self.row = nc, nr

    @property
    def position(self) -> Tuple[int, int]:
        return self.col, self.row


<<<<<<< HEAD
def _player_visible_to_predator(
    grid: Grid,
    pred_col: int,
    pred_row: int,
    player: Player,
) -> bool:
    """
    Line-of-sight along walkable tiles (walls block). Other agents do not block sight.
    In shadow, player is only visible within shorter graph distance.
    """
    px, py = player.position
    dm = bfs_walkable_depth_map(
        grid,
        (pred_col, pred_row),
        PREDATOR_VISION_RANGE,
        PREDATOR_LOS_MAX_NODES,
    )
    if (px, py) not in dm:
        return False
    d = dm[(px, py)]
    if grid.is_shadow(px, py):
        return d <= PREDATOR_SHADOW_VISION_RANGE
    return d <= PREDATOR_VISION_RANGE


=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
@dataclass
class Agent:
    """
    Autonomous agent: predator (chase with local perception) or neutral (wander).
    Avoids overlapping with others via shared occupied set.
<<<<<<< HEAD
    Predators keep last_seen_player for stalking when LOS is lost.
=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
    """
    col: int
    row: int
    color: Tuple[int, int, int]
    kind: str  # "predator" | "neutral"
<<<<<<< HEAD
    last_seen_player: Optional[Tuple[int, int]] = None
=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45

    @property
    def position(self) -> Tuple[int, int]:
        return self.col, self.row

    def possible_moves(
        self, grid: Grid, occupied: Sequence[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Sensors: walkable neighbor tiles not already occupied."""
<<<<<<< HEAD
        occ = set(occupied)
        neighbors = []
        for dc, dr in DIRS_4:
            nc, nr = self.col + dc, self.row + dr
            if grid.is_walkable(nc, nr) and (nc, nr) not in occ:
=======
        neighbors = []
        for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nc, nr = self.col + dc, self.row + dr
            if grid.is_walkable(nc, nr) and (nc, nr) not in set(occupied):
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
                neighbors.append((nc, nr))
        return neighbors

    def step_towards_player(
        self,
        grid: Grid,
        player: Player,
        occupied: Sequence[Tuple[int, int]],
    ) -> None:
        """
<<<<<<< HEAD
        Predator: graph-based LOS (walls block), memory of last seen position,
        BFS chase when visible, stalk toward memory or intercept toward exit when blind.
        """
        px, py = player.position

        if self.last_seen_player is not None:
            lpx, lpy = self.last_seen_player
            if abs(px - lpx) + abs(py - lpy) > PREDATOR_MEMORY_DECAY_TILES:
                self.last_seen_player = None

        visible = _player_visible_to_predator(grid, self.col, self.row, player)
        if visible:
            self.last_seen_player = (px, py)

        occ_no_player = [p for p in occupied if p != (px, py)]
        blocked = set(occ_no_player)

        if visible:
            nxt = bfs_first_step_toward(
                self.position,
                (px, py),
                grid,
                blocked,
                PREDATOR_BFS_MAX_EXPANSIONS,
            )
            if nxt is not None:
                self.col, self.row = nxt
                return
            moves = self.possible_moves(grid, occ_no_player)
            if not moves:
                return
            best = min(moves, key=lambda p: abs(p[0] - px) + abs(p[1] - py))
            self.col, self.row = best
            return

        if random.random() < PREDATOR_STALK_JITTER:
            self.step_random(grid, occupied)
            return

        if self.last_seen_player is not None:
            lx, ly = self.last_seen_player
            if grid.is_walkable(lx, ly):
                stalk = bfs_first_step_toward(
                    self.position,
                    (lx, ly),
                    grid,
                    blocked,
                    PREDATOR_BFS_MAX_EXPANSIONS,
                )
                if stalk is not None:
                    self.col, self.row = stalk
                    return

        gx, gy = grid.exit_col, grid.exit_row
        intercept = bfs_first_step_toward(
            self.position,
            (gx, gy),
            grid,
            blocked,
            max(60, PREDATOR_BFS_MAX_EXPANSIONS // 2),
        )
        if intercept is not None:
            self.col, self.row = intercept
            return

        moves = self.possible_moves(grid, occupied)
        if moves:
            self.col, self.row = min(moves, key=lambda p: abs(p[0] - gx) + abs(p[1] - gy))
            return
        self.step_random(grid, occupied)
=======
        Predator: chase player using local perception and greedy pathfinding.
        Limited vision range; reduced range when player is in shadow.
        """
        px, py = player.position
        distance = abs(self.col - px) + abs(self.row - py)

        if distance > PREDATOR_VISION_RANGE:
            self.step_random(grid, occupied)
            return
        if grid.is_shadow(px, py) and distance > PREDATOR_SHADOW_VISION_RANGE:
            self.step_random(grid, occupied)
            return

        # Player tile is a valid capture move; exclude only player from occupancy for pathing
        occ_no_player = [p for p in occupied if p != (px, py)]
        blocked = set(occ_no_player)
        nxt = bfs_first_step_toward(
            self.position,
            (px, py),
            grid,
            blocked,
            PREDATOR_BFS_MAX_EXPANSIONS,
        )
        if nxt is not None:
            self.col, self.row = nxt
            return

        moves = self.possible_moves(grid, occ_no_player)
        if not moves:
            return
        best = min(moves, key=lambda p: abs(p[0] - px) + abs(p[1] - py))
        self.col, self.row = best
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45

    def step_random(
        self, grid: Grid, occupied: Sequence[Tuple[int, int]]
    ) -> None:
        """Neutral: wander randomly; unintentionally blocks paths."""
        moves = self.possible_moves(grid, occupied)
        if not moves or random.random() < 0.2:
            return
        self.col, self.row = random.choice(moves)


def update_agents(
    agents: Sequence[Agent],
    player: Player,
    grid: Grid,
) -> None:
    """
    Advance all autonomous agents one step. Predators first, then neutrals.
    Occupied set prevents overlapping.
    """
    occupied: List[Tuple[int, int]] = [player.position]
    for agent in agents:
        if agent.kind == "predator":
            agent.step_towards_player(grid, player, occupied)
            occupied.append(agent.position)
    for agent in agents:
        if agent.kind == "neutral":
            agent.step_random(grid, occupied)
            occupied.append(agent.position)


def is_player_caught(agents: Sequence[Agent], player: Player) -> bool:
    """True if any predator shares the player's tile (loss condition)."""
    return any(
        agent.kind == "predator" and agent.position == player.position
        for agent in agents
    )


def auto_move_player(
    player: Player,
    grid: Grid,
    agents: Sequence[Agent],
) -> None:
    """
    Player policy (autonomous):
    - Prefer moves that maximize distance from the nearest predator.
    - Prefer shadow tiles for stealth.
<<<<<<< HEAD
    - Until every switch has been hit once, strongly prefer visiting remaining switches.
    - After all switches are done, bias toward the exit (when not in immediate danger).
=======
    - Small bonus for stepping on a switch to manipulate shadows.
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
    """
    predator_positions = [a.position for a in agents if a.kind == "predator"]
    occupied = {a.position for a in agents}

    # Candidate moves: four directions + staying still
    candidates = [(player.col, player.row)]
<<<<<<< HEAD
    for dc, dr in DIRS_4:
=======
    for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
        nc, nr = player.col + dc, player.row + dr
        if grid.is_walkable(nc, nr) and (nc, nr) not in occupied:
            candidates.append((nc, nr))

<<<<<<< HEAD
    ex, ey = grid.exit_col, grid.exit_row
    switches_done = grid.all_switches_pressed()

=======
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
    def score(cell: Tuple[int, int]) -> float:
        c, r = cell
        if predator_positions:
            nearest_predator = min(abs(c - pc) + abs(r - pr) for pc, pr in predator_positions)
        else:
            nearest_predator = 10

<<<<<<< HEAD
        dist_exit = abs(c - ex) + abs(r - ey)
        s = float(nearest_predator)
        if grid.is_shadow(c, r):
            s += 1.5
        if grid.switch_needs_visit(c, r):
            s += 6.0
        elif grid.is_switch(c, r):
            s += 0.4
        if not switches_done:
            for sc, sr in grid.switches:
                if (sc, sr) in grid.switches_pressed:
                    continue
                d = abs(c - sc) + abs(r - sr)
                s += max(0, 14 - d) * 0.35
            s += (10 - dist_exit) * 0.03
        else:
            if nearest_predator > 4:
                s += (28 - dist_exit) * 0.22
            else:
                s += (16 - dist_exit) * 0.06
=======
        s = float(nearest_predator)
        if grid.is_shadow(c, r):
            s += 1.5
        if grid.is_switch(c, r):
            s += 0.8
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
        if cell == player.position:
            s -= 0.2
        return s

    best_score = max(score(cell) for cell in candidates)
    best_moves = [cell for cell in candidates if score(cell) == best_score]
    chosen = random.choice(best_moves)
    player.col, player.row = chosen

    if grid.is_switch(*player.position):
<<<<<<< HEAD
        grid.press_switch(player.col, player.row)
=======
        grid.toggle_shadows()
>>>>>>> 58bbd3ee03c12ba2e1cea585802b4282f57f5c45
