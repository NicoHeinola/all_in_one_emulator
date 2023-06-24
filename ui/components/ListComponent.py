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
        self.add_component(self._text)

    def get_y(self) -> int:
        y = super().get_y()
        y += self.get_height() * self._index
        return y

    def get_index(self) -> int:
        return self._index

    def set_parent(self, parent) -> None:
        super().set_parent(parent)

        self._recalculate_is_in_view()

    def _recalculate_is_in_view(self) -> None:
        if self._parent is None:
            self._is_in_view = False
            return

        self._is_in_view = True
        max_y = self._parent.get_height() - self._parent.get_padding_bottom() - self.get_height()
        y = self.get_y()

        if y > max_y:
            self._is_in_view = False

    def set_selected(self, selected: bool) -> None:
        self._is_selected = selected

    def set_text(self, text: str) -> None:
        self._text.set_text(text)

    def set_index(self, index: int) -> None:
        self._index = index
        self._recalculate_is_in_view()

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
        self._scroll_view_index: int = 0
        self._list_items: List[VerticalListItem] = []

    def add_list_item(self, text: str) -> None:
        index = len(self._list_items)
        item = VerticalListItem(self._window, self.get_width() - self.get_padding_left() - self.get_padding_right(), 30)
        item.set_position_type(PositionType.RELATIVE)
        item.set_index(index)
        item.set_text(text)
        item.set_padding_left(15)
        item.set_color(self._color.r, self._color.g, self._color.b, self._color.a)
        item.set_selected(False)
        item.set_selected_color(self._selected_color.r, self._selected_color.g, self._selected_color.b, self._selected_color.a)
        self._list_items.append(item)
        self.add_component(item)

    def get_selected_index(self) -> int:
        return self._selected_item_index

    def set_selected_index(self, index: int) -> None:
        if index < 0 or index > len(self._list_items) - 1:
            return
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
