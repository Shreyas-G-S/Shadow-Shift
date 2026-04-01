# Shadow Shift – Final Progress Report


---

## Implemented code

Shadow Shift is a **multi-agent grid maze** in Python with **pygame** for visualization. The codebase is split so the **environment**, **agents**, **pathfinding**, and **simulation loop** are easy to explain and map to the project proposal (PEAS, roles, survival objective).

### `main.py`

Entry point only: imports `run()` from `simulation.py` and starts the game. Keeps startup simple and separates “how to run” from game logic.

### `config.py`

Central configuration: window size, FPS, grid dimensions (`GRID_COLS`, `GRID_ROWS`, `TILE_SIZE`), colors, **predator perception** (`PREDATOR_VISION_RANGE`, `PREDATOR_SHADOW_VISION_RANGE`), **local BFS cap** (`PREDATOR_BFS_MAX_EXPANSIONS`), **game goal** (`SURVIVE_SECONDS`), **step timing** (`STEP_INTERVAL_MS`), and **`AUTO_PLAYER`** (autonomous vs manual player). Tuning difficulty and demos without editing behavior code.

### `grid.py`

**Environment model** (no pygame):

- **`Grid`** holds the maze (`tiles`: wall vs floor), **shadow mask** (`shadows`), **switch positions**, and which **shadow corridor row** is active (`shadow_rows`, `current_shadow_index`).
- **`Grid.simple_maze(...)`** builds a bordered maze with internal walls, initializes one shadow corridor, and places switches.
- **`is_walkable`**, **`is_shadow`**, **`is_switch`**: queries used by agents and rendering.
- **`toggle_shadows()`**: cycles the active shadow row—implements the **actuator** “switches manipulate shadow zones.”

### `agents.py`

**Agent model and step logic:**

- **`Player`**: grid position; **`move(dx, dy, grid)`** for one-tile moves respecting walls.
- **`Agent`**: `kind` is `"predator"` or `"neutral"`; **`possible_moves`** returns walkable neighbors not blocked by occupied tiles (local obstacle sensing).
- **Predators** – **`step_towards_player`**: if the player is outside vision, or in shadow beyond reduced range, the predator **wanders**; if the player is visible, it uses **`pathfinding.bfs_first_step_toward`** (shortest path, capped) with **`occ_no_player`** so the **player tile can be entered** (capture). If BFS fails within the cap, **greedy** one-step chase is used.
- **Neutrals** – **`step_random`**: constrained random walk (sometimes stay still), which can **block corridors** without a global plan.
- **`update_agents`**: moves **predators first**, then **neutrals**, maintaining an **occupied** list so agents do not overlap each other (except predator-on-player handled via pathing).
- **`is_player_caught`**: loss if any predator shares the player’s tile.
- **`auto_move_player`**: autonomous player policy—scores moves by distance from nearest predator, bonus for shadow and switches, then toggles shadows if landing on a switch.

### `pathfinding.py`

**Breadth-first search (BFS)** on the grid: from a start cell toward a goal, respecting walls and a **blocked** set (other agents), with **`max_expansions`** to keep search **local**. Returns the **first step** along a shortest discovered path, or `None` if the goal is not reached in time.

### `simulation.py`

**Controller + view:**

- **`create_world()`**: builds a fresh `Grid`, `Player`, and list of `Agent` instances (used at startup and on restart).
- **Drawing**: `draw_grid`, `draw_player`, `draw_agents` (walls, floors, shadows, switches, entities).
- **`handle_keydown`**: manual mode—one key press, one tile; switches toggle shadows on landing.
- **`run()`**: pygame init, main loop with **`STEP_INTERVAL_MS`** accumulation; each step optionally runs **`auto_move_player`**, then **`update_agents`**; win/lose checks; HUD (countdown or final time); **game-over overlay** with restart/quit hints.

### `trials.py`

**Headless evaluation** (no pygame): repeats episodes with the **auto player**, same step order as the game, reports **win rate**, **lose-time statistics**, an **ASCII histogram**, and optional **`--csv`** export (e.g. for spreadsheets or charts).

### `pyrightconfig.json`

Tells the type checker / IDE to treat the project root as the Python environment root, improving resolution of imports like `config`, `grid`, and `agents`.

### Supporting files

- **`requirements.txt`**: `pygame` dependency.
- **`shadow_shift.md`**: original project proposal (unchanged).
- **`results.csv`**: optional output from `trials.py` for analysis.

---

## Changes made

### Auto agent and manual/auto toggle

- Added an **autonomous player policy** (`auto_move_player` in `agents.py`) so the game can run **without keyboard input**.
- Added **`AUTO_PLAYER`** in `config.py` (`True` = auto, `False` = manual arrows/WASD, one key = one tile).
- **`simulation.py`** runs the auto policy each simulation step only when `AUTO_PLAYER` is true; manual input uses `handle_keydown` when `AUTO_PLAYER` is false.

### Predator pathfinding (local BFS) – `pathfinding.py` + `agents.py`

When a predator can see the player, it takes the **first step** of a **shortest path (BFS)** around walls, capped by **`PREDATOR_BFS_MAX_EXPANSIONS`** in `config.py`. If BFS hits the cap, it falls back to the **old greedy** move.

**Bugfix:** Predators can **step onto the player’s tile (capture)** by treating the player cell as allowed while pathing (**`occ_no_player`**).

### Game over + restart – `simulation.py`

After win/lose the loop **pauses**; shows time and **“Press R to play again”**. **R** or **Enter** restarts with **`create_world()`**. **Q** or **Esc** quits. Bottom hint line: **R restart Q quit** (+ movement hint in manual mode).

**Win timing:** Inside the step loop, **`sim_elapsed`** is read from the clock **each step** so multi-step frames don’t delay a win.

### Headless trials – `trials.py`

No pygame: runs **N** episodes with the auto player, prints **win rate**, **lose-time stats**, and a simple **ASCII histogram**. Optional **`--csv results.csv`**.

Example:

```bash
python3 trials.py --n 40 --seed 1
```

### Pyright – `pyrightconfig.json`

Helps the IDE resolve local imports like `config`, `grid`, `agents`.

### Other changes (architecture and behavior)

- **Refactor from a single large `main.py`** into **`config`**, **`grid`**, **`agents`**, **`simulation`**, and thin **`main`** entry—matches a clear “environment / agents / simulation” story for reports and demos.
- **Discrete simulation steps** via **`STEP_INTERVAL_MS`** so auto and agent updates are readable and aligned with **`trials.py`**.
- **`create_world()`** centralizes spawn layout so **restart** matches initial state.
- **Progress Report 1** items addressed in code: **BFS-style predator movement** within perception, and a path to **measure performance** via **`trials.py`** and CSV.

---

## Improvements before final submission

Suggested enhancements that would strengthen the demo, write-up, and alignment with “emergent multi-agent” language:

1. **Documentation bundle**  
   Short **README** with install (`pip install -r requirements.txt`), run (`python main.py`), `AUTO_PLAYER`, controls, and **`python trials.py --n …`**. One paragraph mapping **PEAS** to file/function names.

2. **Figures from `results.csv`**  
   Plot win rate or survival-time distribution (spreadsheet or matplotlib) and **paste one figure** into the final report with a one-sentence takeaway.

3. **Emergent behavior narrative**  
   Short bullet list of **observable** patterns (e.g. neutrals blocking a chase, shadow + switch breaking line-of-sight, two predators interfering in a corridor) tied to **local rules** only—no central planner.

4. **Balance pass**  
   Tune **`SURVIVE_SECONDS`**, **`STEP_INTERVAL_MS`**, vision ranges, and **`PREDATOR_BFS_MAX_EXPANSIONS`** so both **manual** and **auto** modes feel fair for a live demo.

5. **Optional UX**  
   Pause (**P**), mute, or fullscreen; optional **debug overlay** (e.g. highlight tiles within predator vision) for the presentation.

6. **Richer environment (if time)**  
   Extra shadow row, exit tile, or cooldown on switches to increase **strategic** depth without new agent types.

7. **Tests**  
   A few **unit tests** for `Grid.toggle_shadows`, `is_walkable`, and one BFS case (fixed maze) to show engineering rigor.

8. **Code cleanup**  
   Deduplicate **`make_world`** in `trials.py` vs **`create_world`** in `simulation.py` via a shared **`world.py`** (optional) if you want a single source of truth for spawns—only if it does not complicate the report narrative.

---

## Relation to Progress Report 1

Progress Report 1 listed **BFS within perception** and **balancing** as next steps. The current build implements **capped local BFS** for visible predators, adds **auto/manual modes**, **restart UX**, **headless trials**, and clearer **module boundaries**. Remaining work is mostly **polish, plots, and narrative** for the final submission rather than core mechanics.
