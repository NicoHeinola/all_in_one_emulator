from enum import Enum
from typing import List
from pygame import Surface
from ui.components.Drawable import Drawable
from ui.components.Drawable import PositionType


class ForceHorizontalLayout(Enum):
    NONE = 0
    SPACE_BETWEEN = 1
    SPACE_EVENLY = 2
    CENTER = 3


class Frame(Drawable):
    def __init__(self, window: Surface, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        self._force_horizontal_layout: ForceHorizontalLayout = ForceHorizontalLayout.NONE
        self._horizontal_gap: float = 0
        self._children_can_affect_layout: bool = True

        super().__init__(window, width, height, x, y)

    def set_children_can_affect_layout(self, children_can_affect_layout: bool) -> None:
        self._children_can_affect_layout = children_can_affect_layout

    def set_horizontal_gap(self, gap: float) -> None:
        self._horizontal_gap = gap

    def set_force_horizontal_layout(self, force_horizontal_layout: ForceHorizontalLayout) -> None:
        self._force_horizontal_layout = force_horizontal_layout

    def recalculate_x(self) -> None:
        super().recalculate_x()
        self._recalculate_horizontal_layout()

    def _child_width_updated(self, child: Drawable) -> None:
        super()._child_width_updated(child)

        if self._children_can_affect_layout:
            self._recalculate_horizontal_layout()

    def _recalculate_horizontal_layout(self) -> None:
        if self._force_horizontal_layout != ForceHorizontalLayout.NONE:
            component_widths = [component.get_width() for component in self._components]
            if self._force_horizontal_layout == ForceHorizontalLayout.SPACE_BETWEEN:
                component_positions = Frame.calculate_space_between_positions(component_widths, self.get_x(), self.get_width())
            elif self._force_horizontal_layout == ForceHorizontalLayout.SPACE_EVENLY:
                component_positions = Frame.calculate_space_evenly_positions(component_widths, self.get_x(), self.get_width())
            elif self._force_horizontal_layout == ForceHorizontalLayout.CENTER:
                component_positions = Frame.calculate_center_positions(component_widths, self.get_x(), self.get_width(), self._horizontal_gap)
            for index, component in enumerate(self._components):
                component.set_x(component_positions[index])
                component.recalculate_x()

    @staticmethod
    def calculate_center_positions(element_widths: List[float], start_pos: int, width: float, gap: int = 0) -> List[int]:
        element_count = len(element_widths) + 1
        if element_count == 1:
            return [0]

        left_over_space = width
        for index, width in enumerate(element_widths):
            left_over_space -= width
        space = left_over_space / 2
        space -= gap * (element_count - 2)

        x = 0
        element_positions = []
        for index, element_width in enumerate(element_widths):
            if index == element_count - 1:
                gap = 0
            element_positions.append(space + x + gap)
            x += element_width + gap

        return element_positions

    @staticmethod
    def calculate_space_evenly_positions(element_widths: List[float], start_pos: int, width: float) -> List[int]:
        element_count = len(element_widths) + 1
        if element_count == 1:
            return []

        left_over_space = width
        for width in element_widths:
            left_over_space -= width
        space_per_component = left_over_space / element_count

        x = 0
        element_positions = []
        for index, element_width in enumerate(element_widths):
            element_positions.append(start_pos + space_per_component + x)
            x += element_width + space_per_component

        return element_positions

    @staticmethod
    def calculate_space_between_positions(element_widths: List[float], start_pos: int, width: float) -> List[int]:
        element_count = len(element_widths)
        if element_count == 1:
            return [0]

        left_over_space = width
        for width in element_widths:
            left_over_space -= width
        space_per_component = left_over_space / (element_count - 1)

        x = 0
        element_positions = []
        for index, element_width in enumerate(element_widths):
            if index == 0:
                space = 0
            else:
                space = space_per_component

            element_positions.append(start_pos + space + x)
            x += element_width + space

        return element_positions
