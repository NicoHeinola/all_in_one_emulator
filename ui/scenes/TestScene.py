from pygame import Color, Surface
import pygame
from scenes.Scene import Scene
from components.List import List
from components.CardItem import CardItem
from components.Drawable import Drawable
from components.Drawable import PositionType
from components.Image import Image


class TestScene(Scene):
    def __init__(self, window: Surface) -> None:
        super().__init__(window)

    def create_elements(self) -> None:
        super().create_elements()

        window = self._window
        list1 = List(window, 100, 100)
        list1.set_color(255, 0, 0)
        list1.set_border_color(153, 225, 235)
        list1.set_border_size(10)
        # self._add_element(list1)

        frame = Drawable(window, window.get_width(), window.get_height())
        self._add_element(frame)

        carditem = CardItem(window, 300, 400)
        carditem.set_color(153, 225, 235)
        carditem.set_position_type(PositionType.CENTER)
        carditem.load_image('images/icons/game-controller.png')

        frame.add_component(carditem)
        frame.recalculate_position()

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
