from typing import List
from components.Drawable import Drawable


class Scene:
    def __init__(self, window) -> None:
        self._window = window
        self._elements: List[Drawable] = []

    def _add_element(self, element: Drawable):
        self._elements.append(element)

    def draw(self):
        for element in self._elements:
            element.draw()

    def update(self):
        for element in self._elements:
            element.update()
