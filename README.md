# Shadow Shift

A **multi-agent grid maze** game in Python where the player, predators, and neutrals share a dynamic environment with **shadow corridors** and **switches**. The design follows the project proposal’s focus on **local perception**, **simple rules**, and **emergent interaction**—no central planner coordinates the whole maze.

---

## Core principles

### Multi-agent design

| Idea | In this codebase |
|------|------------------|
| **Decentralized control** | Each agent type runs its own policy each step: human or `auto_move_player` for the player, `step_towards_player` / `step_random` for AI agents. |
| **Shared environment** | All agents read the same `Grid` (walls, shadows, exit, switches) and respect occupancy so entities do not overlap (except predator catching the player). |
| **Emergent behavior** | Global patterns (flanking, bottlenecks, losing line-of-sight) arise from **local** chase, random walk, shadow rules, and turn order—not from a single “maze brain.” |

### PEAS (high level)

| PEAS | Shadow Shift |
|------|----------------|
| **Performance** | Survival time; successful avoidance; optional win by **exit** after hitting all **switches**, or **time** survival. |
| **Environment** | Grid maze, corridors, **dynamic lighting** (shadow rows), moving agents (predators + neutrals). |
| **Actuators** | Grid moves (player and agents); **switches** cycle which row is shadowed (`Grid.press_switch` / `toggle_shadows`). |
| **Sensors** | **Limited**: predators use graph-based **line-of-sight** (walls block), shadow reduces effective range, **last-seen memory** when blind; neutrals only see walkable neighbors and occupancy. |

### Separation of concerns (architecture)

- **Environment state** is separate from **rendering** (pygame lives only in `simulation.py`).
- **Win/lose rules** live in one place (`game_rules.py`) so the **game** and **headless trials** stay consistent.
- **World construction** is centralized (`world.py`) so simulation and batch runs use the same spawns.

---

## Repository map (how to navigate the code)

Read in this order for a full picture: **`config` → `grid` → `agents` / `pathfinding` → `game_rules` / `world` → `simulation`**.

| File | Role |
|------|------|
| **`main.py`** | Entry point: calls `simulation.run()`. |
| **`config.py`** | Window size, grid size, colors, predator perception limits, `SURVIVE_SECONDS`, `STEP_INTERVAL_MS`, `AUTO_PLAYER`, shared `DIRS_4`. **Tune difficulty here.** |
| **`grid.py`** | **`Grid`**: maze tiles, shadow mask, switches, exit tile, `press_switch`, `toggle_shadows`, walkability / shadow / exit queries. |
| **`pathfinding.py`** | **`bfs_walkable_depth_map`** (LOS / distances), **`bfs_first_step_toward`** (shortest-path first step with a step budget). |
| **`agents.py`** | **`Player`**, **`Agent`** (predator / neutral), **`update_agents`**, **`is_player_caught`**, **`auto_move_player`**, predator LOS + memory + stalk/intercept behavior. |
| **`game_rules.py`** | **`evaluate_round(...)`** → `(won, lost, win_kind)` for loss, exit win, or time win. Single source of truth for rules. |
| **`world.py`** | **`create_world()`** → new `Grid.simple_maze`, player at `(1,1)`, default predator/neutral list. |
| **`simulation.py`** | Pygame: event loop, discrete steps, drawing, HUD, restart (`R` / `Q`), uses `create_world` + `evaluate_round`. |
| **`trials.py`** | Headless episodes for stats; same step order as the game; optional CSV export. |
| **`plot_results.py`** | Reads a trials CSV and writes PNG figures under `figures/` (requires matplotlib). |
| **`tests/test_grid_pathfinding.py`** | Unit tests for `Grid` walkability / `toggle_shadows` and BFS on a fixed small maze. |
| **`shadow_shift.md`** | Original project proposal (concept document). |

**Data flow (one frame / step):**

1. Input (optional): manual move **or** `auto_move_player`.
2. `update_agents` (predators, then neutrals).
3. `evaluate_round` → win/lose/time.

---

## How to run

### 1. Prerequisites

- **Python 3.10+** recommended (stdlib `unittest`, typing).
- A virtual environment is optional but good practice.

### 2. Install dependencies

From the project root (`shadow_shift/`):

```bash
pip install -r requirements.txt
```

This installs **pygame** (game) and **matplotlib** (plotting). **`main.py`** / **`simulation.py`** require pygame; **`trials.py`** and **`tests/`** do not. **`plot_results.py`** requires matplotlib only.

### 3. Run the game

```bash
python main.py
```

or:

```bash
python3 main.py
```

- **`AUTO_PLAYER`** in `config.py`:  
  - `True` → autonomous player policy.  
  - `False` → **arrow keys** or **WASD**, **one key = one tile**; switches activate when you step on them.

After a win or loss: **`R`** or **Enter** restarts, **`Q`** or **Esc** quits (when the end-game overlay is shown or from the main loop as implemented).

### 4. Headless trials (statistics)

```bash
python trials.py
python trials.py --n 100 --seed 0
python trials.py --n 50 --csv results.csv
```

Prints win rate and optional histogram of lose times; CSV columns include `episode`, `outcome`, `win_kind`, `time_sec`, `steps`.

### 5. Plot figures from CSV

After you have `results.csv` (or another export):

```bash
python plot_results.py results.csv
python plot_results.py results.csv --out figures
```

PNG files are written to the chosen folder (default `figures/`). If matplotlib cache warnings appear, you can set `MPLCONFIGDIR` to a writable folder inside the project.

### 6. Unit tests

```bash
python -m unittest discover -s tests -v
```

---

## Win conditions (summary)

- **Lose**: any **predator** occupies the same tile as the **player**.
- **Win (exit)**: player stands on the **exit** (green outline) **and** every **switch** has been stepped on at least once this run.
- **Win (time)**: elapsed time reaches **`SURVIVE_SECONDS`** without being caught.

Rules are implemented in **`game_rules.evaluate_round`**.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| `ModuleNotFoundError: pygame` | Run `pip install -r requirements.txt` in the same Python you use to run `main.py`. |
| Imports unresolved in the IDE | Open the **`shadow_shift`** folder as the workspace root; `pyrightconfig.json` helps analysis. |
| Plot script errors | Install matplotlib; use **`Agg`** backend (already set in `plot_results.py`) for headless runs. |

---

## License / course use

This repository is built for an academic **multi-agent systems** style project. Adapt the text in **`shadow_shift.md`** and **`FinalProgressReport.md`** for your submission as required by your instructor.
