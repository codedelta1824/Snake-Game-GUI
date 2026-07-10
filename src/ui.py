import pygame

from src.config import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    BOARD_X,
    BOARD_Y,
    BORDER,
    CELL_SIZE,
    Colors,
    FOOD,
    MUTED,
    PANEL_ALT,
    SNAKE_BODY,
    SNAKE_HEAD,
    TEXT,
    WIDTH,
)
from src.states import GameState


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, label: str) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label

    def collidepoint(self, point) -> bool:
        return self.rect.collidepoint(point)

    def draw(self, surface: pygame.Surface, mouse_pos) -> None:
        hovered = self.rect.collidepoint(mouse_pos)
        color = ACCENT if hovered else PANEL_ALT
        pygame.draw.rect(surface, color, self.rect, border_radius=14)
        pygame.draw.rect(surface, BORDER, self.rect, width=2, border_radius=14)
        draw_text(surface, self.label, 20, TEXT, self.rect.centerx, self.rect.centery, bold=True)


def draw_text(surface: pygame.Surface, text: str, size: int, color, x: int, y: int, bold: bool = False) -> None:
    font = pygame.font.SysFont("arial", size, bold=bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x, y))
    surface.blit(rendered, rect)


def draw_gradient_background(surface: pygame.Surface) -> None:
    for step in range(0, surface.get_height(), 4):
        ratio = step / max(1, surface.get_height())
        color = (
            int(Colors.BACKGROUND_TOP[0] + (Colors.BACKGROUND_BOTTOM[0] - Colors.BACKGROUND_TOP[0]) * ratio),
            int(Colors.BACKGROUND_TOP[1] + (Colors.BACKGROUND_BOTTOM[1] - Colors.BACKGROUND_TOP[1]) * ratio),
            int(Colors.BACKGROUND_TOP[2] + (Colors.BACKGROUND_BOTTOM[2] - Colors.BACKGROUND_TOP[2]) * ratio),
        )
        pygame.draw.line(surface, color, (0, step), (surface.get_width(), step))


def draw_hud(surface: pygame.Surface, score: int, high_score: int, pause_button: Button, state) -> None:
    score_panel = pygame.Rect(40, 30, 220, 70)
    pygame.draw.rect(surface, (15, 23, 42), score_panel, border_radius=16)
    pygame.draw.rect(surface, BORDER, score_panel, width=2, border_radius=16)
    draw_text(surface, f"Score: {score}", 20, TEXT, score_panel.centerx, score_panel.centery - 10, bold=True)
    draw_text(surface, f"Best: {high_score}", 16, MUTED, score_panel.centerx, score_panel.centery + 16)

    pause_button.draw(surface, pygame.mouse.get_pos())

    if state == GameState.PAUSED:
        draw_text(surface, "Paused", 18, (251, 191, 36), pause_button.rect.centerx, pause_button.rect.centery + 2, bold=True)


def draw_snake(surface: pygame.Surface, snake) -> None:
    for index, (x, y) in enumerate(snake):
        pixel_x = BOARD_X + x * CELL_SIZE
        pixel_y = BOARD_Y + y * CELL_SIZE
        rect = pygame.Rect(pixel_x + 2, pixel_y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        color = SNAKE_HEAD if index == 0 else SNAKE_BODY
        pygame.draw.rect(surface, color, rect, border_radius=6)


def draw_food(surface: pygame.Surface, food_pos) -> None:
    x, y = food_pos
    pixel_x = BOARD_X + x * CELL_SIZE
    pixel_y = BOARD_Y + y * CELL_SIZE
    center = (pixel_x + CELL_SIZE // 2, pixel_y + CELL_SIZE // 2)
    pygame.draw.circle(surface, FOOD, center, CELL_SIZE // 2 - 2)
    pygame.draw.circle(surface, (255, 255, 255), center, 4)


def draw_menu_overlay(surface: pygame.Surface, start_button: Button) -> None:
    overlay = pygame.Surface((WIDTH, 400), pygame.SRCALPHA)
    overlay.fill((15, 23, 42, 180))
    surface.blit(overlay, (0, 90))
    draw_text(surface, "Classic Snake, Reimagined", 34, TEXT, WIDTH // 2, 180, bold=True)
    draw_text(surface, "Eat food, grow longer, and avoid collisions.", 20, MUTED, WIDTH // 2, 232)
    draw_text(surface, "Controls: WASD or Arrow Keys", 18, MUTED, WIDTH // 2, 270)
    start_button.draw(surface, pygame.mouse.get_pos())


def draw_pause_overlay(surface: pygame.Surface, resume_button: Button) -> None:
    overlay = pygame.Surface((WIDTH, 400), pygame.SRCALPHA)
    overlay.fill((15, 23, 42, 180))
    surface.blit(overlay, (0, 90))
    draw_text(surface, "Paused", 34, (251, 191, 36), WIDTH // 2, 180, bold=True)
    draw_text(surface, "Press P or Escape to resume", 20, MUTED, WIDTH // 2, 232)
    resume_button.draw(surface, pygame.mouse.get_pos())


def draw_game_over_overlay(surface: pygame.Surface, restart_button: Button, score: int) -> None:
    overlay = pygame.Surface((WIDTH, 400), pygame.SRCALPHA)
    overlay.fill((15, 23, 42, 180))
    surface.blit(overlay, (0, 90))
    draw_text(surface, "Game Over", 34, (248, 113, 113), WIDTH // 2, 180, bold=True)
    draw_text(surface, f"Final Score: {score}", 24, TEXT, WIDTH // 2, 232)
    draw_text(surface, "Press Enter or click below to play again", 18, MUTED, WIDTH // 2, 270)
    restart_button.draw(surface, pygame.mouse.get_pos())
