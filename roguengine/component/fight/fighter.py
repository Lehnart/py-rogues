from enum import Enum
from typing import Optional


class Type(Enum):
    MONSTER = 0,
    HUMAN = 1


class FighterComponent:

    def __init__(self, attack: int, defense: int, hp: int, type: Type = Type.MONSTER):
        self._attack = attack
        self._defense = defense
        self._hp = hp
        self._hp_max = hp
        self._type = type
        self._last_attacker = None

    def set_last_attacker(self, ent: int):
        self._last_attacker = ent

    def last_attacker(self) -> Optional[int]:
        return self._last_attacker

    def hp(self) -> int:
        return self._hp

    def hp_max(self) -> int:
        return self._hp_max

    def attack(self) -> int:
        return self._attack

    def defense(self) -> int:
        return self._defense

    def damage(self, damage: int):
        self._hp -= damage

    def type(self) -> Type:
        return self._type
