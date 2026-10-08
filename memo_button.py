import pygame
from button import Button
from colors import Color

class MemoButton(Button):
    def __init__(self, position, size, texture_path):
        super().__init__(position, size, Color.TRANSPARENT.value, Color.TRANSPARENT.value)
        self.texture_path = texture_path
        self.matched = False

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        
        if self.is_active:
            texture = pygame.image.load(self.texture_path)
            texture = pygame.transform.scale(texture, self.rect.size)
        else:
            texture = button_surface = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
            pygame.draw.rect(button_surface, Color.BLACK.value, button_surface.get_rect())

        return screen.blit(texture, self.rect)

    def get_texture(self):
        return self.texture_path

    def has_same_texture(self, other: MemoButton):
        return self.get_texture() == other.get_texture()

    def flip(self):
        self.is_active = not self.is_active
