import math
from typing import List
from pygame import Color, Surface
import pygame
from ui.components.Drawable import Drawable, PositionType
from ui.components.Text import Text


class VerticalListItem(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._index: int = 0
        self._is_selected: bool = False
        self._selected_color = Color(255, 255, 255)
        self._color = Color(255, 255, 255)
        self._text: Text = Text(window, width, height, 0, 0)
        self._text.set_font_size(18)
        self._text.set_position_type(PositionType.VERTICAL_CENTER)
        self._is_in_view: bool = False
        self._max_list_item_index: int = 0
        self.add_component(self._text)

    def get_y(self) -> int:
        y = super().get_y()
        y += self.get_height() * self._index
        return y

    def get_index(self) -> int:
        return self._index

    def set_parent(self, parent) -> None:
        super().set_parent(parent)

        self.recalculate_is_in_view()

    def get_is_in_view(self) -> bool:
        return self._is_in_view

    def set_is_in_view(self, is_in_view: bool) -> None:
        self._is_in_view = is_in_view

    def recalculate_is_in_view(self) -> None:
        if self._parent is None or self._index < 0:
            self._is_in_view = False
            return

        height = self._parent.get_height()
        padding = self._parent.get_vertical_padding()
        true_height = height - padding
        self._max_list_item_index = math.floor(true_height / self.get_height()) - 1

        if self._index > self._max_list_item_index:
            self._is_in_view = False
        else:
            self._is_in_view = True

    def recalculate_y(self) -> None:
        super().recalculate_y()

        self.recalculate_is_in_view()

    def set_selected(self, selected: bool) -> None:
        self._is_selected = selected

    def set_text(self, text: str) -> None:
        self._text.set_text(text)

    def set_index(self, index: int, do_recalculation: bool = True) -> None:
        self._index = index
        if do_recalculation:
            self.recalculate_is_in_view()
        self.recalculate_y()

    def set_selected_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._selected_color = Color(r, g, b, a)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

    def draw(self) -> None:
        if not self._is_in_view:
            return

        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_height()

        if self._is_selected:
            color = self._selected_color
        else:
            color = self._color

        pygame.draw.rect(self._window, color, (x, y, width, height))

        super().draw()


class ListComponent(Drawable):

    def __init__(self, window, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._color = Color(255, 255, 255)
        self._selected_color = Color(255, 255, 255)
        self._border_radius: int = 0

        # Items
        self._selected_item_index: int = 0
        self._max_list_item_index: int = 0
        self._scroll_view_index: int = 0
        self._list_items: List[VerticalListItem] = []
        self._list_item_functions: list = []
        self._list_item_height: float = 40

        self._recalculate_max_index()

    def add_list_item(self, text: str, function) -> None:
        index = len(self._list_items)
        item = VerticalListItem(self._window, self.get_width() - self.get_padding_left() - self.get_padding_right(), self._list_item_height)
        item.set_position_type(PositionType.RELATIVE)
        item.set_index(index)
        item.set_text(text)
        item.set_padding_left(15)
        item.set_color(self._color.r, self._color.g, self._color.b, self._color.a)
        item.set_selected(False)
        item.set_selected_color(self._selected_color.r, self._selected_color.g, self._selected_color.b, self._selected_color.a)
        self._list_items.append(item)
        self.add_component(item)
        self._list_item_functions.append(function)

    def get_list_item_height(self) -> float:
        return self._list_item_height

    def call_list_item_function(self, list_item_index: int = None) -> None:
        if list_item_index is None:
            list_item_index = self.get_selected_index()
        function = self._list_item_functions[list_item_index]
        function()

    def set_height(self, height: float) -> None:
        super().set_height(height)
        self._recalculate_max_index()

    def set_padding_top(self, padding: float) -> None:
        super().set_padding_top(padding)
        self._recalculate_max_index()

    def set_padding_bottom(self, padding: float) -> None:
        super().set_padding_bottom(padding)
        self._recalculate_max_index()

    def _recalculate_max_index(self) -> None:
        height = self.get_height()
        padding = self.get_vertical_padding()
        true_height = height - padding
        self._max_list_item_index = math.floor(true_height / self._list_item_height) - 1

    def get_selected_index(self) -> int:
        return self._selected_item_index

    def set_selected_index(self, index: int) -> None:
        if index < 0 or index > len(self._list_items) - 1:
            return

        if index > self._max_list_item_index + self._scroll_view_index:
            self._scroll_view_index += 1
            for i, item in enumerate(self._list_items[self._selected_item_index - self._max_list_item_index:index + 1]):
                item.set_index(i - 1)
        elif index - self._scroll_view_index < 0:
            self._scroll_view_index -= 1
            for i, item in enumerate(self._list_items[index:index + self._max_list_item_index + 2]):
                item.set_index(i)

        self._list_items[self._selected_item_index].set_selected(False)
        self._selected_item_index = index
        self._list_items[self._selected_item_index].set_selected(True)

    def set_border_radius(self, radius: int) -> None:
        self._border_radius = radius

    def set_padding_left(self, padding: float) -> None:
        super().set_padding_left(padding)

        for item in self._list_items:
            item.set_width(self.get_width() - self.get_padding_left() - self.get_padding_right())

    def set_selected_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._selected_color = Color(r, g, b, a)

        for item in self._list_items:
            item.set_selected_color(r, g, b, a)

    def set_color(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._color = Color(r, g, b, a)

        for item in self._list_items:
            item.set_color(r, g, b, a)

    def draw(self):
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_height()

        # List
        pygame.draw.rect(self._window, self._color, (x, y, width, height), border_radius=self._border_radius)

        super().draw()
