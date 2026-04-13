"""
Shadow Shift – simulation loop: input, update order, win/lose, rendering.
Ties together grid (environment) and agents; implements Performance (survival time).
"""
import sys
from typing import List

import pygame

import config
from game_rules import evaluate_round
from world import create_world
from grid import Grid
from agents import Player, Agent, update_agents, auto_move_player


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
            if grid.is_exit(col, row):
                inset = 5
                pygame.draw.rect(
                    surface,
                    config.COLOR_EXIT,
                    (
                        x + inset,
                        y + inset,
                        config.TILE_SIZE - 2 * inset,
                        config.TILE_SIZE - 2 * inset,
                    ),
                    width=3,
                    border_radius=6,
                )
            if grid.is_switch(col, row):
                pad = config.TILE_SIZE // 4
                sw_color = (
                    config.COLOR_SWITCH_VISITED
                    if (col, row) in grid.switches_pressed
                    else config.COLOR_SWITCH
                )
                pygame.draw.rect(
                    surface,
                    sw_color,
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


def handle_keydown(event: pygame.event.Event, player: Player, grid: Grid) -> None:
    """Manual mode: one key press moves one tile; switches toggle shadows."""
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
            grid.press_switch(player.col, player.row)


def run() -> None:
    """Main loop: init, create world, run until win/lose/quit; R restarts, Q quits."""
    pygame.init()
    pygame.display.set_caption("Shadow Shift")
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    grid, player, agents = create_world()
    survival_start_ms = pygame.time.get_ticks()
    running = True
    won = False
    lost = False
    win_kind = ""  # "exit" | "time" when won
    step_accumulator_ms = 0
    final_survival_sec = 0.0

    def apply_round_result(w: bool, l: bool, reason: str, t: float) -> None:
        nonlocal won, lost, win_kind, final_survival_sec
        if l:
            lost = True
            final_survival_sec = t
        elif w:
            won = True
            win_kind = reason
            final_survival_sec = t

    while running:
        dt_ms = clock.tick(config.FPS)
        elapsed_sec = (pygame.time.get_ticks() - survival_start_ms) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if won or lost:
                    if event.key in (pygame.K_r, pygame.K_RETURN):
                        grid, player, agents = create_world()
                        survival_start_ms = pygame.time.get_ticks()
                        won = False
                        lost = False
                        win_kind = ""
                        step_accumulator_ms = 0
                        final_survival_sec = 0.0
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                elif not config.AUTO_PLAYER:
                    handle_keydown(event, player, grid)
                    if not won and not lost:
                        sim_elapsed = (pygame.time.get_ticks() - survival_start_ms) / 1000.0
                        apply_round_result(
                            *evaluate_round(grid, player, agents, sim_elapsed),
                            sim_elapsed,
                        )

        if not won and not lost:
            step_accumulator_ms += dt_ms
            while step_accumulator_ms >= config.STEP_INTERVAL_MS and not won and not lost:
                step_accumulator_ms -= config.STEP_INTERVAL_MS
                if config.AUTO_PLAYER:
                    auto_move_player(player, grid, agents)
                update_agents(agents, player, grid)
                sim_elapsed = (pygame.time.get_ticks() - survival_start_ms) / 1000.0
                apply_round_result(
                    *evaluate_round(grid, player, agents, sim_elapsed),
                    sim_elapsed,
                )

        screen.fill(config.COLOR_BG)
        draw_grid(screen, grid)
        draw_player(screen, player)
        draw_agents(screen, agents)

        # HUD: survival time (Performance metric)
        if not won and not lost:
            remain = max(0, config.SURVIVE_SECONDS - int(elapsed_sec))
            time_text = font.render(f"Survive: {remain}s", True, config.COLOR_TEXT)
        else:
            time_text = font.render(f"Time: {final_survival_sec:.1f}s", True, config.COLOR_TEXT)
        hud_x = config.GRID_OFFSET_X
        sw_done = grid.switches_hit_count()
        sw_total = len(grid.switches)
        sw_line = font_small.render(
            f"Switches: {sw_done}/{sw_total}  (visit each bright yellow tile once)",
            True,
            config.COLOR_TEXT,
        )
        goal_line = font_small.render(
            f"Exit (green) counts only after all switches  |  Or survive {config.SURVIVE_SECONDS}s",
            True,
            config.COLOR_TEXT,
        )
        screen.blit(sw_line, (hud_x, 8))
        screen.blit(goal_line, (hud_x, 32))
        screen.blit(time_text, (hud_x, config.GRID_OFFSET_Y - 26))

        hint = font_small.render(
            "R restart  Q quit" + ("" if config.AUTO_PLAYER else "  arrows/WASD move"),
            True,
            config.COLOR_TEXT,
        )
        screen.blit(hint, (config.GRID_OFFSET_X, config.WINDOW_HEIGHT - 28))

        if won:
            if win_kind == "exit":
                msg = font.render("Escaped! (Switches + exit)", True, (100, 255, 100))
                ox = -200
            else:
                msg = font.render("You survived! (Time)", True, (100, 255, 100))
                ox = -150
            screen.blit(msg, (config.WINDOW_WIDTH // 2 + ox, config.WINDOW_HEIGHT // 2 - 40))
            h2 = font_small.render("Press R to play again", True, config.COLOR_TEXT)
            screen.blit(h2, (config.WINDOW_WIDTH // 2 - 110, config.WINDOW_HEIGHT // 2 + 8))
        if lost:
            msg = font.render("Caught! (Lose)", True, (255, 100, 100))
            screen.blit(msg, (config.WINDOW_WIDTH // 2 - 100, config.WINDOW_HEIGHT // 2 - 40))
            h2 = font_small.render("Press R to try again", True, config.COLOR_TEXT)
            screen.blit(h2, (config.WINDOW_WIDTH // 2 - 100, config.WINDOW_HEIGHT // 2 + 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)
