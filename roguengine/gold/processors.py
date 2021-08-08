from roguengine.gold.components import GoldComponent, GoldBagComponent
from roguengine.gold.events import GoldPickUpEvent
from roguengine.log.events import LogEvent
from roguengine.rogue_esper import Processor


class GoldProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for msg in self.world.receive(GoldPickUpEvent):
            gold_entity = msg.gold_ent
            picker_ent = msg.picker_ent

            gold_component: GoldComponent = self.world.component_for_entity(gold_entity, GoldComponent)
            if not self.world.has_component(picker_ent, GoldBagComponent):
                continue

            gold_bag_component = self.world.component_for_entity(picker_ent, GoldBagComponent)
            gold_amount = gold_component.random_amount()
            gold_bag_component.add(gold_amount)
            self.world.publish(LogEvent("You've picked up " + str(gold_amount) + " golds."))
            self.world.delete_entity(gold_entity, True)
