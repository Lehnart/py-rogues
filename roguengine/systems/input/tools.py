from roguengine.esper import esper
from roguengine.systems.input.components import InputListenerComponent


def is_listening(world: esper.World, ent: int) -> bool:
    return world.has_component(ent, InputListenerComponent)
