from roguengine.esper import esper
from roguengine.systems.gold.components import GoldComponent


def is_gold(world: esper.World, ent: int) -> bool:
    return world.has_component(ent, GoldComponent)
