from typing import Tuple


class PositionComponent:

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def xy(self) -> Tuple[int, int]:
        return self._x, self._y

    def move(self, dx: int, dy: int):
        self._x += dx
        self._y += dy
