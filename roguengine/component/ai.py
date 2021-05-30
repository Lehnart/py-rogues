from enum import Enum


class State(Enum):
    PASSIVE = 0,
    HOSTILE = 1,
    GUARDING = 2,


class AIComponent:

    def __init__(self, state: State, enemy: int = None):
        self._state = state
        self._enemy = enemy

    def state(self) -> State:
        return self._state

    def set_state(self, state: State):
        self._state = state

    def hostile(self, enemy: int):
        self._state = State.HOSTILE
        self._enemy = enemy

    def enemy(self) -> int:
        return self._enemy

    def set_enemy(self, enemy: int):
        self._enemy = enemy
