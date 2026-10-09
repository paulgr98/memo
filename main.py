import os
import random

import pygame

from colors import Color
from memo_button import MemoButton
from util import GameState, Vector2i


class Memo:
    GRID_ROWS = 6
    GRID_COLS = 6

    BUTTON_SIZE = Vector2i(80, 80)

    SCREEN_WIDTH = 820
    SCREEN_HEIGHT = 680
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    OFFSET_X = 140
    OFFSET_Y = 80
    TILE_GAP = 10

    TICKRATE = 60
    FLIP_DELAY_MS = 500

    def __init__(self) -> None:
        pygame.init()

        self.running = True

        self.score = 0
        self.tries = 0

        self.max_score = (self.GRID_ROWS * self.GRID_COLS) // 2

        self.flipped_tiles: list[MemoButton] = []

        self.start_time = pygame.time.get_ticks()
        self.end_time = 0
        self.flip_back_at = 0

        self.game_state = GameState.PLAYER_TURN

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Memo")

        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()

        textures = self._load_textures("assets")
        self.buttons = self._build_board(textures)

    @property
    def elapsed_seconds(self) -> float:
        end_time = (
            self.end_time
            if self.game_state == GameState.GAME_OVER
            else pygame.time.get_ticks()
        )

        return (end_time - self.start_time) / 1000.0

    def start(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.TICKRATE)

    def handle_events(self) -> None:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                continue

            if self.game_state != GameState.PLAYER_TURN:
                continue

            if e.type != pygame.MOUSEBUTTONDOWN:
                continue

            self._handle_tile_clicked(e)

    def _handle_tile_clicked(self, event: pygame.event.Event) -> None:
        for button in self.buttons:
            if not button.was_clicked(event):
                continue

            if button.matched:
                return

            if button.is_active:
                return

            button.flip()
            self.flipped_tiles.append(button)

            self._check_pair()
            return

    def _check_pair(self) -> None:
        if len(self.flipped_tiles) != 2:
            return

        self.tries += 1

        first, second = self.flipped_tiles

        if first.has_same_texture(second):
            self._handle_match(first, second)
        else:
            self._schedule_flip_back()

    def _handle_match(self, first: MemoButton, second: MemoButton) -> None:
        first.matched = True
        second.matched = True

        self.score += 1

        if self.score >= self.max_score:
            self._finish_game()
            return

        self._schedule_flip_back()

    def _schedule_flip_back(self) -> None:
        self.game_state = GameState.CHECKING_PAIRS
        self.flip_back_at = (
            pygame.time.get_ticks() + self.FLIP_DELAY_MS
        )

    def _finish_game(self) -> None:
        self.end_time = pygame.time.get_ticks()
        self.game_state = GameState.GAME_OVER
        self.flipped_tiles.clear()

    def update(self) -> None:
        self._update_flip_timer()

    def _update_flip_timer(self) -> None:
        if self.flip_back_at == 0:
            return

        if pygame.time.get_ticks() < self.flip_back_at:
            return

        self._hide_unmatched_tiles()

        if self.game_state != GameState.GAME_OVER:
            self.game_state = GameState.PLAYER_TURN

    def _hide_unmatched_tiles(self) -> None:
        for tile in self.flipped_tiles:
            if tile.matched:
                continue

            tile.is_active = False

        self.flipped_tiles.clear()
        self.flip_back_at = 0

    def draw(self) -> None:
        self.screen.fill(Color.BACKGROUND.value)

        self._draw_score()

        for button in self.buttons:
            button.draw(self.screen)

    def _draw_score(self) -> None:
        if self.game_state == GameState.GAME_OVER:
            score_message = (
                f"KONIEC. "
                f"Czas gry: {self.elapsed_seconds:.2f}s "
                f"/ Prób: {self.tries}"
            )
            time_message = ""
        else:
            score_message = (
                f"Wynik: {self.score} / {self.max_score}"
            )
            time_message = (
                f"Czas: {self.elapsed_seconds:.2f}s"
            )

        score_surface = self.font.render(
            score_message,
            True,
            Color.WHITE.value
        )

        self.screen.blit(score_surface, (40, 20))

        if time_message:
            time_surface = self.font.render(
                time_message,
                True,
                Color.WHITE.value
            )

            self.screen.blit(
                time_surface,
                (self.SCREEN_WIDTH - 180, 20)
            )

    def _load_textures(self, folder_path: str) -> list[str]:
        return [
            os.path.join(folder_path, file_name)
            for file_name in os.listdir(folder_path)
            if file_name.endswith((".png", ".jpg"))
        ]

    def _build_board(self, textures: list[str]) -> list[MemoButton]:
        layout = self._generate_tiles_layout(textures)

        buttons: list[MemoButton] = []

        for index, texture in enumerate(layout):
            row = index // self.GRID_COLS
            col = index % self.GRID_COLS

            buttons.append(
                MemoButton(
                    self._tile_position(row, col),
                    self.BUTTON_SIZE,
                    texture
                )
            )

        return buttons

    def _tile_position(
        self,
        row: int,
        col: int
    ) -> Vector2i:
        return Vector2i(
            self.OFFSET_X
            + col * (self.BUTTON_SIZE.x + self.TILE_GAP),
            self.OFFSET_Y
            + row * (self.BUTTON_SIZE.y + self.TILE_GAP),
        )

    def _generate_tiles_layout(self, textures: list[str]) -> list[str]:
        while True:
            tiles = textures * 2
            random.shuffle(tiles)

            if self._count_adjacent_pairs(tiles) <= 1:
                return tiles

    def _count_adjacent_pairs(self, tiles: list[str]) -> int:
        adjacent_pairs = 0

        for index, texture in enumerate(tiles):
            row, col = divmod(index, self.GRID_COLS)

            if (
                col < self.GRID_COLS - 1
                and tiles[index + 1] == texture
            ):
                adjacent_pairs += 1

            if (
                row < self.GRID_ROWS - 1
                and tiles[index + self.GRID_COLS] == texture
            ):
                adjacent_pairs += 1

        return adjacent_pairs


if __name__ == "__main__":
    Memo().start()
