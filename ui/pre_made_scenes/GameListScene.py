from typing import List
from pygame import Color, Surface
from helpers.RomManager import Rom, RomManager
from ui.InputActions import InputAction
from ui.components.Drawable import PositionType
from ui.components.Frame import ForceHorizontalLayout, Frame
from ui.components.ListComponent import ListComponent
from ui.scenes.Scene import Scene


class GameListScene(Scene):
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

        game_list = ListComponent(self._window, 700, 600, 0, 0)
        self._game_list = game_list
        game_list.set_color(154, 234, 172)
        game_list.set_selected_color(110, 200, 146)
        game_list.set_border_radius(15)
        game_list.set_padding_top(20)
        game_list.set_padding_bottom(20)
        game_list.set_position_type(PositionType.CENTER)

        self._rom_list = RomManager.get_rom_list()

        game_list.add_list_item("Go back", lambda: self._scene_loader.set_active_scene('main-menu'))

        for i, rom in enumerate(self._rom_list):
            game_list.add_list_item(rom.get_name_with_extension(), lambda i=i: self._open_rom(i))

        game_list.set_selected_index(0)

        frame.add_component(game_list)

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

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
