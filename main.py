
import pygame
import os
import random

from util import GameState, Vector2i
from memo_button import MemoButton
from colors import Color


class Memo:
    def __init__(self):
        pygame.init()

        self.running = True

        self.TICKRATE = 60
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 820, 680
        self.BUTTON_SIZE = Vector2i(80, 80)

        self.BUTTON_ROWS = 6
        self.BUTTON_COLS = 6

        self.score: int = 0
        self.max_score: int = (self.BUTTON_COLS * self.BUTTON_ROWS) // 2
        self.flipped_tiles: list[MemoButton] = []

        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Memo")
        self.font = pygame.font.SysFont(None, 36)

        self.clock = pygame.time.Clock()

        self.next_reset_time = 0
        self.start_time = pygame.time.get_ticks()
        self.end_time = 0

        self.textures: list[str] = self._get_textures("assets")
        self.buttons: list[MemoButton] = self._create_buttons(self.textures)

        self.game_state = GameState.PLAYER_TURN

    def _get_textures(self, folder_path: str) -> list[str]:
        files = []
        for item in os.listdir(folder_path):
            if item.endswith(".png") or item.endswith(".jpg"):
                files.append(f'{folder_path}/{item}')
        return files

    def _create_buttons(self, textures: list[str]):
        OFFSET_X = 140
        OFFSET_Y = 80
        GAP = 10

        buttons = []

        textures = textures * 2
        random.shuffle(textures)

        for col in range(self.BUTTON_COLS):
            for row in range(self.BUTTON_ROWS):
                random_texture = textures.pop()
                mb = MemoButton(
                    Vector2i(
                        OFFSET_X + ((GAP + self.BUTTON_SIZE.x) * col),
                        OFFSET_Y + ((GAP + self.BUTTON_SIZE.y) * row)
                    ),
                    self.BUTTON_SIZE,
                    random_texture
                )
                buttons.append(mb)
        return buttons

    def start(self):
        self.new_game()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.TICKRATE)

    def new_game(self):
        self.start_next_round()

    def start_next_round(self):
        self.game_state = GameState.PLAYER_TURN

    def game_over(self):
        self.game_state = GameState.GAME_OVER

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

            if self.game_state != GameState.PLAYER_TURN:
                continue

            if e.type != pygame.MOUSEBUTTONDOWN:
                continue

            for button in self.buttons:
                if button.was_clicked(e):
                    if button.matched:
                        continue
                    if button in self.flipped_tiles:
                        self.flipped_tiles.remove(button)
                    else:
                        self.flipped_tiles.append(button)

                    button.flip()
                    break
            self.handle_checking_stage()

    def handle_checking_stage(self):
        if len(self.flipped_tiles) != 2:
            return

        first, second = self.flipped_tiles
        if first is second:
            self.flipped_tiles.clear()
            return

        if first.has_same_texture(second):
            self.score += 1
            first.matched = second.matched = True
            if self.score == self.max_score:
                self.game_over()
                self.flipped_tiles.clear()
                self.end_time = pygame.time.get_ticks()
                return

        self.next_reset_time = pygame.time.get_ticks() + 500

    def update(self):
        if len(self.flipped_tiles) >= 2:
            self.game_state = GameState.CHECKING_PAIRS

        current_time = pygame.time.get_ticks()
        if self.next_reset_time != 0 and current_time >= self.next_reset_time:
            self.reset_tiles()
            self.game_state = GameState.PLAYER_TURN

    def reset_tiles(self):
        for tile in self.flipped_tiles:
            if not tile.matched:
                tile.is_active = False

        self.flipped_tiles.clear()
        self.next_reset_time = 0

    def draw(self):
        self.screen.fill(Color.BACKGROUND.value)
        self.draw_score()
        for button in self.buttons:
            button.draw(self.screen)

    def draw_score(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000

        score_message = f"Wynik: {self.score} / {self.max_score}"
        time_message = f"Czas: {elapsed}"

        if self.game_state == GameState.GAME_OVER:
            play_time = self.end_time - self.start_time // 1000
            score_message = f"KONIEC. Czas gry: {play_time}s"

        score_render_text = self.font.render(score_message,
                                             True,
                                             Color.WHITE.value)
        time_render_text = self.font.render(time_message, True, Color.WHITE.value
                                            )
        self.screen.blit(score_render_text, (40, 20))
        self.screen.blit(time_render_text, (self.SCREEN_WIDTH - 150, 20))


if __name__ == "__main__":
    memo = Memo()
    memo.start()
