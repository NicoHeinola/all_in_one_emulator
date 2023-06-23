from pygame import Color, Surface
from ui.components.Drawable import PositionType
from ui.components.Frame import ForceHorizontalLayout, Frame
from ui.components.ListComponent import ListComponent
from ui.scenes.Scene import Scene


class GameListScene(Scene):
    def __init__(self, window: Surface, scene_loader) -> None:
        super().__init__(window, scene_loader)

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.NONE)
        self._add_element(frame)

        game_list = ListComponent(self._window, 700, 600, 0, 0)
        game_list.set_color(154, 234, 172)
        game_list.set_position_type(PositionType.CENTER)
        frame.add_component(game_list)

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
