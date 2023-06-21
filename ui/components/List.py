from pygame import Color
import pygame
from components.Drawable import Drawable


class List(Drawable):

    def __init__(self, window, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._border_color = Color(255, 255, 255)
        self._border_size = 0
        self._color = Color(255, 255, 255)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def set_border_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._border_color = Color(r, g, b, a)

    def set_border_size(self, size: int):
        self._border_size = size

    def draw(self):
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_height()

        # List
        pygame.draw.rect(self._window, self._color, (x, y, width, height))

        # Border
        border_x = x
        border_y = y
        border_width = width - self._border_size
        border_height = height - self._border_size
        pygame.draw.rect(self._window, self._border_color, (border_x, border_y, border_width, border_height))

    def update(self):
        pass
