import argparse
import os
import sys

import pygame

from src.config import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    BOARD_X,
    BOARD_Y,
    CELL_SIZE,
    FPS,
    GRID_SIZE,
    HEIGHT,
    WIDTH,
)
from src.states import GameState
from src.ui import (
    Button,
    draw_food,
    draw_gradient_background,
    draw_hud,
    draw_menu_overlay,
    draw_pause_overlay,
    draw_snake,
    draw_text,
    draw_game_over_overlay,
)


class SnakeGame:
    def __init__(self, headless: bool = False) -> None:
        pygame.init()
        pygame.display.set_caption("Professional Snake GUI")
        self.headless = headless
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU

        self.score = 0
        self.high_score = self.load_high_score()
        self.reset()

        self.start_button = Button(WIDTH // 2 - 125, 430, 250, 55, "Start Game")
        self.restart_button = Button(WIDTH // 2 - 125, 430, 250, 55, "Play Again")
        self.resume_button = Button(WIDTH // 2 - 125, 430, 250, 55, "Resume")
        self.pause_button = Button(WIDTH - 165, 28, 120, 46, "Pause")

    def load_high_score(self) -> int:
        score_file = os.path.join(os.path.dirname(__file__), "highscore.txt")
        if os.path.exists(score_file):
            with open(score_file, "r", encoding="utf-8") as handle:
                try:
                    return int(handle.read().strip() or 0)
                except ValueError:
                    return 0
        return 0

    def save_high_score(self) -> None:
        score_file = os.path.join(os.path.dirname(__file__), "highscore.txt")
        with open(score_file, "w", encoding="utf-8") as handle:
            handle.write(str(self.high_score))

    def reset(self) -> None:
        self.snake = [
            (GRID_SIZE // 2, GRID_SIZE // 2),
            (GRID_SIZE // 2 - 1, GRID_SIZE // 2),
            (GRID_SIZE // 2 - 2, GRID_SIZE // 2),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.speed = 8

    def spawn_food(self):
        while True:
            position = (
                pygame.math.Vector2(
                    pygame.randint(0, GRID_SIZE - 1),
                    pygame.randint(0, GRID_SIZE - 1),
                )
            )
            if tuple(position) not in self.snake:
                return (int(position.x), int(position.y))

    def start_game(self) -> None:
        self.reset()
        self.state = GameState.PLAYING

    def pause_game(self) -> None:
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume_game(self) -> None:
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def end_game(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.state = GameState.GAME_OVER

    def queue_direction(self, new_direction) -> None:
        if new_direction == (-self.direction[0], -self.direction[1]):
            return
        self.next_direction = new_direction

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = event.pos
                if self.state == GameState.MENU and self.start_button.collidepoint(position):
                    self.start_game()
                elif self.state == GameState.PLAYING and self.pause_button.collidepoint(position):
                    self.pause_game()
                elif self.state == GameState.PAUSED and self.resume_button.collidepoint(position):
                    self.resume_game()
                elif self.state == GameState.GAME_OVER and self.restart_button.collidepoint(position):
                    self.start_game()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    if self.state == GameState.PLAYING:
                        self.pause_game()
                    elif self.state == GameState.PAUSED:
                        self.resume_game()
                    continue

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.state in (GameState.MENU, GameState.GAME_OVER):
                        self.start_game()
                    elif self.state == GameState.PAUSED:
                        self.resume_game()
                    continue

                if self.state != GameState.PLAYING:
                    continue

                if event.key in (pygame.K_w, pygame.K_UP):
                    self.queue_direction((0, -1))
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    self.queue_direction((0, 1))
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    self.queue_direction((-1, 0))
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.queue_direction((1, 0))

    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return

        if self.next_direction:
            if self.next_direction != (-self.direction[0], -self.direction[1]):
                self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.snake[0]
        next_x = head_x + self.direction[0]
        next_y = head_y + self.direction[1]
        next_head = (next_x, next_y)

        if not (0 <= next_head[0] < GRID_SIZE and 0 <= next_head[1] < GRID_SIZE):
            self.end_game()
            return

        if next_head in self.snake[1:]:
            self.end_game()
            return

        self.snake.insert(0, next_head)

        if next_head == self.food:
            self.score += 1
            self.speed = min(16, 8 + self.score // 3)
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self) -> None:
        draw_gradient_background(self.screen)
        draw_text(self.screen, "Snake Deluxe", 36, (248, 250, 252), WIDTH // 2, 32, bold=True)
        draw_text(self.screen, "WASD to move • P to pause", 18, (203, 213, 225), WIDTH // 2, 70)

        pygame.draw.rect(self.screen, (15, 23, 42), (BOARD_X - 16, BOARD_Y - 16, BOARD_WIDTH + 32, BOARD_HEIGHT + 32), border_radius=18)
        pygame.draw.rect(self.screen, (51, 65, 85), (BOARD_X - 10, BOARD_Y - 10, BOARD_WIDTH + 20, BOARD_HEIGHT + 20), width=2, border_radius=16)

        draw_hud(self.screen, self.score, self.high_score, self.pause_button, self.state)
        draw_snake(self.screen, self.snake)
        draw_food(self.screen, self.food)

        if self.state == GameState.MENU:
            draw_menu_overlay(self.screen, self.start_button)
        elif self.state == GameState.PAUSED:
            draw_pause_overlay(self.screen, self.resume_button)
        elif self.state == GameState.GAME_OVER:
            draw_game_over_overlay(self.screen, self.restart_button, self.score)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Snake Deluxe game")
    parser.add_argument("--headless", action="store_true", help="Run a short headless smoke test")
    args = parser.parse_args()

    game = SnakeGame(headless=args.headless)

    if args.headless:
        for _ in range(3):
            game.handle_events()
            game.update()
            game.draw()
        pygame.quit()
        return

    game.run()


if __name__ == "__main__":
    main()
