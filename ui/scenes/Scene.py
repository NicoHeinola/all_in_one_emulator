from typing import Dict, List

from pygame import Surface
from ui.InputActions import InputAction
from ui.components.Drawable import Drawable


class Scene:
    def __init__(self, window: Surface, scene_loader) -> None:
        from ui.scenes.Scene import SceneLoader
        self._window: Surface = window
        self._scene_loader: SceneLoader = scene_loader
        self._elements: List[Drawable] = []
        self._mouse_x: int = 0
        self._mouse_y: int = 0

    def create_elements(self) -> None:
        self._empty_elements()

    def _add_element(self, element: Drawable) -> None:
        self._elements.append(element)

    def _empty_elements(self) -> None:
        self._elements = []

    def action_performed(self, action: InputAction):
        pass

    def mouse_action_performed(self, action: InputAction) -> None:
        self.action_performed(action)

    def mouse_moved(self, x: int, y: int) -> None:
        self._mouse_x = x
        self._mouse_y = y

    def joystick_key_down(self, key_code) -> None:
        pass

    def keyboard_key_down(self, key_code) -> None:
        pass

    def draw(self) -> None:
        for element in self._elements:
            element.draw()

    def update(self) -> None:
        for element in self._elements:
            element.update()


class SceneLoader:

    def __init__(self) -> None:
        self._scenes: Dict[str, Scene] = {}
        self._active_scene: Scene = None

    def add_scene(self, title: str, scene: Scene):
        self._scenes[title] = scene

    def set_active_scene(self, title: str):
        self._active_scene = self._scenes[title]

    def get_active_scene(self) -> Scene:
        return self._active_scene

    def build_scenes(self) -> None:
        for scene in self._scenes.values():
            scene.create_elements()
