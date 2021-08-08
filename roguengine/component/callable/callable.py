from typing import Callable, Type

from roguengine.rogue_esper import Event


class CallableComponent:

    def __init__(self, event_type: Type[Event], call: Callable):
        self.event_type = event_type
        self.call = call
