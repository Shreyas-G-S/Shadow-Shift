"""
Shared win/lose evaluation for simulation and headless trials (single source of truth).
"""
from typing import Sequence, Tuple

import config
from grid import Grid
from agents import Player, Agent, is_player_caught


def evaluate_round(
    grid: Grid,
    player: Player,
    agents: Sequence[Agent],
    elapsed_sec: float,
) -> Tuple[bool, bool, str]:
    """
    Returns (won, lost, win_kind).
    win_kind is 'exit', 'time', or '' (ignored if not won).
    Loss beats win if a predator shares the player's tile.
    """
    if is_player_caught(agents, player):
        return False, True, ""
    if grid.is_exit(*player.position) and grid.all_switches_pressed():
        return True, False, "exit"
    if elapsed_sec >= config.SURVIVE_SECONDS:
        return True, False, "time"
    return False, False, ""
