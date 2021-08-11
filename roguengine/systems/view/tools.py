from roguengine.esper import esper
from roguengine.systems.view.components import VisibleComponent, ViewedComponent


def is_visible(world: esper.World, ent: int):
    return world.has_component(ent, VisibleComponent)


def has_been_viewed(world: esper.World, ent: int):
    return world.has_component(ent, ViewedComponent)
