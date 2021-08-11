from typing import Tuple, Optional, List

from roguengine.esper import esper
from roguengine.systems.dungeon.components import PositionComponent, MovableComponent, DungeonComponent


class Rect:

    def __init__(self, x0: int, y0: int, w: int, h: int):
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h

    def is_in(self, x: int, y: int) -> bool:
        if self.x0 <= x < self.x0 + self.w and self.y0 <= y < self.y0 + self.h:
            return True
        return False


def get_position(world: esper.World, entity: int) -> Optional[Tuple[int, int]]:
    if not world.entity_exists(entity):
        return None

    if world.has_component(entity, PositionComponent):
        position = world.component_for_entity(entity, PositionComponent)
        return position.xy()
    return None


def get_entities_at(world: esper.World, x: int, y: int) -> List[int]:
    entities = []
    for ent, (pos, *_) in world.get_components(PositionComponent):
        if pos.xy() == (x, y):
            entities.append(ent)
    return entities


def get_entities_with_position(world: esper.World) -> List[int]:
    ents = world.get_component(PositionComponent)
    return [ent[0] for ent in ents]


def get_w_and_h(world: esper.World) -> Tuple[int, int]:
    dungeon_entity, dungeon_component = world.get_component(DungeonComponent)[0]
    return dungeon_component.width(), dungeon_component.height()


def get_room(world: esper.World, x: int, y: int) -> Optional[Rect]:
    dungeon_entity, dungeon_component = world.get_component(DungeonComponent)[0]
    rooms = [Rect(r.x0, r.y0, r.w, r.h) for r in dungeon_component.rooms() if r.is_in(x, y)]
    if not rooms:
        return None
    return rooms[0]


def is_movable(world: esper.World, x: int, y: int) -> bool:
    entities = get_entities_at(world, x, y)
    for e in entities:
        if world.has_component(e, MovableComponent):
            return True
    return False
