from typing import Optional

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
