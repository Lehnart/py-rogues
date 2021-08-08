from roguengine.esper import esper
from roguengine.fight.components import FighterComponent


def is_fighter(world: esper.World, entity: int) -> bool:
    return world.has_component(entity, FighterComponent)
