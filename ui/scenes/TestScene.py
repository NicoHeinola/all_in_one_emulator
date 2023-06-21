from scenes.Scene import Scene
from components.List import List


class TestScene(Scene):
    def __init__(self, window) -> None:
        super().__init__(window)

        list1 = List(window, 100, 100)
        list1.set_color(255, 0, 0)
        list1.set_border_color(0, 255, 0)
        list1.set_border_size(10)
        self._add_element(list1)
