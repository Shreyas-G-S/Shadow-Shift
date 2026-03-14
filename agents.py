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

from config import PREDATOR_VISION_RANGE, PREDATOR_SHADOW_VISION_RANGE
from grid import Grid


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

        moves = self.possible_moves(grid, occupied)
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
