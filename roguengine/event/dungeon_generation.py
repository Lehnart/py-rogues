from typing import Optional

from roguengine.rogue_esper import Event


class DungeonGenerationEvent(Event):

    def __init__(self, dungeon: Optional):
        super().__init__()
        self.dungeon = dungeon
