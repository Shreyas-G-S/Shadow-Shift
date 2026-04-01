"""
Shadow Shift – agent definitions and behavior (Player, Predators, Neutrals).
PEAS: Sensors = limited perception of nearby tiles, obstacles, other agents.
       Actuators = player/agent movement.
Agent roles: Player (manual, switches); Predators (chase, local pathfinding, no overlap);
             Neutrals (wander, block paths).
"""
import random
from dataclasses import dataclass
from typing import Tuple, List, Sequence

from config import (
    PREDATOR_VISION_RANGE,
    PREDATOR_SHADOW_VISION_RANGE,
    PREDATOR_BFS_MAX_EXPANSIONS,
)
from grid import Grid
from pathfinding import bfs_first_step_toward


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


@dataclass
class Agent:
    """
    Autonomous agent: predator (chase with local perception) or neutral (wander).
    Avoids overlapping with others via shared occupied set.
    """
    col: int
    row: int
    color: Tuple[int, int, int]
    kind: str  # "predator" | "neutral"

    @property
    def position(self) -> Tuple[int, int]:
        return self.col, self.row

    def possible_moves(
        self, grid: Grid, occupied: Sequence[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Sensors: walkable neighbor tiles not already occupied."""
        neighbors = []
        for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nc, nr = self.col + dc, self.row + dr
            if grid.is_walkable(nc, nr) and (nc, nr) not in set(occupied):
                neighbors.append((nc, nr))
        return neighbors

    def step_towards_player(
        self,
        grid: Grid,
        player: Player,
        occupied: Sequence[Tuple[int, int]],
    ) -> None:
        """
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
    - Small bonus for stepping on a switch to manipulate shadows.
    """
    predator_positions = [a.position for a in agents if a.kind == "predator"]
    occupied = {a.position for a in agents}

    # Candidate moves: four directions + staying still
    candidates = [(player.col, player.row)]
    for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nc, nr = player.col + dc, player.row + dr
        if grid.is_walkable(nc, nr) and (nc, nr) not in occupied:
            candidates.append((nc, nr))

    def score(cell: Tuple[int, int]) -> float:
        c, r = cell
        if predator_positions:
            nearest_predator = min(abs(c - pc) + abs(r - pr) for pc, pr in predator_positions)
        else:
            nearest_predator = 10

        s = float(nearest_predator)
        if grid.is_shadow(c, r):
            s += 1.5
        if grid.is_switch(c, r):
            s += 0.8
        if cell == player.position:
            s -= 0.2
        return s

    best_score = max(score(cell) for cell in candidates)
    best_moves = [cell for cell in candidates if score(cell) == best_score]
    chosen = random.choice(best_moves)
    player.col, player.row = chosen

    if grid.is_switch(*player.position):
        grid.toggle_shadows()
