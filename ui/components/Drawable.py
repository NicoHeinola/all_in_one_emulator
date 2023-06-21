class Drawable:
    def __init__(self, window, width: float = 0, height: float = 0, x: int = 0, y: int = 0) -> None:
        self._window = window
        self._x: int = x
        self._y: int = y
        self._width: float = width
        self._height: float = height

    def set_width(self, width: float) -> None:
        self._width = width

    def set_height(self, height: float) -> None:
        self._height = height

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def set_x(self, x: int) -> None:
        self._x = x

    def set_y(self, y: int) -> None:
        self._y = y

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def draw(self):
        pass

    def update(self):
        pass
