from typing import List
from pygame import Surface
import pygame
from ui.components.Drawable import Drawable, PositionType
from ui.components.Text import Text


class SelectItem(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._index: int = 0
        self._border_radius = 0
        self._text: Text = Text(window, 0, 0, 0, 0)
        self._text.set_font_size(18)
        self._text.set_position_type(PositionType.VERTICAL_CENTER)
        self.add_component(self._text)

        self._value: str = ""

        self._parent: Select = None

    def set_text(self, text: str) -> None:
        self._text.set_text(text)
        self._text.render_text()

    def get_text(self) -> str:
        return self._text.get_text()

    def set_value(self, value: str) -> None:
        self._value = value

    def get_value(self) -> str:
        return self._value

    def set_index(self, index: int) -> None:
        self._index = index

    def recalculate_y(self) -> None:
        super().recalculate_y()
        self._draw_y += self.get_height() * self.get_index()
        if self._parent is not None:
            self._draw_y += self._parent.get_height()
        self._recalculate_children_y()

    def on_click(self, x: int, y: int) -> None:
        super().on_click(x, y)

        if self.is_hovered() and self._parent is not None:
            self._parent.set_selected_index(self.get_index())

    def get_index(self) -> int:
        return self._index

    def draw(self) -> None:
        pygame.draw.rect(self._window, self.get_current_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()), border_bottom_left_radius=self.get_border_radius_bottom_left(), border_bottom_right_radius=self.get_border_radius_bottom_right())

        super().draw()


class Select(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._list_items: List[SelectItem] = []
        self._opened: bool = False
        self._selected_index: int = -1

        self._text: Text = Text(window, 0, 0, 0, 0)
        self._text.set_font_size(18)
        self._text.set_position_type(PositionType.VERTICAL_CENTER)
        self.add_component(self._text)

    def set_text(self, text: str) -> None:
        self._text.set_text(text)
        self._text.render_text()
        self._text.set_x(15)
        self._text.recalculate_position()

    def add_list_item(self, text: str, value: str) -> None:
        list_item = SelectItem(self._window, self.get_width(), 50, 0, 0)
        list_item.set_index(len(self._list_items))
        list_item.set_color(self.get_color().r, self.get_color().g, self.get_color().b, self.get_color().a)
        list_item.set_border_radius_bottom_left(15)
        list_item.set_border_radius_bottom_right(15)
        list_item.set_padding_left(15)
        list_item.set_text(text)
        list_item.set_value(value)
        for existing_list_item in self._list_items:
            existing_list_item.set_border_radius_bottom_left(0)
            existing_list_item.set_border_radius_bottom_right(0)
        self._list_items.append(list_item)
        self.add_component(list_item)

    def set_selected_index(self, index: int) -> None:
        list_index = index
        if self._selected_index != -1 and index >= self._selected_index:
            list_index += 1

        component = self._list_items[list_index]
        self.remove_component(component)

        if self._selected_index != -1:
            add_component_back = self._list_items[self._selected_index]
            add_component_back.set_is_hovered(False)
            self.add_component(add_component_back)

            for component in self._list_items[self._selected_index + 1:]:
                component.set_index(component.get_index() + 1)
                component.recalculate_y()

        if list_index == len(self._list_items) - 1:
            new_top_list_item = self._list_items[len(self._list_items) - 2]
            new_top_list_item.set_border_radius_bottom_right(15)
            new_top_list_item.set_border_radius_bottom_left(15)
        elif self._selected_index == len(self._list_items) - 1:
            new_top_list_item = self._list_items[len(self._list_items) - 1]
            new_top_list_item.set_border_radius_bottom_right(15)
            new_top_list_item.set_border_radius_bottom_left(15)

            old_top_list_item = self._list_items[len(self._list_items) - 2]
            old_top_list_item.set_border_radius_bottom_right(0)
            old_top_list_item.set_border_radius_bottom_left(0)

        self._selected_index = list_index

        hidden_list_item = self._list_items[list_index]
        self._text.set_text(hidden_list_item.get_text())
        self._text.render_text()
        self._text.set_x(15)
        self._text.recalculate_position()

        for component in self._list_items[list_index + 1:]:
            component.set_index(component.get_index() - 1)
            component.recalculate_y()

        self.set_open(not self.is_opened())

    def has_selected_item(self) -> bool:
        return self._selected_index != -1

    def get_selected_item_text(self) -> str:
        if self.has_selected_item():
            return self._list_items[self._selected_index].get_text()
        return None

    def get_selected_item_value(self) -> str:
        if self.has_selected_item():
            return self._list_items[self._selected_index].get_value()
        return None

    def set_open(self, open: bool) -> None:
        self._opened = open
        if open:
            self.set_border_radius_bottom_right(0)
            self.set_border_radius_bottom_left(0)
        else:
            self.set_border_radius_bottom_right(15)
            self.set_border_radius_bottom_left(15)

    def on_click(self, x: int, y: int) -> None:
        super().on_click(x, y)

        if self.is_hovered():
            self.set_open(not self.is_opened())

    def on_click_children(self, x: int, y: int) -> None:
        if self.is_opened():
            super().on_click_children(x, y)

    def is_opened(self) -> bool:
        return self._opened

    def set_list_item_color(self, r: int, g: int, b: int, a: int = 255):
        for list_item in self._list_items:
            list_item.set_color(r, g, b, a)

    def draw(self) -> None:
        pygame.draw.rect(self._window, self.get_current_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()), border_top_left_radius=self.get_border_radius_top_left(), border_top_right_radius=self.get_border_radius_top_right(), border_bottom_left_radius=self.get_border_radius_bottom_left(), border_bottom_right_radius=self.get_border_radius_bottom_right())
        if self.is_opened():
            super().draw()
        else:
            self._text.draw()
