from typing import Tuple

from roguengine.rogue_esper import Event


class Movement:
    def __init__(self, dx: int, dy: int):
        self._dx = dx
        self._dy = dy

    def dx_dy(self) -> Tuple[int, int]:
        return self._dx, self._dy


class MoveEvent(Event):

    def __init__(self, entity: int, movement: Movement, is_player: bool = False):
        super().__init__()
        self.entity = entity
        self.movement = movement
        self.is_player = is_player