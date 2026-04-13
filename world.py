"""
Single place to build maze + player + agents (simulation and trials stay in sync).
"""
from typing import List, Tuple

import config
from grid import Grid
from agents import Player, Agent


def create_world() -> Tuple[Grid, Player, List[Agent]]:
    """Fresh maze, player spawn, and default agent roster."""
    grid = Grid.simple_maze(config.GRID_COLS, config.GRID_ROWS)
    player = Player(col=1, row=1)
    agents: List[Agent] = [
        Agent(config.GRID_COLS - 2, 1, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS - 2, config.GRID_ROWS - 2, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS // 2, config.GRID_ROWS // 2, config.COLOR_NEUTRAL, "neutral"),
        Agent(2, config.GRID_ROWS - 2, config.COLOR_NEUTRAL, "neutral"),
    ]
    return grid, player, agents
