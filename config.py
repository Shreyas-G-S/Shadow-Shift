"""
Shadow Shift – central configuration.
Tune window, grid, colors, predator perception, and win condition here.
"""

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
PREDATOR_VISION_RANGE = 6       # tiles; beyond this, predator cannot see player
PREDATOR_SHADOW_VISION_RANGE = 3  # tiles; in shadow, predator sees only this close

# --- Game goal (Performance: survival time) ---
SURVIVE_SECONDS = 60  # Win if player survives this long

# --- Colors ---
COLOR_BG = (10, 10, 20)
COLOR_WALL = (40, 40, 80)
COLOR_FLOOR = (20, 20, 40)
COLOR_SHADOW_FLOOR = (8, 8, 16)
COLOR_PLAYER = (80, 200, 255)
COLOR_PREDATOR = (255, 80, 120)
COLOR_NEUTRAL = (120, 255, 160)
COLOR_GRID_LINES = (30, 30, 60)
COLOR_SWITCH = (230, 210, 80)
COLOR_TEXT = (220, 220, 240)
