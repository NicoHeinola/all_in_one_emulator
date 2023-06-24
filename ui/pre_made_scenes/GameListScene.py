from pygame import Color, Surface
from ui.InputActions import InputAction
from ui.components.Drawable import PositionType
from ui.components.Frame import ForceHorizontalLayout, Frame
from ui.components.ListComponent import ListComponent
from ui.scenes.Scene import Scene


class GameListScene(Scene):
    def __init__(self, window: Surface, scene_loader) -> None:
        super().__init__(window, scene_loader)
        self._game_list: ListComponent = None

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.NONE)
        self._add_element(frame)

        game_list = ListComponent(self._window, 700, 600, 0, 0)
        self._game_list = game_list
        game_list.set_color(154, 234, 172)
        game_list.set_selected_color(110, 200, 146)
        game_list.set_border_radius(15)
        game_list.set_padding_top(20)
        game_list.set_padding_bottom(20)
        game_list.set_position_type(PositionType.CENTER)

        for i in range(1, 32):
            game_list.add_list_item(f'Item {i}')

        game_list.set_selected_index(0)

        frame.add_component(game_list)

    def action_performed(self, action: InputAction):
        super().action_performed(action)

        if action == InputAction.DOWN:
            self._game_list.set_selected_index(self._game_list.get_selected_index() + 1)
        elif action == InputAction.UP:
            self._game_list.set_selected_index(self._game_list.get_selected_index() - 1)

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
