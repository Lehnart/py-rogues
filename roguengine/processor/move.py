from typing import List

from roguengine.dungeon.components import DungeonResidentComponent
from roguengine.component.movable import MovableComponent
from roguengine.component.player import PlayerComponent
from roguengine.dungeon.components import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent
from roguengine.event.ai import AIEvent
from roguengine.event.move import MoveEvent
from roguengine.turn_count.events import NewTurnEvent
from roguengine.fight.components import FighterComponent
from roguengine.fight.events import FightEvent
from roguengine.gold.components import GoldComponent, GoldBagComponent
from roguengine.gold.events import GoldPickUpEvent
from roguengine.rogue_esper import Processor


class MoveProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        messages: List[MoveEvent] = self.world.receive(MoveEvent)
        for msg in messages:
            ent, move = msg.entity, msg.movement

            if not self.world.entity_exists(ent):
                continue

            pos = self.world.component_for_entity(ent, PositionComponent)
            sprite = self.world.component_for_entity(ent, VisibleSpriteComponent)

            x, y = pos.xy()
            dx, dy = move.dx_dy()

            fighting_entities = self.get_entities_at(x + dx, y + dy, FighterComponent)
            if self.world.has_component(ent, FighterComponent) and fighting_entities:
                self.world.publish(FightEvent(ent, fighting_entities[0]))
                if self.world.has_component(ent, PlayerComponent):
                    self.world.publish(AIEvent())
                    self.world.publish(NewTurnEvent())
                continue

            if self.world.has_component(ent, DungeonResidentComponent) and not self.get_entities_at(x + dx, y + dy, MovableComponent):
                continue

            gold_entities = self.get_entities_at(x + dx, y + dy, GoldComponent)
            if self.world.has_component(ent, GoldBagComponent) and gold_entities:
                self.world.publish(GoldPickUpEvent(gold_entities[0], ent))

            pos.move(dx, dy)
            sprite.move(dx, dy)

            if self.world.has_component(ent, PlayerComponent):
                self.world.publish(AIEvent())
                self.world.publish(NewTurnEvent())

    def get_entities_at(self, x: int, y: int, *component_types):
        entities = []
        for ent, (pos, *_) in self.world.get_components(PositionComponent, *component_types):
            if pos.xy() == (x, y):
                entities.append(ent)
        return entities
