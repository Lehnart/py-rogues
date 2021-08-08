class ArmorComponent:

    def __init__(self, defense: int):
        self._defense_bonus = defense

    def defense_bonus(self) -> int:
        return self._defense_bonus
