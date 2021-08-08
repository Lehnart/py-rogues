from roguengine.esper import esper
from roguengine.systems.view.components import VisibleComponent


def is_visible(world: esper.World, ent: int):
    return world.has_component(ent, VisibleComponent)
