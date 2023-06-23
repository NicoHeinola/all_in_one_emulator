from pygame import Color
import pygame
from ui.components.Drawable import Drawable


class ListComponent(Drawable):

    def __init__(self, window, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._color = Color(255, 255, 255)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def draw(self):
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_height()

        # List
        pygame.draw.rect(self._window, self._color, (x, y, width, height))

    def update(self):
        pass
