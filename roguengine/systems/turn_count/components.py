class TurnCountComponent:

    def __init__(self):
        self._current_turn = 0

    def get_turn(self) -> int:
        return self._current_turn

    def next(self):
        self._current_turn += 1


