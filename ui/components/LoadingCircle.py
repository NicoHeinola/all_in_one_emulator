from pygame import Color, Surface
import pygame
from ui.components.Drawable import Drawable
import math


class LoadingCircle(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)

        self._color: Color = Color(255, 255, 255)
        self._angle: int = 0
        self._end_angle: int = 180
        self._rotation_speed: int = 4

    def set_rotation_speed(self, speed: int) -> None:
        self._rotation_speed = speed

    def set_angle(self, angle: int) -> None:
        self._angle = angle

    def set_end_angle(self, angle: int) -> None:
        self._end_angle = angle

    def set_width(self, width: float) -> None:
        super().set_width(width)
        self._height = width

    def set_height(self, height: float) -> None:
        super().set_height(height)
        self._width = height

    def get_radius(self) -> float:
        return self.get_width() / 2

    def draw(self) -> None:
        if not self.is_visible():
            return

        # Draw the loading circle
        start_angle = math.radians(self._angle)
        end_angle = math.radians(self._angle + self._end_angle)  # Adjust this value to change the arc length
        pygame.draw.arc(self._window, self.get_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()), start_angle, end_angle, 4)

        self._angle += self._rotation_speed
