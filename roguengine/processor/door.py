from typing import List, Dict

from roguengine.component.door import DoorComponent, DoorState
from roguengine.component.dungeon import DungeonComponent, DoorTile
from roguengine.component.position import PositionComponent
from roguengine.component.sprite import VisibleSpriteComponent, InvisibleSpriteComponent
from roguengine.esper import Processor
from roguengine.event.move import MoveEvent


class DoorProcessor(Processor):

    def __init__(self, sprites: Dict):
        super().__init__()
        self._sprites = sprites

    def process(self):
        messages: List[MoveEvent] = self.world.receive(MoveEvent)
        for msg in messages:

            ent, move = msg.entity, msg.movement
            pos = self.world.component_for_entity(ent, PositionComponent)
            x, y = pos.xy()
            dx, dy = move.dx_dy()
            nx, ny = x + dx, y + dy

            for door_ent, [door_comp, door_pos] in self.world.get_components(DoorComponent, PositionComponent):
                x, y = door_pos.xy()
                if x != nx or y != ny:
                    continue

                if not door_comp.is_closed():
                    break

                door_comp.open()

                dungeon = self.world.get_component(DungeonComponent)
                if not dungeon:
                    continue
                dungeon_entity, dungeon_component = dungeon[0]
                door_tile = dungeon_component.tile(x, y)
                if not isinstance(door_tile, DoorTile):
                    continue

                if self.world.has_component(door_ent, VisibleSpriteComponent):
                    layer = self.world.component_for_entity(door_ent, VisibleSpriteComponent).layer()
                    self.world.remove_component(door_ent, VisibleSpriteComponent)
                    sprite = self._sprites[(door_tile, DoorState.OPEN)]
                    sprite_comp = VisibleSpriteComponent(
                        x * sprite.get_width(),
                        y * sprite.get_height(),
                        sprite,
                        layer
                    )
                    self.world.add_component(door_ent, sprite_comp)

                if self.world.has_component(door_ent, InvisibleSpriteComponent):
                    layer = self.world.component_for_entity(door_ent, InvisibleSpriteComponent).layer()
                    self.world.remove_component(door_ent, InvisibleSpriteComponent)
                    sprite = self._sprites[(door_tile, DoorState.OPEN)]
                    sprite_comp = InvisibleSpriteComponent(
                        x * sprite.get_width(),
                        y * sprite.get_height(),
                        sprite,
                        layer
                    )
                    self.world.add_component(door_ent, sprite_comp)
