import sys
from typing import List
from ui.InputActions import InputAction
from ui.components.Frame import Frame, ForceHorizontalLayout
from ui.components.Image import Image
from ui.components.Drawable import PositionType
from ui.components.Drawable import Drawable
from ui.components.CardItem import CardItem
from ui.scenes.Scene import Scene, SceneLoader
import pygame
from pygame import Color, Surface
from helpers.ConfigManager import ConfigManager


class MainMenuScene(Scene):
    def __init__(self, window: Surface, scene_loader: SceneLoader) -> None:
        super().__init__(window, scene_loader)

        self._selected_card_index: int = 0
        self._menu_components: List[Drawable] = []

    def create_elements(self) -> None:
        super().create_elements()

        self._menu_components = []

        window = self._window
        card_width = 300
        card_height = 400

        frame = Frame(window, window.get_width(), window.get_height())
        frame.set_force_horizontal_layout(ForceHorizontalLayout.CENTER)
        frame.set_horizontal_gap(50)
        self._add_element(frame)

        animation_speed = 4

        games_card_item = CardItem(window, card_width, card_height)
        games_card_item.set_size_animation_speed(animation_speed)
        games_card_item.set_color(153, 225, 235)
        games_card_item.set_position_type(PositionType.VERTICAL_CENTER)
        games_card_item.load_image('images/icons/download-game.png')
        games_card_item.set_text('Download Games')
        frame.add_component(games_card_item)
        self._menu_components.append(games_card_item)

        games_card_item = CardItem(window, card_width, card_height)
        games_card_item.set_size_animation_speed(animation_speed)
        games_card_item.set_color(153, 225, 235)
        games_card_item.set_position_type(PositionType.VERTICAL_CENTER)
        games_card_item.load_image('images/icons/game-controller.png')
        frame.add_component(games_card_item)
        self._menu_components.append(games_card_item)

        frame.recalculate_position()

        self._set_card_selected_index(1)

    def _set_card_selected_index(self, index: int) -> None:
        if index > len(self._menu_components) - 1:
            index = 0
        elif index < 0:
            index = len(self._menu_components) - 1

        from_component: Drawable = self._menu_components[self._selected_card_index]
        to_component: Drawable = self._menu_components[index]
        self._selected_card_index = index

        from_component.set_animated_width(300)
        from_component.set_animated_height(400)
        to_component.set_animated_width(350)
        to_component.set_animated_height(450)

    def action_performed(self, action: InputAction):
        super().action_performed(action)

        if action == InputAction.RIGHT:
            self._set_card_selected_index(self._selected_card_index + 1)
        elif action == InputAction.LEFT:
            self._set_card_selected_index(self._selected_card_index - 1)
        elif action == InputAction.ACTIVATE:
            self._scene_loader.set_active_scene('game-list')

    def draw(self) -> None:
        self._window.fill(Color(255, 255, 255))

        super().draw()
