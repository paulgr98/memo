from util import Vector2i
from colors import Color
import pygame


class Button:
    def __init__(self, position: Vector2i, size: Vector2i, normal_color: Color, active_color: Color):
        self.rect = pygame.Rect(position.x, position.y, size.x, size.y)
        self.normal_color: Color = normal_color
        self.active_color: Color = active_color
        self.is_active = False

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, value):
        self.rect.width = value

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, value):
        self.rect.height = value

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    # def draw(self, screen: pygame.Surface) -> pygame.Rect:
    #     color = self.active_color if self.is_active else self.normal_color
    #     button_surface = pygame.Surface(pygame.Rect(self.rect).size, pygame.SRCALPHA)
    #     pygame.draw.rect(button_surface, color.value, button_surface.get_rect())
    #     return screen.blit(button_surface, self.rect)

    def draw(self, screen: pygame.Surface) -> pygame.Rect:
        color = self.active_color if self.is_active else self.normal_color
        return pygame.draw.rect(screen, color.value, self.rect)

    def is_hovered(self, event: pygame.Event) -> bool:
        return self.rect.collidepoint(event.pos)

    def was_clicked(self, event: pygame.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.is_hovered(event)
        )
