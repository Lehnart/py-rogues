from typing import Callable

from roguengine.event.key_pressed import KeyPressedEvent


class KeyCallableComponent:

    def __init__(self, key_pressed_event: KeyPressedEvent, call: Callable):
        self.key_pressed_event = key_pressed_event
        self.call = call
