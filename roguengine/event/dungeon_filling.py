from roguengine.component.dungeon import DungeonComponent
from roguengine.esper import Event


class DungeonFillingEvent(Event):

    def __init__(self, dungeon: DungeonComponent):
        super().__init__()
        self.dungeon = dungeon
