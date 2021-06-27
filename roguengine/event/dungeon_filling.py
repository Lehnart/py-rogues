from roguengine.component.dungeon import DungeonComponent
from roguengine.rogue_esper import Event


class DungeonFillingEvent(Event):

    def __init__(self, dungeon: DungeonComponent):
        super().__init__()
        self.dungeon = dungeon
