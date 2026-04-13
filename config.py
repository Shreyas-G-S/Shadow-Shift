"""
Shadow Shift – central configuration.
Tune window, grid, colors, predator perception, and win condition here.
"""

# --- Grid movement (shared by agents) ---
DIRS_4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

# --- Display ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# --- Grid (environment) ---
GRID_COLS = 20
GRID_ROWS = 15
TILE_SIZE = 32

# Derived: center grid in window
GRID_WIDTH = GRID_COLS * TILE_SIZE
GRID_HEIGHT = GRID_ROWS * TILE_SIZE
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_OFFSET_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

# --- Predator perception (limited sensors per PEAS) ---
PREDATOR_VISION_RANGE = 6       # graph steps along walkable tiles (walls block LOS)
PREDATOR_SHADOW_VISION_RANGE = 3  # in shadow, shorter LOS along same graph
PREDATOR_LOS_MAX_NODES = 220      # cap flood-fill work for line-of-sight
# Local BFS pathfinding when chasing (cap work → still "local" planning)
PREDATOR_BFS_MAX_EXPANSIONS = 160
# When blind: probability of pure random step (rest is stalk/intercept)
PREDATOR_STALK_JITTER = 0.12
# Forget last seen if player has moved this far from that cell (Manhattan)
PREDATOR_MEMORY_DECAY_TILES = 14

# --- Game goal (Performance: survival time) ---
SURVIVE_SECONDS = 60  # Win if player survives this long
STEP_INTERVAL_MS = 180  # one simulation step every N ms
AUTO_PLAYER = True  # True: autonomous player, False: keyboard-controlled player

# --- Colors ---
COLOR_BG = (10, 10, 20)
COLOR_WALL = (40, 40, 80)
COLOR_FLOOR = (20, 20, 40)
COLOR_SHADOW_FLOOR = (8, 8, 16)
COLOR_PLAYER = (80, 200, 255)
COLOR_PREDATOR = (255, 80, 120)
COLOR_NEUTRAL = (120, 255, 160)
COLOR_GRID_LINES = (30, 30, 60)
COLOR_SWITCH = (255, 190, 60)  # switch not yet hit this run (stand out)
COLOR_SWITCH_VISITED = (140, 120, 50)  # switch already pressed at least once
COLOR_EXIT = (60, 220, 120)  # goal tile (distinct from floor / neutrals)
COLOR_TEXT = (220, 220, 240)
