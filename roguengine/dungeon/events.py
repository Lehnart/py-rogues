from typing import Optional, Tuple

from roguengine.dungeon.components import DungeonComponent
from roguengine.rogue_esper import Event


class DungeonCreationEvent(Event):

    def __init__(self, dungeon: DungeonComponent):
        super().__init__()
        self.dungeon = dungeon


class DungeonFillingEvent(Event):

    def __init__(self, dungeon: DungeonComponent):
        super().__init__()
        self.dungeon = dungeon


class DungeonGenerationEvent(Event):

    def __init__(self, dungeon: Optional):
        super().__init__()
        self.dungeon = dungeon


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
