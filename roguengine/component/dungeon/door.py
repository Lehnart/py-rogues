from enum import Enum


class DoorState(Enum):
    CLOSED = 0,
    OPEN = 1,
    BROKEN = 2


class DoorComponent:

    def __init__(self, state: DoorState = DoorState.CLOSED):
        self._state = state

    def is_closed(self):
        return self._state == DoorState.CLOSED

    def open(self):
        self._state = DoorState.OPEN
