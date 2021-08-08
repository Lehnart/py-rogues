from typing import Optional

from roguengine.esper import esper
from roguengine.player.components import PlayerComponent


def get_player_entity(world: esper.World) -> Optional[int]:
    entities = world.get_component(PlayerComponent)
    assert len(entities) <= 1
    return entities[0][0] if entities else None


def is_player(world: esper.World, ent: int) -> bool:
    return world.has_component(ent, PlayerComponent)
