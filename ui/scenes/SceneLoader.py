from typing import Dict, List

from scenes.Scene import Scene


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
