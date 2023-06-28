from pygame import Color, Surface
import pygame
from ui.components.Drawable import Drawable


class Circle(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)

        self._color: Color = Color(255, 255, 255)

    def set_width(self, width: float) -> None:
        super().set_width(width)
        self._height = width

    def set_height(self, height: float) -> None:
        super().set_height(height)
        self._width = height

    def get_radius(self) -> float:
        return self.get_width() / 2

    def draw(self) -> None:
        pygame.draw.circle(self._window, self.get_current_color(), (self.get_x() + self.get_width() / 2, self.get_y() + self.get_height() / 2), self.get_radius())

        super().draw()
