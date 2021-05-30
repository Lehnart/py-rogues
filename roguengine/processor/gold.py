from queue import Queue

from roguengine.component.gold import GoldComponent
from roguengine.component.goldbag import GoldBagComponent
from roguengine.component.player import PlayerComponent
from roguengine.esper import Processor
from roguengine.event.gold_pickup import GoldPickUpEvent
from roguengine.event.log import LogEvent


class GoldProcessor(Processor):

    def __init__(self):
        super().__init__()
        self._queue = Queue()

    def process(self):
        for msg in self.world.receive(GoldPickUpEvent):
            gold_entity = msg.gold_ent
            gold_component: GoldComponent = self.world.component_for_entity(gold_entity, GoldComponent)
            player, [player_component, gold_bag_component] = \
                self.world.get_components(PlayerComponent, GoldBagComponent)[0]

            gold_amount = gold_component.random_amount()
            gold_bag_component.add(gold_amount)
            self.world.publish(LogEvent("You've picked up " + str(gold_amount) + " golds."))
            self.world.delete_entity(gold_entity, True)
