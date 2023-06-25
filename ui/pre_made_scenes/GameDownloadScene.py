from typing import List
from pygame import Color, Surface
from helpers.RomManager import Rom, RomManager
from ui.InputActions import InputAction
from ui.components.Drawable import PositionType
from ui.components.Frame import ForceHorizontalLayout, Frame
from ui.components.ListComponent import ListComponent
from ui.scenes.Scene import Scene


class GameDownloadScene(Scene):
    def __init__(self, window: Surface, scene_loader) -> None:
        super().__init__(window, scene_loader)
        self._game_list: ListComponent = None
        self._rom_list = List[Rom]

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.NONE)
        self._add_element(frame)

        # Game list
        game_list = ListComponent(self._window, 500, 400, 0, 0)
        self._game_list = game_list
        game_list.set_color(154, 234, 172)
        game_list.set_selected_color(110, 200, 146)
        game_list.set_border_radius(15)
        game_list.set_padding_top(20)
        game_list.set_padding_bottom(20)
        game_list.set_y(frame.get_height() - game_list.get_height() - 50)
        game_list.set_position_type(PositionType.HORIZONTAL_CENTER)

        for i in range(100):
            game_list.add_list_item(f'Game {i}', lambda i=i: print(f'Game {i}'))
        game_list.set_selected_index(0)

        frame.add_component(game_list)

        # Search
        search_frame = Frame(window, game_list.get_width(), 50)
        frame.add_component(search_frame)

    def _open_rom(self, index: int) -> None:
        rom: Rom = self._rom_list[index]
        rom.open()
        rom.make_top_most()
        rom.make_full_screen()

    def action_performed(self, action: InputAction):
        super().action_performed(action)

        if action == InputAction.DOWN:
            self._game_list.set_selected_index(self._game_list.get_selected_index() + 1)
        elif action == InputAction.UP:
            self._game_list.set_selected_index(self._game_list.get_selected_index() - 1)
        elif action == InputAction.ACTIVATE:
            self._game_list.call_list_item_function()
        elif action == InputAction.BACK:
            self._scene_loader.set_active_scene("main-menu")

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
