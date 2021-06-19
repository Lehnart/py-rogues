from typing import List

from roguengine.component.fighter import FighterComponent
from roguengine.component.gold import GoldComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.esper import Processor
from roguengine.event.fight import FightEvent
from roguengine.event.gold_pickup import GoldPickUpEvent
from roguengine.event.log import LogEvent
from roguengine.event.move import MoveEvent


class MoveProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        messages: List[MoveEvent] = self.world.receive(MoveEvent)
        for msg in messages:
            ent, move = msg.entity, msg.movement

            if ent not in self.world.entities():
                continue

            pos = self.world.component_for_entity(ent, PositionComponent)
            sprite = self.world.component_for_entity(ent, VisibleSpriteComponent)

            x, y = pos.xy()
            dx, dy = move.dx_dy()

            fighting_entities = self.get_entities_at(x + dx, y + dy, FighterComponent)
            if fighting_entities:
                self.world.publish(FightEvent(ent, fighting_entities[0]))
                continue

            if not self.get_entities_at(x + dx, y + dy, MovableComponent):
                continue

            gold_entities = self.get_entities_at(x + dx, y + dy, GoldComponent)
            if gold_entities:
                self.world.publish(GoldPickUpEvent(gold_entities[0]))

            pos.move(dx, dy)
            sprite.move(dx, dy)

    def get_entities_at(self, x: int, y: int, *component_types):
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities
