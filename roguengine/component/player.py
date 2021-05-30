class PlayerComponent:

    def __init__(self, level: int = 1):
        self._level = level
        self._exp = 0

    def exp(self):
        return self._exp

    def level(self) -> int:
        return self._level
