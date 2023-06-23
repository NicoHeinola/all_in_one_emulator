from typing import List

from pygame import Surface
from ui.components.Drawable import Drawable


class Scene:
    def __init__(self, window: Surface) -> None:
        self._window: Surface = window
        self._elements: List[Drawable] = []

    def create_elements(self) -> None:
        self._empty_elements()

    def _add_element(self, element: Drawable) -> None:
        self._elements.append(element)

    def _empty_elements(self) -> None:
        self._elements = []

    def joystick_key_down(self, key_code) -> None:
        pass

    def keyboard_key_down(self, key_code) -> None:
        pass

    def draw(self) -> None:
        for element in self._elements:
            element.draw()

    def update(self) -> None:
        for element in self._elements:
            element.update()
