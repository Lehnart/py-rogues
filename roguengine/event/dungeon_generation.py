from typing import Optional

from roguengine.esper import Event


class DungeonGenerationEvent(Event):

    def __init__(self, dungeon: Optional):
        super().__init__()
        self.dungeon = dungeon
