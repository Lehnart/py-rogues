from roguengine.component.dungeon.dungeon import DungeonComponent
from roguengine.rogue_esper import Event


class DungeonCreationEvent(Event):

    def __init__(self, dungeon: DungeonComponent):
        super().__init__()
        self.dungeon = dungeon
