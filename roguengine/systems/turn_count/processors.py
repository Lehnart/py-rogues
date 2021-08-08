from typing import List

from roguengine.rogue_esper import Processor
from roguengine.systems.turn_count.components import TurnCountComponent
from roguengine.systems.turn_count.events import NewTurnEvent


class TurnCounterProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        events: List[NewTurnEvent] = self.world.receive(NewTurnEvent)
        for _ in events:
            turn_counts = self.world.get_component(TurnCountComponent)
            for turn_count_ent, turn_count_component in turn_counts:
                turn_count_component.next()
