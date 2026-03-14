"""
Shadow Shift – simulation loop: input, update order, win/lose, rendering.
Ties together grid (environment) and agents; implements Performance (survival time).
"""
import sys
from typing import List

import pygame

import config
from grid import Grid
from agents import Player, Agent, update_agents, is_player_caught


def draw_grid(surface: pygame.Surface, grid: Grid) -> None:
    """Draw maze tiles, shadow zones, and switch markers."""
    for row in range(grid.rows):
        for col in range(grid.cols):
            x = config.GRID_OFFSET_X + col * config.TILE_SIZE
            y = config.GRID_OFFSET_Y + row * config.TILE_SIZE
            if grid.tiles[row][col] == 1:
                color = config.COLOR_WALL
            else:
                color = (
                    config.COLOR_SHADOW_FLOOR
                    if grid.is_shadow(col, row)
                    else config.COLOR_FLOOR
                )
            pygame.draw.rect(
                surface, color, (x, y, config.TILE_SIZE, config.TILE_SIZE)
            )
            if grid.is_switch(col, row):
                pad = config.TILE_SIZE // 4
                pygame.draw.rect(
                    surface,
                    config.COLOR_SWITCH,
                    (x + pad, y + pad, config.TILE_SIZE - 2 * pad, config.TILE_SIZE - 2 * pad),
                    border_radius=4,
                )
    for col in range(grid.cols + 1):
        x = config.GRID_OFFSET_X + col * config.TILE_SIZE
        pygame.draw.line(
            surface,
            config.COLOR_GRID_LINES,
            (x, config.GRID_OFFSET_Y),
            (x, config.GRID_OFFSET_Y + config.GRID_HEIGHT),
        )
    for row in range(grid.rows + 1):
        y = config.GRID_OFFSET_Y + row * config.TILE_SIZE
        pygame.draw.line(
            surface,
            config.COLOR_GRID_LINES,
            (config.GRID_OFFSET_X, y),
            (config.GRID_OFFSET_X + config.GRID_WIDTH, y),
        )


def draw_player(surface: pygame.Surface, player: Player) -> None:
    """Draw the player sprite."""
    col, row = player.position
    x = config.GRID_OFFSET_X + col * config.TILE_SIZE
    y = config.GRID_OFFSET_Y + row * config.TILE_SIZE
    pad = 4
    pygame.draw.rect(
        surface,
        config.COLOR_PLAYER,
        (x + pad, y + pad, config.TILE_SIZE - 2 * pad, config.TILE_SIZE - 2 * pad),
        border_radius=6,
    )


def draw_agents(surface: pygame.Surface, agents: List[Agent]) -> None:
    """Draw all autonomous agents."""
    pad = 6
    for agent in agents:
        x = config.GRID_OFFSET_X + agent.col * config.TILE_SIZE
        y = config.GRID_OFFSET_Y + agent.row * config.TILE_SIZE
        pygame.draw.rect(
            surface,
            agent.color,
            (x + pad, y + pad, config.TILE_SIZE - 2 * pad, config.TILE_SIZE - 2 * pad),
            border_radius=4,
        )


def handle_keydown(
    event: pygame.event.Event, player: Player, grid: Grid
) -> None:
    """One key press → one tile move; stepping on a switch toggles shadows."""
    dx, dy = 0, 0
    if event.key in (pygame.K_UP, pygame.K_w):
        dy = -1
    elif event.key in (pygame.K_DOWN, pygame.K_s):
        dy = 1
    elif event.key in (pygame.K_LEFT, pygame.K_a):
        dx = -1
    elif event.key in (pygame.K_RIGHT, pygame.K_d):
        dx = 1
    if dx != 0 or dy != 0:
        player.move(dx, dy, grid)
        if grid.is_switch(*player.position):
            grid.toggle_shadows()


def run() -> None:
    """Main loop: init, create world, run until win/lose/quit."""
    pygame.init()
    pygame.display.set_caption("Shadow Shift")
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    grid = Grid.simple_maze(config.GRID_COLS, config.GRID_ROWS)
    player = Player(col=1, row=1)
    agents: List[Agent] = [
        Agent(config.GRID_COLS - 2, 1, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS - 2, config.GRID_ROWS - 2, config.COLOR_PREDATOR, "predator"),
        Agent(config.GRID_COLS // 2, config.GRID_ROWS // 2, config.COLOR_NEUTRAL, "neutral"),
        Agent(2, config.GRID_ROWS - 2, config.COLOR_NEUTRAL, "neutral"),
    ]

    survival_start_ms = pygame.time.get_ticks()
    running = True
    won = False
    lost = False

    while running:
        dt_ms = clock.tick(config.FPS)
        elapsed_sec = (pygame.time.get_ticks() - survival_start_ms) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not won and not lost:
                handle_keydown(event, player, grid)

        if not won and not lost:
            update_agents(agents, player, grid)
            if is_player_caught(agents, player):
                lost = True
            elif elapsed_sec >= config.SURVIVE_SECONDS:
                won = True

        screen.fill(config.COLOR_BG)
        draw_grid(screen, grid)
        draw_player(screen, player)
        draw_agents(screen, agents)

        # HUD: survival time (Performance metric)
        time_text = font.render(f"Survive: {max(0, config.SURVIVE_SECONDS - int(elapsed_sec))}s", True, config.COLOR_TEXT)
        screen.blit(time_text, (config.GRID_OFFSET_X, config.GRID_OFFSET_Y - 28))
        if won:
            msg = font.render("You survived! (Win)", True, (100, 255, 100))
            screen.blit(msg, (config.WINDOW_WIDTH // 2 - 100, config.WINDOW_HEIGHT // 2 - 20))
        if lost:
            msg = font.render("Caught! (Lose)", True, (255, 100, 100))
            screen.blit(msg, (config.WINDOW_WIDTH // 2 - 80, config.WINDOW_HEIGHT // 2 - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)
