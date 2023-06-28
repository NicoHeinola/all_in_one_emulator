from typing import List
from pygame import Color, Surface
import pygame
from apis.VimmsLairAPI import VimmsLairEmulator, VimmsLairRegion, VimmsLairSearchAPI
from helpers.ConfigManager import ConfigManager
from helpers.RomManager import Rom, RomManager
from ui.InputActions import InputAction
from ui.components.Circle import Circle
from ui.components.Drawable import Drawable, PositionType
from ui.components.Frame import ForceHorizontalLayout, Frame
from ui.components.Image import Image
from ui.components.ListComponent import ListComponent
from ui.components.LoadingCircle import LoadingCircle
from ui.components.SearchInput import SearchInput
from ui.components.Select import Select
from ui.scenes.Scene import ActionFrom, Scene
import threading


class GameDownloadScene(Scene):
    def __init__(self, window: Surface, scene_loader) -> None:
        super().__init__(window, scene_loader)
        self._game_list: ListComponent = None
        self._rom_list = List[Rom]
        self._search_input: SearchInput = None
        self._emulator_select: Select = None
        self._search_button: Drawable = None
        self._loading_circle: LoadingCircle = None

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.NONE)
        self._add_element(frame)

        # Game list
        game_list = ListComponent(self._window, 800, 400, 0, 0)
        self._game_list = game_list
        game_list.set_color(154, 234, 172)
        game_list.set_selected_color(110, 200, 146)
        game_list.set_border_radius(15)
        game_list.set_padding_top(20)
        game_list.set_padding_bottom(20)
        game_list.set_y(frame.get_height() - game_list.get_height() - 50)
        game_list.set_position_type(PositionType.HORIZONTAL_CENTER)

        frame.add_component(game_list)
        game_list.recalculate_position()

        # Search
        search_frame = Frame(window, game_list.get_width(), 40)
        search_frame.set_force_horizontal_layout(ForceHorizontalLayout.SPACE_BETWEEN)
        search_frame.set_position_type(PositionType.HORIZONTAL_CENTER)
        search_frame.set_y(game_list.get_y() - search_frame.get_height() - 50)
        frame.add_component(search_frame)

        emulator_select = Select(window, game_list.get_width() / 3 * 1.8 - 20, 40, 0, 0)
        emulator_select.set_color(210, 220, 240)
        emulator_select.set_text('Choose emulator')

        for emulator in VimmsLairEmulator:
            emulator_select.add_list_item(emulator.value, emulator.name)

        emulator_select.set_list_item_color(210, 220, 240)
        self._emulator_select = emulator_select
        search_frame.add_component(emulator_select)

        search_input_frame = Frame(window, game_list.get_width() / 3 * 1.2, search_frame.get_height(), 0, 0)
        search_input_frame.set_force_horizontal_layout(ForceHorizontalLayout.SPACE_BETWEEN)
        search_input_frame.set_position_type(PositionType.RELATIVE)
        search_frame.add_component(search_input_frame)

        search_icon = Image(window, 0, search_input_frame.get_height() / 2)
        search_icon.set_position_type(PositionType.CENTER)
        search_icon.load_image_from('images/icons/search-icon.png', False)
        search_icon.set_aspect_ratio(1, True)

        search_icon_circle = Circle(window)
        search_icon_circle.set_width(search_input_frame.get_height())
        search_icon_circle.set_color(210, 220, 240)
        search_icon_circle.add_component(search_icon)
        self._search_button = search_icon_circle

        search_input = SearchInput(window, search_input_frame.get_width() - search_icon_circle.get_radius() * 2 - 20, search_input_frame.get_height(), 0, 0)
        search_input.set_color(120, 140, 210)
        search_input.set_placeholder_text_input('Write a game name here')
        search_input.set_text_input('Mario')
        self._search_input = search_input

        search_input_frame.add_component(search_input)
        search_input_frame.add_component(search_icon_circle)

        loading_circle = LoadingCircle(window)
        loading_circle.set_width(search_input_frame.get_height())
        loading_circle.set_color(235, 235, 245)
        loading_circle.set_position_type(PositionType.CENTER)
        loading_circle.set_visible(False)
        self._loading_circle = loading_circle
        self._game_list.add_component(loading_circle)

        # Calculate all element positions
        frame.recalculate_position()

    def _open_rom(self, index: int) -> None:
        rom: Rom = self._rom_list[index]
        rom.open()
        rom.make_top_most()
        rom.make_full_screen()

    def mouse_moved(self, x: int, y: int) -> None:
        super().mouse_moved(x, y)
        self._emulator_select.on_mouse_move(x, y)
        self._search_input.on_mouse_move(x, y)
        self._search_button.on_mouse_move(x, y)

    def keyboard_key_down(self, key_code, unicode) -> None:
        super().keyboard_key_down(key_code, unicode)

        if self._search_input.is_focused():
            current_text = self._search_input.get_text_input()
            if key_code == 8:  # Backspace
                self._search_input.set_text_input(current_text[:len(current_text) - 1])
            else:
                self._search_input.set_text_input(current_text + unicode)

    def action_performed(self, action: InputAction, action_from: ActionFrom):
        super().action_performed(action, action_from)

        # If user is typing
        if self._search_input.is_focused():
            if action_from == ActionFrom.MOUSE and action == InputAction.ACTIVATE and not self._search_input.is_hovered():
                self._search_input.set_focus(False)
            return

        if action == InputAction.DOWN:
            self._game_list.set_selected_index(self._game_list.get_selected_index() + 1)
        elif action == InputAction.UP:
            self._game_list.set_selected_index(self._game_list.get_selected_index() - 1)
        elif action == InputAction.ACTIVATE:
            if self._search_input.is_hovered():
                self._search_input.set_focus(True)
            else:
                self._search_input.set_focus(False)

            self._game_list.call_list_item_function()
        elif action == InputAction.BACK:
            self._scene_loader.set_active_scene("main-menu")

    def mouse_action_performed(self, action: InputAction, x: int, y: int) -> None:
        do_return: bool = False
        if not self._search_input.is_focused():
            if action == InputAction.ACTIVATE:
                self._emulator_select.on_click(x, y)
                do_return = True
            if self._search_button.is_hovered() and action == InputAction.ACTIVATE:
                self.search()
                do_return = True

        if do_return:
            return

        super().mouse_action_performed(action, x, y)

    def search(self) -> None:
        keyword = self._search_input.get_text_input()
        emulator = self._emulator_select.get_selected_item_value()
        if emulator is None:
            return
        print(emulator, keyword)

        self._game_list.empty_list_items()
        self._game_list.recalculate_position()
        self._loading_circle.set_visible(True)

        def thread_function(scene: GameDownloadScene, emulator: VimmsLairEmulator, keyword: str):
            roms = VimmsLairSearchAPI.search_roms(VimmsLairRegion.USA, VimmsLairEmulator[emulator], keyword)
            output_folder = ConfigManager.get_config()['rom_folder_path']
            for rom in roms:
                scene._game_list.add_list_item(rom.get_name(), lambda r=rom, output_folder=output_folder: r.download(output_folder))
                scene._game_list.recalculate_position()
                scene._game_list.set_selected_index(0)
            self._loading_circle.set_visible(False)

        thread = threading.Thread(target=lambda a=self, b=emulator, c=keyword: thread_function(a, b, c))
        thread.start()

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
