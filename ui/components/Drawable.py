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

        self._aspect_ratio: int = 0

        self._draw_x = self._x
        self._draw_y = self._y

        self._width: float = width
        self._height: float = height

        # Animations
        self._size_animation_speed: float = 1
        self._target_width: float = width
        self._target_height: float = height
        self._target_width_dir: int = 1
        self._target_height_dir: int = 1
        self._animate_size = False

        self._parent: Drawable = None
        self._components: List[Drawable] = []
        self._position_type: PositionType = PositionType.RELATIVE

        self.recalculate_position()

    def _child_width_updated(self, child) -> None:
        pass

    def set_size_animation_speed(self, speed: float) -> None:
        self._size_animation_speed = speed

    def set_aspect_ratio(self, ratio: int) -> None:
        self._aspect_ratio = ratio
        self.set_width(self._width)
        self.set_height(self._height)

    def get_position_type(self) -> PositionType:
        return self._position_type

    def set_position_type(self, position_type: PositionType):
        self._position_type = position_type
        self.recalculate_position()

    def set_parent(self, parent):
        self._parent = parent
        self.recalculate_position()

    def remove_component(self, component):
        self._components.remove(component)
        self.recalculate_position()

    def add_component(self, component):
        component.set_parent(self)
        self._components.append(component)

    def set_width(self, width: float) -> None:
        if width == 0:
            width = self.get_height() * self._aspect_ratio
        self._width = width

        if self._parent is not None:
            self._parent._child_width_updated(self)

    def set_height(self, height: float) -> None:
        if height == 0 and self._aspect_ratio != 0:
            height = self.get_width() / self._aspect_ratio
        self._height = height

        if self._target_width < self.get_width():
            self._target_width_dir = -1
        else:
            self._target_width_dir = 1

    def set_animated_height(self, height):
        self.set_height(self._get_target_height())
        if height == 0 and self._aspect_ratio != 0:
            height = self.get_width() / self._aspect_ratio
        self._target_height = height
        self._animate_size = True

        if self._target_height < self.get_height():
            self._target_height_dir = -1
        else:
            self._target_height_dir = 1

    def set_animated_width(self, width):
        self.set_width(self._get_target_width())
        if width == 0:
            width = self.get_height() * self._aspect_ratio
        self._target_width = width
        self._animate_size = True

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def _get_target_width(self) -> float:
        return self._target_width

    def _get_target_height(self) -> float:
        return self._target_height

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

    def _recalculate_children_x(self) -> None:
        for component in self._components:
            component.recalculate_x()

    def _recalculate_children_y(self) -> None:
        for component in self._components:
            component.recalculate_y()

    def recalculate_x(self) -> None:
        # Relative is default
        x = self._x
        if self._parent is not None:
            x += self._parent.get_x()

        if self._position_type == PositionType.ABSOLUTE:
            x = self.get_x()
        elif self._position_type == PositionType.HORIZONTAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_x = self._parent.get_x()
                parent_width = self._parent.get_width()
                width = self.get_width()
                x = Drawable.get_center(parent_x, width, parent_width)
        self._draw_x = x

        self._recalculate_children_x()

    def recalculate_y(self) -> None:
        # Relative is default
        y = self._y
        if self._parent is not None:
            y += self._parent.get_y()

        if self._position_type == PositionType.ABSOLUTE:
            y = self.get_y()
        elif self._position_type == PositionType.VERTICAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_y = self._parent.get_y()
                parent_height = self._parent.get_height()
                height = self.get_height()
                y = Drawable.get_center(parent_y, height, parent_height)
        self._draw_y = y

        self._recalculate_children_y()

    def draw(self) -> None:
        for component in self._components:
            component.draw()

    def update(self) -> None:
        if self._animate_size:
            self._do_size_animation()

        for component in self._components:
            component.update()

    def _do_size_animation(self) -> None:
        # Get size variables
        width = self.get_width()
        height = self.get_height()
        target_width = self._get_target_width()
        target_height = self._get_target_height()

        # If we need to animate width
        if width != target_width:
            new_width = width + self._size_animation_speed * self._target_width_dir

            # Check if we've gone past target
            if self._target_width_dir == 1 and new_width > target_width:
                new_width = target_width
            elif self._target_width_dir == -1 and new_width < target_width:
                new_width = target_width

            self.set_width(new_width)

        # If we need to animate height
        if height != target_height:
            new_height = height + self._size_animation_speed * self._target_height_dir
            # Check if we've gone past target
            if self._target_height_dir == 1 and new_height > target_height:
                new_height = target_height
            elif self._target_height_dir == -1 and new_height < target_height:
                new_height = target_height

            self.set_height(new_height)

        # If all animations are finished
        if self.get_height() == target_height and self.get_width() == target_width:
            self._animate_size = False

        self.recalculate_position()

    @staticmethod
    def get_center(pos: float, size: int, parent_size: int):
        left_over_size = parent_size - size
        center_pos = pos + left_over_size / 2
        return round(center_pos)

    @staticmethod
    def get_right_most(pos: float, size: int, parent_size: int):
        left_over_size = parent_size - size
        right_most_pos = pos + left_over_size
        return round(right_most_pos)
