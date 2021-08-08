from typing import Tuple, Optional, List

from roguengine.dungeon.components import PositionComponent, MovableComponent
from roguengine.esper import esper


def get_position(world: esper.World, entity: int) -> Optional[Tuple[int, int]]:
    if not world.entity_exists(entity):
        return None

    position = world.component_for_entity(entity, PositionComponent)
    return position.xy()


def get_entities_at(world: esper.World, x: int, y: int) -> List[int]:
    entities = []
    for ent, (pos, *_) in world.get_components(PositionComponent):
        if pos.xy() == (x, y):
            entities.append(ent)
    return entities


def is_movable(world: esper.World, x: int, y: int) -> bool:
    entities = get_entities_at(world, x, y)
    for e in entities:
        if world.has_component(e, MovableComponent):
            return True
    return False
