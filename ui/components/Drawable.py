from enum import Enum
from typing import List

from pygame import Surface


class PositionType(Enum):
    RELATIVE = 1
    ABSOLUTE = 2
    VERTICAL_CENTER = 3
    HORIZONTAL_CENTER = 4
    CENTER = 5


class Drawable:
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        self._window: Surface = window
        self._x: int = x
        self._y: int = y
        self._draw_x: int = x
        self._draw_y: int = y

        self._draw_x = self._x
        self._draw_y = self._y

        self._width: float = width
        self._height: float = height

        self._parent: Drawable = None
        self._components: List[Drawable] = []
        self._position_type: PositionType = PositionType.RELATIVE

        self.recalculate_position()

    def set_position_type(self, position_type: PositionType):
        self._position_type = position_type
        self.recalculate_position()

    def set_parent(self, parent):
        self._parent = parent
        self.recalculate_position()

    def add_component(self, component):
        component.set_parent(self)
        self._components.append(component)

    def set_width(self, width: float) -> None:
        self._width = width

    def set_height(self, height: float) -> None:
        self._height = height

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def set_x(self, x: int) -> None:
        self._x = x
        self.recalculate_x()

    def set_y(self, y: int) -> None:
        self._y = y
        self.recalculate_y()

    def get_x(self) -> int:
        return self._draw_x

    def get_y(self) -> int:
        return self._draw_y

    def recalculate_position(self) -> None:
        self.recalculate_x()
        self.recalculate_y()

    def recalculate_x(self) -> None:
        x = self.get_x()
        if self._position_type == PositionType.RELATIVE:
            if self._parent is not None:
                x += self._parent.get_x()
        elif self._position_type == PositionType.HORIZONTAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_x = self._parent.get_x()
                parent_width = self._parent.get_width()
                width = self.get_width()
                x = Drawable.get_center(parent_x, width, parent_width)
        self._draw_x = x

    def recalculate_y(self) -> None:
        y = self.get_y()
        if self._position_type == PositionType.RELATIVE:
            if self._parent is not None:
                y += self._parent.get_y()
        elif self._position_type == PositionType.VERTICAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_y = self._parent.get_y()
                parent_height = self._parent.get_height()
                height = self.get_height()
                y = Drawable.get_center(parent_y, height, parent_height)
        self._draw_y = y

    def draw(self) -> None:
        for component in self._components:
            component.draw()

    def update(self) -> None:
        for component in self._components:
            component.update()

    @staticmethod
    def get_center(pos: float, size: int, parent_size: int):
        left_over_size = parent_size - size
        center_pos = pos + left_over_size / 2
        return round(center_pos)
