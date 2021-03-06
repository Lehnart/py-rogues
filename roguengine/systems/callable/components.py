from typing import Callable, Type

from roguengine.rogue_esper import Event
from roguengine.systems.callable.events import KeyPressedEvent


class CallableComponent:

    def __init__(self, event_type: Type[Event], call: Callable):
        self.event_type = event_type
        self.call = call


class KeyCallableComponent:

    def __init__(self, key_pressed_event: KeyPressedEvent, call: Callable):
        self.key_pressed_event = key_pressed_event
        self.call = call
