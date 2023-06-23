from pygame import Color, Rect, Surface
import pygame
from components.Drawable import Drawable


class CardItem(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._color = Color(255, 255, 255)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def draw(self) -> None:
        rect: Rect = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height())
        pygame.draw.rect(self._window, self._color, rect)

        return super().draw()
