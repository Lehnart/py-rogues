class WeaponComponent:

    def __init__(self, atk: int):
        self._attack_bonus = atk

    def attack_bonus(self) -> int:
        return self._attack_bonus
