from typing import Optional, Tuple, List

from roguengine.esper import esper
from roguengine.systems.render.components import VisibleSpriteComponent, InvisibleSpriteComponent


def get_sprite_position(world: esper.World, ent: int) -> Optional[Tuple[int, int]]:
    sprite = world.component_for_entity(ent, VisibleSpriteComponent)
    return sprite.top_left_pixel_position()


def get_entities_with_sprite(world: esper.World) -> List[int]:
    visible_ents = [e[0] for e in world.get_components(VisibleSpriteComponent)]
    invisible_ents = [e[0] for e in world.get_components(InvisibleSpriteComponent)]
    ents = set(visible_ents + invisible_ents)
    return list(ents)
