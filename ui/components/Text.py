from enum import Enum
import os
from typing import Dict, List
from pygame import Color, Surface
import pygame
from components.Drawable import Drawable


class TextAlign(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2


class Text(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        self._text: str = ""
        self._font_size: int = 60
        self._font_name: str = ''
        self._font: pygame.font.Font = None
        self._color = Color(0, 0, 0)

        self._text_surfaces: List[Surface] = []
        self._text_surface_positions: List[Dict[str, int]] = []
        self._text_align: TextAlign = TextAlign.LEFT
        self._text_push_down: bool = True

        self._word_wrap: bool = False
        self._max_width: float = 0

        super().__init__(window, width, height, x, y)

        self.set_font_from_fonts('OpenSans-VariableFont.ttf')

    def _get_text_line_x(self, line_index: int) -> int:
        return self._text_surface_positions[line_index]['x']

    def _get_text_line_y(self, line_index: int) -> int:
        return self._text_surface_positions[line_index]['y']

    def _set_text_line_x(self, line_index: int, x: int) -> None:
        if line_index > len(self._text_surface_positions) - 1:
            position = {'x': x, 'y': self.get_y()}
            self._text_surface_positions.append(position)
        else:
            position = {'x': x, 'y': self._get_text_line_y(line_index)}
            self._text_surface_positions[line_index] = position

    def _set_text_line_y(self, line_index: int, y: int) -> None:
        if line_index > len(self._text_surface_positions) - 1:
            position = {'x': self.get_x(), 'y': y}
            self._text_surface_positions.append(position)
        else:
            position = {'x': self._get_text_line_x(line_index), 'y': y}
            self._text_surface_positions[line_index] = position

    def get_text(self) -> str:
        return self._text

    def set_text_push_down(self, text_push_down: bool) -> None:
        self._text_push_down = text_push_down
        self._render_text()

    def set_parent(self, parent):
        super().set_parent(parent)
        self._max_width = self._parent.get_width()

    def set_max_width(self, max_width: float) -> None:
        self._max_width = max_width
        self._render_text()

    def set_text_align(self, text_align: TextAlign) -> None:
        self._text_align = text_align

    def set_word_wrap(self, word_wrap: bool) -> None:
        self._word_wrap = word_wrap
        self._render_text()

    def set_color(self, r: int, g: int, b: int, a: int = 255):
        self._color = Color(r, g, b, a)
        self._render_text()

    def set_font(self, font: pygame.font.Font) -> None:
        self._font = font
        self._render_text()

    def set_font_from_fonts(self, font_name: str) -> None:
        self._font_name = font_name
        self._font = pygame.font.Font(os.path.join("fonts", font_name), self._font_size)
        self._render_text()

    def set_font_size(self, size: int) -> None:
        self._font_size = size
        self._font = pygame.font.Font(os.path.join("fonts", self._font_name), self._font_size)
        self._render_text()

    def set_text(self, text: str) -> None:
        self._text = text
        self._render_text()

    def _render_text(self) -> None:
        self._text_surfaces = []

        if self._font is None:
            return

        if self._word_wrap:
            # Word wrap
            text = self._text
            words = text.split()
            current_line = ""
            for word in words:
                # If current line is NOT wider than max
                if self._font.size(current_line + " " + word)[0] <= self._max_width:
                    current_line += " " + word
                else:
                    rendered_text: Surface = self._font.render(current_line.lstrip(), True, self._color)
                    self._text_surfaces.append(rendered_text)

                    # Properly set height of this text class
                    rendered_text_width = rendered_text.get_width()
                    rendered_text_height = rendered_text.get_height()

                    if rendered_text_width > self.get_width():
                        self.set_width(rendered_text_width)

                    self.set_height(self.get_height() + rendered_text_height)
                    current_line = word

            rendered_text = self._font.render(current_line.lstrip(), True, self._color)
            self._text_surfaces.append(rendered_text)

            # Properly set height of this text class
            rendered_text_width = rendered_text.get_width()
            rendered_text_height = rendered_text.get_height()
            if rendered_text_width > self.get_width():
                self.set_width(rendered_text_width)
            self.set_height(self.get_height() + rendered_text_height)

        else:
            rendered_text: Surface = self._font.render(self._text, True, self._color)
            self._text_surfaces.append(rendered_text)
            self.set_width(rendered_text.get_width())
            self.set_height(rendered_text.get_height())

        self.recalculate_text_lines_x()
        self.recalculate_text_lines_y()

    def recalculate_x(self) -> None:
        super().recalculate_x()
        self.recalculate_text_lines_x()

    def recalculate_y(self) -> None:
        super().recalculate_y()
        self.recalculate_text_lines_y()

    def recalculate_text_lines_x(self):
        width = self.get_width()
        x = self.get_x()

        for index, text_line in enumerate(self._text_surfaces):
            if self._text_align == TextAlign.LEFT:
                self._set_text_line_x(index, x)
            elif self._text_align == TextAlign.CENTER:
                text_line_width = text_line.get_width()
                text_line_x = Drawable.get_center(x, text_line_width, width)
                self._set_text_line_x(index, text_line_x)
            elif self._text_align == TextAlign.RIGHT:
                text_line_width = text_line.get_width()
                text_line_x = Drawable.get_right_most(x, text_line_width, width)
                self._set_text_line_x(index, text_line_x)

    def recalculate_text_lines_y(self):
        if self._font is None:
            return

        y = self.get_y()
        line_height = self._font.get_linesize()

        for index, text_line in enumerate(self._text_surfaces):
            self._set_text_line_y(index, y)

            if self._text_push_down:
                y += line_height
            else:
                y -= line_height * (len(self._text_surfaces) - 2)

    def draw(self) -> None:
        for index, line in enumerate(self._text_surfaces):
            text_x = self._get_text_line_x(index)
            text_y = self._get_text_line_y(index)
            self._window.blit(line, (text_x, text_y))

        return super().draw()
