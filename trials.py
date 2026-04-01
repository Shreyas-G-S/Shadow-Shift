#!/usr/bin/env python3
"""
Headless batch runs for Shadow Shift (no pygame).
Reports win rate and survival time distribution for the autonomous player.

Usage:
  python trials.py
  python trials.py --n 40 --seed 1
  python trials.py --n 100 --csv results.csv
"""
import argparse
import csv
import random
import statistics
import sys
from typing import List, Tuple

import config
from grid import Grid
from agents import Player, Agent, update_agents, is_player_caught, auto_move_player


def make_world() -> Tuple[Grid, Player, List[Agent]]:
    grid = Grid.simple_maze(config.GRID_COLS, config.GRID_ROWS)
    player = Player(col=1, row=1)
    agents: List[Agent] = [
        Agent(config.GRID_COLS - 2, 1, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS - 2, config.GRID_ROWS - 2, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS // 2, config.GRID_ROWS // 2, config.COLOR_NEUTRAL, "neutral"),
        Agent(2, config.GRID_ROWS - 2, config.COLOR_NEUTRAL, "neutral"),
    ]
    return grid, player, agents


def run_episode(max_steps: int = 100_000) -> Tuple[str, float, int]:
    """
    One episode: same step order as simulation (auto player, then agents).
    Time advances by STEP_INTERVAL_MS per step.
    Returns (outcome, elapsed_seconds, step_count) where outcome is win|lose.
    """
    grid, player, agents = make_world()
    dt = config.STEP_INTERVAL_MS / 1000.0
    t = 0.0
    steps = 0
    for _ in range(max_steps):
        auto_move_player(player, grid, agents)
        update_agents(agents, player, grid)
        steps += 1
        t += dt
        if is_player_caught(agents, player):
            return "lose", t, steps
        if t >= config.SURVIVE_SECONDS:
            return "win", t, steps
    return "timeout", t, steps


def ascii_histogram(values: List[float], bins: int = 8) -> str:
    if not values:
        return "(no data)"
    lo, hi = min(values), max(values)
    if hi <= lo:
        return f"[{lo:.1f}]  " + "#" * min(40, len(values))
    width = (hi - lo) / bins or 1.0
    counts = [0] * bins
    for v in values:
        i = min(bins - 1, int((v - lo) / width))
        counts[i] += 1
    mx = max(counts) or 1
    lines = []
    for i, c in enumerate(counts):
        left = lo + i * width
        bar = "#" * max(1, int(40 * c / mx))
        lines.append(f"  {left:5.1f}s–{left + width:5.1f}s  {bar} ({c})")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="Batch trials for Shadow Shift (headless)")
    p.add_argument("--n", type=int, default=30, help="number of episodes")
    p.add_argument("--seed", type=int, default=None, help="RNG seed (per-episode seed offsets)")
    p.add_argument("--csv", type=str, default=None, help="optional CSV output path")
    args = p.parse_args()

    wins = 0
    losses = 0
    timeouts = 0
    lose_times: List[float] = []
    rows = []

    for i in range(args.n):
        if args.seed is not None:
            random.seed(args.seed + i)
        outcome, t, steps = run_episode()
        rows.append({"episode": i, "outcome": outcome, "time_sec": round(t, 3), "steps": steps})
        if outcome == "win":
            wins += 1
        elif outcome == "lose":
            losses += 1
            lose_times.append(t)
        else:
            timeouts += 1

    print(f"Episodes: {args.n}  |  Wins: {wins}  Losses: {losses}  Timeouts: {timeouts}")
    print(f"Win rate: {100.0 * wins / args.n:.1f}%")
    if lose_times:
        print(f"Lose times (s): mean={statistics.mean(lose_times):.2f}  "
              f"median={statistics.median(lose_times):.2f}  "
              f"min={min(lose_times):.2f}  max={max(lose_times):.2f}")
        print("Histogram (survival time until caught):")
        print(ascii_histogram(lose_times))
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["episode", "outcome", "time_sec", "steps"])
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote {args.csv}")


if __name__ == "__main__":
    main()
    sys.exit(0)
