import pygame

WIDTH, HEIGHT = 900, 650
FPS = 60
GRID_SIZE = 24
CELL_SIZE = 24
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE
BOARD_X = (WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 120


class Colors:
    BACKGROUND_TOP = (15, 23, 42)
    BACKGROUND_BOTTOM = (30, 41, 59)
    PANEL = (15, 23, 42)
    PANEL_ALT = (30, 41, 59)
    BORDER = (51, 65, 85)
    TEXT = (248, 250, 252)
    MUTED = (203, 213, 225)
    SNAKE_BODY = (74, 222, 128)
    SNAKE_HEAD = (34, 197, 94)
    FOOD = (248, 113, 113)
    ACCENT = (56, 189, 248)
    WARNING = (251, 191, 36)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def get_board_rect() -> pygame.Rect:
    return pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
