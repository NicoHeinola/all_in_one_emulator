from pygame import Color, Rect, Surface
import pygame
from ui.components.Drawable import Drawable, PositionType
from ui.components.Text import Text


class SearchInput(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        super().__init__(window, width, height, x, y)
        self._text_cursor = Text(window)
        self._text_cursor.set_font_size(18)
        self._text_cursor.set_color(255, 255, 255)
        self._text_cursor.set_position_type(PositionType.VERTICAL_CENTER)
        self._text_cursor.set_text("|")
        self._text_cursor.render_text()

        self._text = Text(window)
        self._text.set_font_size(18)
        self._text.set_color(255, 255, 255)
        self._text.set_position_type(PositionType.VERTICAL_CENTER)

        self._placeholder_text = Text(window, 0, 0, 0, 0)
        self._placeholder_text.set_font_size(18)
        self._placeholder_text.set_color(210, 210, 240)
        self._placeholder_text.set_position_type(PositionType.VERTICAL_CENTER)

        self.add_component(self._text)
        self.add_component(self._text_cursor)
        self.add_component(self._placeholder_text)

        self.set_padding_left(15)

        self._blink_counter: int = 0
        self._show_cursor: bool = False
        self._focused: bool = False

    def is_focused(self) -> bool:
        return self._focused

    def set_focus(self, focus: bool) -> None:
        if self._focused == focus:
            return

        self._focused = focus
        self._show_cursor = focus
        self._blink_counter = 0

    def get_text_input(self) -> str:
        return self._text.get_text()

    def set_text_input(self, text: str) -> None:
        self._text.set_text(text)
        self._text.render_text()
        self.recalculate_position()

    def recalculate_x(self) -> None:
        super().recalculate_x()

        self._text_cursor.set_x(self._text.get_width() - 4)
        self._text_cursor.recalculate_x()

    def set_placeholder_text_input(self, text: str) -> None:
        self._placeholder_text.set_text(text)
        self._placeholder_text.render_text()

    def draw(self) -> None:
        rect: Rect = pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height())
        pygame.draw.rect(self._window, self._color, rect, border_radius=15)

        if self._text.get_text() == "":
            self._placeholder_text.draw()
        else:
            self._text.draw()
        if self._show_cursor:
            self._text_cursor.draw()
        # super().draw()

    def update(self) -> None:
        super().update()

        if self._focused:
            self._blink_counter += 1
            if self._blink_counter > 25:
                self._blink_counter = 0
                self._show_cursor = not self._show_cursor
