from enum import Enum
from typing import List
from pygame import Color, Surface
import pygame


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

        self._padding_top: float = 0
        self._padding_bottom: float = 0
        self._padding_left: float = 0
        self._padding_right: float = 0

        self._color: Color = Color(255, 255, 255)
        self._hover_color: Color = Color(244, 244, 244)
        self._is_hovered: bool = False

        self._border_radius_top_left: int = 15
        self._border_radius_top_right: int = 15
        self._border_radius_bottom_left: int = 15
        self._border_radius_bottom_right: int = 15

        self._visible: bool = True

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

    def collidepoint(self, x: int, y: int) -> bool:
        my_rect = pygame.rect.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height())
        return my_rect.collidepoint(x, y)

    def set_visible(self, visible: bool) -> None:
        self._visible = visible

    def is_visible(self) -> bool:
        return self._visible

    def _check_hover(self, x: int, y: int) -> None:
        if self.collidepoint(x, y):
            self.set_is_hovered(True)
        else:
            self.set_is_hovered(False)

    def on_mouse_move(self, x: int, y: int) -> None:
        self._check_hover(x, y)
        self.on_mouse_move_children(x, y)

    def on_click(self, x: int, y: int) -> None:
        self.on_click_children(x, y)

    def on_click_children(self, x: int, y: int) -> None:
        for component in self._components:
            component.on_click(x, y)

    def on_mouse_move_children(self, x: int, y: int) -> None:
        for component in self._components:
            component.on_mouse_move(x, y)

    def set_is_hovered(self, is_hovered: bool) -> None:
        self._is_hovered = is_hovered

    def is_hovered(self) -> bool:
        return self._is_hovered

    def set_border_radius_top_left(self, radius: int) -> None:
        self._border_radius_top_left = radius

    def set_border_radius_top_right(self, radius: int) -> None:
        self._border_radius_top_right = radius

    def set_border_radius_bottom_left(self, radius: int) -> None:
        self._border_radius_bottom_left = radius

    def set_border_radius_bottom_right(self, radius: int) -> None:
        self._border_radius_bottom_right = radius

    def get_border_radius_top_left(self) -> None:
        return self._border_radius_top_left

    def get_border_radius_top_right(self) -> None:
        return self._border_radius_top_right

    def get_border_radius_bottom_left(self) -> None:
        return self._border_radius_bottom_left

    def get_border_radius_bottom_right(self) -> None:
        return self._border_radius_bottom_right

    def get_current_color(self) -> Color:
        if self.is_hovered():
            return self.get_hover_color()
        else:
            return self.get_color()

    def get_color(self) -> Color:
        return self._color

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def get_hover_color(self) -> Color:
        return self._hover_color

    def set_hover_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._hover_color = Color(r, g, b, a)

    def get_horizontal_padding(self) -> float:
        return self.get_padding_left() + self.get_padding_right()

    def get_vertical_padding(self) -> float:
        return self.get_padding_top() + self.get_padding_bottom()

    def get_padding_top(self) -> float:
        return self._padding_top

    def get_padding_bottom(self) -> float:
        return self._padding_bottom

    def get_padding_left(self) -> float:
        return self._padding_left

    def get_padding_right(self) -> float:
        return self._padding_right

    def set_padding_top(self, padding: float) -> None:
        self._padding_top = padding

    def set_padding_bottom(self, padding: float) -> None:
        self._padding_bottom = padding

    def set_padding_left(self, padding: float) -> None:
        self._padding_left = padding

    def set_padding_right(self, padding: float) -> None:
        self._padding_right = padding

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

    def set_parent(self, parent) -> None:
        self._parent = parent

    def remove_component(self, component) -> None:
        self._components.remove(component)

    def add_component(self, component) -> None:
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

    def set_animated_height(self, height) -> None:
        if height == 0 and self._aspect_ratio != 0:
            height = self.get_width() / self._aspect_ratio
        self._target_height = height
        self._animate_size = True

        if self._target_height < self.get_height():
            self._target_height_dir = -1
        else:
            self._target_height_dir = 1

    def set_animated_width(self, width) -> None:
        if width == 0:
            width = self.get_height() * self._aspect_ratio
        self._target_width = width
        self._animate_size = True

        if self._target_width < self.get_width():
            self._target_width_dir = -1
        else:
            self._target_width_dir = 1

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

    def set_y(self, y: int) -> None:
        self._y = y

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
            x += self._parent.get_x() + self._parent.get_padding_left()

        if self._position_type == PositionType.ABSOLUTE:
            x = self._x
        elif self._position_type == PositionType.HORIZONTAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_x = self._parent.get_x()
                parent_width = self._parent.get_width()
                parent_padding_left = self._parent.get_padding_left()
                parent_padding_right = self._parent.get_padding_right()
                width = self.get_width()
                x = Drawable.get_center(parent_x + parent_padding_left, width, parent_width - parent_padding_left - parent_padding_right)
        self._draw_x = x
        self._recalculate_children_x()

    def recalculate_y(self) -> None:
        # Relative is default
        y = self._y
        if self._parent is not None:
            y += self._parent.get_y() + self._parent.get_padding_top()

        if self._position_type == PositionType.ABSOLUTE:
            y = self.get_y()
        elif self._position_type == PositionType.VERTICAL_CENTER or self._position_type == PositionType.CENTER:
            if self._parent is not None:
                parent_y = self._parent.get_y()
                parent_height = self._parent.get_height()
                parent_padding_top = self._parent.get_padding_top()
                height = self.get_height()
                y = Drawable.get_center(parent_y + parent_padding_top, height, parent_height - parent_padding_top)
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
