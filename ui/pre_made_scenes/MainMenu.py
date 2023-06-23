import sys
from ui.components.Frame import Frame, ForceHorizontalLayout
from ui.components.Image import Image
from ui.components.Drawable import PositionType
from ui.components.Drawable import Drawable
from ui.components.CardItem import CardItem
from ui.components.List import List
from ui.scenes.Scene import Scene
import pygame
from pygame import Color, Surface
sys.path.append(fr'./')
print(sys.path)
from helpers.ConfigManager import ConfigManager


class MainMenu(Scene):
    def __init__(self, window: Surface) -> None:
        super().__init__(window)

        self._selected_card_index: int = 0

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.SPACE_EVENLY)
        self._add_element(frame)

        games_card_item = CardItem(window, 300, 400)
        games_card_item.set_color(153, 225, 235)
        games_card_item.set_position_type(PositionType.VERTICAL_CENTER)
        games_card_item.load_image('images/icons/game-controller.png')
        frame.add_component(games_card_item)

        games_card_item = CardItem(window, 300, 400)
        games_card_item.set_color(153, 225, 235)
        games_card_item.set_position_type(PositionType.VERTICAL_CENTER)
        games_card_item.load_image('images/icons/game-controller.png')
        frame.add_component(games_card_item)

        games_card_item = CardItem(window, 300, 400)
        games_card_item.set_color(153, 225, 235)
        games_card_item.set_position_type(PositionType.VERTICAL_CENTER)
        games_card_item.load_image('images/icons/game-controller.png')
        frame.add_component(games_card_item)

        frame.recalculate_position()

    def _set_card_selected_index(self, index: int) -> None:
        self._selected_card_index = index

    def keyboard_key_down(self, key_code) -> None:
        super().keyboard_key_down(key_code)

        print(ConfigManager.get_actions_per_keycodes()['keyboard'][key_code])

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
