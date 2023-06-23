from pygame import Color, Rect, Surface
import pygame
from components.Drawable import Drawable
from components.Image import Image
from components.Drawable import PositionType


class CardItem(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._color = Color(255, 255, 255)
        self._image_component: Image = None
        self.set_image(Image(window))

    def set_image(self, image: Image) -> None:
        if self._image_component is not None:
            self.remove_component(self._image_component)

        self._image_component = image
        self.add_component(self._image_component)

    def load_image(self, path: str) -> None:
        image = Image(self._window, 0, 100, 0, 40)
        image.load_image_from(path, True)
        image.set_width(150, False)
        image.set_height(0, False)
        image.resize_image()
        image.set_position_type(PositionType.HORIZONTAL_CENTER)
        self.set_image(image)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def draw(self) -> None:
        rect: Rect = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height())
        pygame.draw.rect(self._window, self._color, rect)
        self._image_component.draw()

        return super().draw()

    def update(self) -> None:
        self._image_component.update()
        return super().update()
