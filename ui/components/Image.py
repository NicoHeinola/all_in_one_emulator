from pygame import Surface
import pygame
from components.Drawable import Drawable


class Image(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._original_image: Surface = None
        self._image: Surface = Surface((0, 0))
        self._aspect_ratio: int = 0

    def set_aspect_ratio(self, ratio: int, resize: bool = True) -> None:
        super().set_aspect_ratio(ratio)
        if resize:
            self.resize_image()

    def set_width(self, width: float, resize: bool = True) -> None:
        super().set_width(width)
        if resize:
            self.resize_image()

    def set_height(self, height: float, resize: bool = True) -> None:
        super().set_height(height)
        if resize:
            self.resize_image()

    def load_image_from(self, path: str, use_image_size=True) -> None:
        self._original_image = pygame.image.load(path).convert_alpha()

        # Uses images original size instead of this classes current definition
        if use_image_size:
            width = self._original_image.get_width()
            height = self._original_image.get_height()
            self.set_width(width, False)
            self.set_height(height, False)
            self.set_aspect_ratio(width / height, False)

        self.resize_image()

    def resize_image(self) -> None:
        image = self._original_image.copy()
        width = self.get_width()
        height = self.get_height()
        image = pygame.transform.scale(image, (width, height))
        self._image = image

    def _get_image(self) -> Surface:
        return self._image

    def draw(self) -> None:
        self._window.blit(self._get_image(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()))

        return super().draw()
