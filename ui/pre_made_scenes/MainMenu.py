from pygame import Color, Surface
import pygame
from scenes.Scene import Scene
from components.List import List
from components.CardItem import CardItem
from components.Drawable import Drawable
from components.Drawable import PositionType
from components.Image import Image
from components.Frame import Frame, ForceHorizontalLayout


class MainMenu(Scene):
    def __init__(self, window: Surface) -> None:
        super().__init__(window)

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.CENTER)
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

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
